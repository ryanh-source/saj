"""Main application window."""
from __future__ import annotations

import ctypes
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import psutil
import pyautogui

from PySide6.QtCore import (
    Qt,
    QSize,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
    QUrl,
)
from PySide6.QtGui import QIcon, QAction, QShortcut, QKeySequence, QColor, QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSystemTrayIcon,
    QMenu,
    QVBoxLayout,
    QTableWidgetItem,

)

from saj import __version__
from saj.constants import (
    AUTO_CHECK_DELAY_SECONDS,
    CALIBRATION_STATES,
    CLICK_TAB_EVERY_ATTEMPT,
    COL_DIM,
    COL_ERROR,
    COL_EVENT,
    COL_INFO,
    COL_SUCCESS,
    COL_TS,
    COL_WARN,
    STATUS_STATES,
    TITLE_BAR_HEIGHT,
    UPDATE_STATES,
    VISIBLE_SLOTS,
)
from saj.core.game import (
    ATTEMPT_FALLBACK,
    ATTEMPT_PATTERN,
    Calibration,
    DisconnectDetector,
    SUCCESS_PATTERNS,
    open_tail,
    perform_click,
    perform_scroll,
    read_new_lines,
)
from saj.core.system import (
    FavoritesWatcher,
    load_settings,
    player_log_path,
    read_favorites_count,
    save_settings,
    settings_path,
)
from saj.core.worker import WorkerSignals
from saj.generated import resources_rc
from saj.generated.index_ui import Ui_MainWindow
from saj.ui.widgets import IconHoverButton, JoinOrderEditor, Toast
from saj.updater.client import UpdateChecker, is_newer
from saj.updater.installer import install_update_and_relaunch


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("SAJ")
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowIcon(QIcon(":/images/images/app_icon.ico"))

        # Setup Signals
        self.signals = WorkerSignals()
        self.signals.log_line.connect(self._log_to_widget)
        self.signals.status.connect(self._set_status_widget)
        self.signals.calibration_label.connect(self._set_calibration_label)
        self.signals.set_running.connect(self._set_running_state)
        self.signals.current_slot.connect(self._set_current_slot_widget)
        self.signals.attempts.connect(self._set_attempts_widget)
        self.signals.show_window.connect(self.show_and_raise)
        self.signals.toast.connect(self._on_toast)

        # Track attempt count for the current run
        self._attempt_count = 0

        self.ui.time.setAlignment(Qt.AlignCenter)
        # status and calibrated are now QPushButtons; alignment is handled via stylesheet.
        # Make them feel like buttons (cursor) but not interactive (no checked state).
        self.ui.status.setCursor(Qt.ArrowCursor)
        self.ui.status.setCheckable(False)
        self.ui.status.setFocusPolicy(Qt.NoFocus)
        self.ui.calibrated.setCursor(Qt.ArrowCursor)
        self.ui.calibrated.setCheckable(False)
        self.ui.calibrated.setFocusPolicy(Qt.NoFocus)

        # ---- Join order chip editor ---------------------------------------
        # Mount the chip editor inside join_order_frame (added in Designer).
        # Qt cascades parent stylesheets to children, so any styling on the
        # frame (background, border) bleeds into our chips. Scope the frame's
        # own stylesheet to itself so it doesn't pollute children.
        existing_ss = self.ui.join_order_frame.styleSheet()
        if existing_ss and "QFrame#join_order_frame" not in existing_ss:
            # Re-wrap whatever Designer put on the frame to target only the frame.
            self.ui.join_order_frame.setStyleSheet(
                f"QFrame#join_order_frame {{ {existing_ss} }}"
            )
        self.join_order_editor = JoinOrderEditor(self.ui.join_order_frame)
        editor_layout = QVBoxLayout(self.ui.join_order_frame)
        editor_layout.setContentsMargins(4, 4, 4, 4)
        editor_layout.addWidget(self.join_order_editor)
        # Watch favorites.txt for changes; auto-refresh chips.
        self.favorites_watcher = FavoritesWatcher(self)
        self.favorites_watcher.favorites_changed.connect(
            self.join_order_editor.set_favorites_count
        )
        # Save settings on every edit so the order persists immediately.
        self.join_order_editor.order_changed.connect(self._on_order_changed)
        # Initial count from disk
        self.join_order_editor.set_favorites_count(read_favorites_count(default=0))

        # OCR-based disconnect detector. Initialized once so the OCR engine
        # is reused across attempts (creation takes ~50ms).
        self.disconnect_detector = DisconnectDetector()
        # Defer the status log until after the window is fully constructed
        # so it appears at the bottom of the boot messages rather than mid-init.
        _ocr_ready = self.disconnect_detector.available
        QTimer.singleShot(0, lambda: self._emit_log(
            "Fast-fail OCR detector ready." if _ocr_ready
            else "Fast-fail OCR detector unavailable — using log-based detection only.",
            "dim",
        ))

        # Restore persisted state
        s = load_settings()
        cal_data = s.get("calibration") or {}

        def _to_tuple(v):
            return tuple(v) if isinstance(v, list) and len(v) == 2 else None

        self.cal_servers: Optional[tuple[int, int]] = _to_tuple(cal_data.get("servers"))
        self.cal_tab: Optional[tuple[int, int]] = _to_tuple(cal_data.get("tab"))
        self.cal_slot1: Optional[tuple[int, int]] = _to_tuple(cal_data.get("slot1"))
        self.cal_slot2: Optional[tuple[int, int]] = _to_tuple(cal_data.get("slot2"))

        # Restore the join order. Prefer the new list-based key; fall back
        # to parsing the old comma-separated string for back-compat.
        saved_list = s.get("join_order_list")
        if isinstance(saved_list, list):
            self.join_order_editor.set_order(
                [int(x) for x in saved_list if isinstance(x, (int, str)) and str(x).strip().isdigit()]
            )
        else:
            legacy = s.get("order", "")
            if isinstance(legacy, str) and legacy.strip():
                try:
                    parsed = [int(t.strip()) for t in legacy.split(",") if t.strip()]
                    self.join_order_editor.set_order(parsed)
                except ValueError:
                    pass
        self.ui.time.setText(f"{s.get('interval', 6.0)}s")

        # Workers
        self._worker: Optional[threading.Thread] = None
        self._stop_evt = threading.Event()
        self._cal_thread: Optional[threading.Thread] = None
        self._drag_pos = None

        # Wire main UI buttons
        self.ui.calibrate_position.clicked.connect(self.on_calibrate_clicked)
        self.ui.start.clicked.connect(self.on_start_clicked)
        self.ui.stop.clicked.connect(self.on_stop_clicked)
        self.ui.calibrate_position.setCheckable(False)
        self.ui.start.setCheckable(False)
        self.ui.stop.setCheckable(False)
        self.ui.stop.setEnabled(False)

        # Initialize UI Components
        self._build_title_bar()
        self._shift_content_below_title_bar()
        self._init_log_area()
        self._setup_system_tray()  # Initialize Tray

        self._set_status_widget("idle", "")
        self._refresh_calibration_label()
        self._check_dependencies()
        self._register_hotkeys()
        self._wire_settings_page()
        self._wire_updates_page()

        # Open on home_page (instant, no fade on first show) and sync nav highlights
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page)
        self._update_nav_state()

        # Start background game watcher
        self.watcher_thread = threading.Thread(target=self._watch_for_game, daemon=True)
        self.watcher_thread.start()

        # Restore last window position, if any
        pos = load_settings().get("window_pos")
        if isinstance(pos, list) and len(pos) == 2:
            try:
                x, y = int(pos[0]), int(pos[1])
                # Sanity check: make sure the position is on a visible screen.
                # Without this, unplugging a second monitor would strand the
                # window off-screen forever.
                from PySide6.QtGui import QGuiApplication
                screens = QGuiApplication.screens()
                on_screen = any(
                    scr.availableGeometry().contains(x + 50, y + 50)
                    for scr in screens
                )
                if on_screen:
                    self.move(x, y)
            except (TypeError, ValueError):
                pass

    
    # ----- Window Management -----
    def show_and_raise(self) -> None:
        """Brings the window out of the tray and to the top of the screen."""
        self.setWindowOpacity(1.0)
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def _on_toast(self, title: str, subtitle: str, kind: str) -> None:
        """Show a slide-down toast under the title bar."""
        reduce_motion = bool(load_settings().get("reduce_motion", False))
        Toast.show_toast(
            self,
            title=title,
            subtitle=subtitle,
            kind=kind,
            duration_ms=3000,
            title_bar_height=TITLE_BAR_HEIGHT,
            reduce_motion=reduce_motion,
        )

    def _fade_window_out(self, on_done) -> None:
        """Fade window opacity to 0 over ~200ms, then call on_done()."""
        if not hasattr(self, "_window_fade_anim"):
            self._window_fade_anim = QPropertyAnimation(self, b"windowOpacity")
            self._window_fade_anim.setEasingCurve(QEasingCurve.InOutQuad)

        self._window_fade_anim.stop()
        try:
            self._window_fade_anim.finished.disconnect()
        except (RuntimeError, TypeError):
            pass

        def _finish():
            on_done()
            # Reset opacity for next time the window is shown.
            self.setWindowOpacity(1.0)

        self._window_fade_anim.finished.connect(_finish)
        self._window_fade_anim.setDuration(200)
        self._window_fade_anim.setStartValue(self.windowOpacity())
        self._window_fade_anim.setEndValue(0.0)
        self._window_fade_anim.start()

    def _fade_and_minimize(self) -> None:
        self._fade_window_out(self.showMinimized)

    def _fade_and_hide(self) -> None:
        self._save_window_position()
        # If the tray is disabled, there's nowhere to "hide" to — quit instead.
        if bool(load_settings().get("tray_enabled", True)):
            self._fade_window_out(self.hide)
        else:
            self._fade_window_out(QApplication.instance().quit)

    # ----- Window Position Persistence -----
    def _save_window_position(self) -> None:
        """Persist current window position so it reopens where the user left it."""
        s = load_settings()
        s["window_pos"] = [self.x(), self.y()]
        save_settings(s)

    def _save_and_quit(self) -> None:
        self._save_window_position()
        QApplication.instance().quit()

    # ----- Background Watcher -----
    def _watch_for_game(self) -> None:
        game_process_name = "SCPSL.exe"
        was_running = False

        while True:
            try:
                # Check if the process is currently active
                is_running = any(
                    proc.name() == game_process_name
                    for proc in psutil.process_iter(['name'])
                )

                if is_running and not was_running:
                    # Only auto-open SAJ if the user has opted in.
                    if bool(load_settings().get("auto_launch", False)):
                        self.signals.log_line.emit("SCP:SL detected! Opening SAJ...", "event")
                        self.signals.show_window.emit()

                was_running = is_running
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Ignore transient process access errors
                pass

            # Use the user-configured poll interval (falls back to 3s if unset)
            time.sleep(getattr(self, "_poll_seconds", 3))

    # ----- System Tray Setup -----
    def _setup_system_tray(self) -> None:
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(":/images/images/app_icon.ico"))
        self.tray_icon.setToolTip("SAJ - SCP:SL Auto-Joiner")

        # Create Right-Click Menu
        tray_menu = QMenu()

        show_action = QAction("Show UI", self)
        show_action.triggered.connect(self.show_and_raise)
        tray_menu.addAction(show_action)

        quit_action = QAction("Quit SAJ", self)
        quit_action.triggered.connect(self._save_and_quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

        # Only show the tray icon if the user has it enabled in settings.
        if bool(load_settings().get("tray_enabled", True)):
            self.tray_icon.show()

        # Double click to show
        self.tray_icon.activated.connect(self._tray_activated)

    def _apply_tray_enabled(self, enabled: bool) -> None:
        """Show or hide the tray icon to match the setting."""
        if not hasattr(self, "tray_icon"):
            return
        if enabled:
            self.tray_icon.show()
        else:
            self.tray_icon.hide()
        self._update_close_btn_tooltip()

    def _update_close_btn_tooltip(self) -> None:
        """Reflect what the close button will actually do based on tray state."""
        if not hasattr(self, "close_btn"):
            return
        if bool(load_settings().get("tray_enabled", True)):
            self.close_btn.setToolTip("Close to Tray")
        else:
            self.close_btn.setToolTip("Quit SAJ")

    # Registry key + value name used for "Open on Windows startup".
    _STARTUP_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    _STARTUP_REG_NAME = "SAJ"

    def _startup_command(self) -> str:
        """Build the command Windows should run at login.

        When frozen (PyInstaller .exe), point at the executable directly.
        When running from source, run the current Python with this script.
        The --minimized flag tells main() to start hidden in the tray.
        """
        if getattr(sys, "frozen", False):
            return f'"{sys.executable}" --minimized'
        script = os.path.abspath(sys.argv[0])
        return f'"{sys.executable}" "{script}" --minimized'

    def _apply_open_startup(self, enabled: bool) -> None:
        """Add or remove the SAJ entry from the Windows Run key."""
        if not sys.platform.startswith("win"):
            return
        try:
            import winreg
        except ImportError:
            return

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self._STARTUP_REG_PATH,
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE,
            ) as key:
                if enabled:
                    winreg.SetValueEx(
                        key,
                        self._STARTUP_REG_NAME,
                        0,
                        winreg.REG_SZ,
                        self._startup_command(),
                    )
                else:
                    try:
                        winreg.DeleteValue(key, self._STARTUP_REG_NAME)
                    except FileNotFoundError:
                        # Already absent — nothing to do.
                        pass
        except OSError as e:
            self._emit_log(f"Could not update startup setting: {e}", "warn")

    def _tray_activated(self, reason) -> None:
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_and_raise()

    # ----- Custom Title Bar -----
    def _build_title_bar(self) -> None:
        self.title_bar = QFrame(self)
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setFixedHeight(TITLE_BAR_HEIGHT)
        self.title_bar.setGeometry(0, 0, self.width(), TITLE_BAR_HEIGHT)
        self.title_bar.setStyleSheet("""
            QFrame#titleBar {
                background-color: #1a1a1a;
                border-bottom: 1px solid #2c2c2e;
            }
            QLabel#titleLabel {
                color: #c8c8c8;
                background-color: transparent;
                font-family: 'Manrope';
                font-weight: bold;
                font-size: 13px;
                border: none;
            }
        """)

        layout = QHBoxLayout(self.title_bar)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        BTN_W = 30
        BTN_H = TITLE_BAR_HEIGHT - 12

        # Settings (far left)
        self.settings_btn = IconHoverButton(
            icon_normal=":/images/images/cog-gray.png",
            icon_hover=":/images/images/cog-white.png",
            icon_size=14,
            hover_bg="#1f1f25",
            parent=self.title_bar,
            spin_on_hover=True,
        )
        self.settings_btn.setFixedSize(BTN_W, BTN_H)
        self.settings_btn.setToolTip("Settings")
        self.settings_btn.clicked.connect(self._show_settings_page)
        layout.addWidget(self.settings_btn)

        # Home (right of settings)
        self.home_btn = IconHoverButton(
            icon_normal=":/images/images/house-gray.png",
            icon_hover=":/images/images/house-blue.png",
            icon_size=14,
            hover_bg="#1f1f25",
            parent=self.title_bar,
        )
        self.home_btn.setFixedSize(BTN_W, BTN_H)
        self.home_btn.setToolTip("Home")
        self.home_btn.clicked.connect(self._show_home_page)
        layout.addWidget(self.home_btn)

        self.updates_btn = IconHoverButton(
            icon_normal=":/images/images/download-gray-title.png",
            icon_hover=":/images/images/download-white-title.png",
            icon_size=14,
            hover_bg="#1f1f25",
            parent=self.title_bar,
        )
        self.updates_btn.setFixedSize(BTN_W, BTN_H)
        self.updates_btn.setToolTip("Updates")
        self.updates_btn.clicked.connect(self._show_updates_page)
        layout.addWidget(self.updates_btn)

        # Stretch on both sides of the title to keep it centered
        layout.addStretch()

        self.title_label = QLabel("SAJ")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        layout.addStretch()

        # Pin
        self.pin_btn = IconHoverButton(
            icon_normal=":/images/images/pin-gray.png",
            icon_hover=":/images/images/pin-blue.png",
            icon_size=14,
            hover_bg="#1f1f25",
            parent=self.title_bar,
        )
        self.pin_btn.setFixedSize(BTN_W, BTN_H)
        self.pin_btn.setToolTip("Toggle always-on-top")
        self.pin_btn.set_locked(True)
        self.pin_btn.clicked.connect(self._toggle_pin)
        layout.addWidget(self.pin_btn)

        # Minimize
        self.min_btn = IconHoverButton(
            icon_normal=":/images/images/min-gray.png",
            icon_hover=":/images/images/min-white.png",
            icon_size=14,
            hover_bg="#1f1f25",
            parent=self.title_bar,
        )
        self.min_btn.setFixedSize(BTN_W, BTN_H)
        self.min_btn.setToolTip("Minimize")
        self.min_btn.clicked.connect(self._fade_and_minimize)
        layout.addWidget(self.min_btn)

        # Close -> hides to tray when tray is enabled, quits otherwise.
        self.close_btn = IconHoverButton(
            icon_normal=":/images/images/x-solid.png",
            icon_hover=":/images/images/x-solid-full.png",
            icon_size=14,
            hover_bg="rgba(239, 68, 68, 100)",
            parent=self.title_bar,
        )
        self.close_btn.setFixedSize(BTN_W, BTN_H)
        self._update_close_btn_tooltip()
        self.close_btn.clicked.connect(self._fade_and_hide)
        layout.addWidget(self.close_btn)

        self.title_bar.raise_()

    def _show_home_page(self) -> None:
        self._fade_to_page(self.ui.home_page)

    def _show_settings_page(self) -> None:
        self._fade_to_page(self.ui.settings_page)

    def _show_updates_page(self) -> None:
        target = getattr(self.ui, "updates_page", None)
        if target is None:
            self._emit_log("Updates page is not defined in the .ui file.", "warn")
            return
        self._fade_to_page(target)

    def _fade_to_page(self, target_page) -> None:
        """Cross-fade the stacked widget to a new page (~250ms total)."""
        sw = self.ui.stackedWidget
        if sw.currentWidget() is target_page:
            # Already on this page — re-sync nav state in case Qt's auto-toggle
            # un-checked the active button on click.
            self._update_nav_state()
            return

        # Reduce motion: skip the fade, just swap instantly.
        if load_settings().get("reduce_motion", False):
            sw.setCurrentWidget(target_page)
            self._update_nav_state()
            return

        # Lazy-init opacity effect + animation on the stacked widget.
        if not hasattr(self, "_page_effect"):
            self._page_effect = QGraphicsOpacityEffect(sw)
            self._page_effect.setOpacity(1.0)
            sw.setGraphicsEffect(self._page_effect)
            self._page_anim = QPropertyAnimation(self._page_effect, b"opacity")
            self._page_anim.setEasingCurve(QEasingCurve.InOutQuad)

        self._page_anim.stop()

        def _on_fade_out_done():
            try:
                self._page_anim.finished.disconnect(_on_fade_out_done)
            except (RuntimeError, TypeError):
                pass
            sw.setCurrentWidget(target_page)
            self._update_nav_state()
            # Fade back in
            self._page_anim.setDuration(125)
            self._page_anim.setStartValue(0.0)
            self._page_anim.setEndValue(1.0)
            self._page_anim.start()

        self._page_anim.finished.connect(_on_fade_out_done)
        self._page_anim.setDuration(125)
        self._page_anim.setStartValue(self._page_effect.opacity())
        self._page_anim.setEndValue(0.0)
        self._page_anim.start()

    def _update_nav_state(self) -> None:
        """Highlight the active page's nav button (white icon locked on)."""
        current = self.ui.stackedWidget.currentWidget()
        on_home = current is self.ui.home_page
        on_updates = current is getattr(self.ui, "updates_page", None)
        on_settings = current is self.ui.settings_page

        self.home_btn.set_locked(on_home)
        if hasattr(self, "updates_btn"):
            self.updates_btn.set_locked(on_updates)
        self.settings_btn.set_locked(on_settings)

    # ----- Updates Page -----
    def _wire_updates_page(self) -> None:
        """Hook up the updates page widgets and kick off an initial check.

        Expected widgets on self.ui (named in Qt Designer):
            update_status      QPushButton or QLabel — status pill
            installed_version  QLabel
            last_checked       QLabel
            release_notes      QTextBrowser
            download_update    QPushButton — primary action
            check_updates      QPushButton — secondary action
        """
        self._updater = UpdateChecker(self)
        sigs = self._updater.signals
        sigs.state_changed.connect(self._on_update_state_changed)
        sigs.latest_version.connect(self._on_latest_version)
        sigs.release_notes.connect(self._on_release_notes)
        sigs.last_checked.connect(self._on_last_checked)
        sigs.download_progress.connect(self._on_download_progress)
        sigs.download_done.connect(self._on_download_done)
        sigs.error.connect(self._on_update_error)
        sigs.releases_list.connect(self._on_releases_list)

        # Hook buttons
        dl_btn = getattr(self.ui, "download_update", None)
        if dl_btn is not None:
            dl_btn.clicked.connect(self._on_download_clicked)
        check_btn = getattr(self.ui, "check_updates", None)
        if check_btn is not None:
            check_btn.clicked.connect(self._on_check_clicked)

        # Installed version is constant — set once, never changes at runtime
        installed_lbl = getattr(self.ui, "installed_version", None)
        if installed_lbl is not None:
            installed_lbl.setTextFormat(Qt.RichText)
            installed_lbl.setText(
                f'<span style="color: #e6e8ec; font-weight: 500;">'
                f'v{__version__}'
                f'</span>'
            )

        # Last-checked starts as "never" until the first check completes.
        last_lbl = getattr(self.ui, "last_checked", None)
        if last_lbl is not None:
            last_lbl.setText("Last checked: never")

        # Empty out release-notes panel until data.
        notes = getattr(self.ui, "release_notes", None)
        if notes is not None:
            notes.setHtml("")

        # Previous-releases table setup.
        releases_table = getattr(self.ui, "releases_table", None)
        if releases_table is not None:
            from PySide6.QtWidgets import QHeaderView, QAbstractItemView

            releases_table.setColumnCount(3)
            releases_table.setHorizontalHeaderLabels(["Version", "Notes", "Released"])
            releases_table.verticalHeader().setVisible(False)
            releases_table.horizontalHeader().setHighlightSections(False)
            releases_table.horizontalHeader().setStretchLastSection(False)
            releases_table.setShowGrid(False)
            releases_table.setSelectionMode(QAbstractItemView.NoSelection)
            releases_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            releases_table.setAlternatingRowColors(False)
            

            header = releases_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            # Double-click a row → open that release page on GitHub
            releases_table.cellDoubleClicked.connect(
                self._on_release_row_double_clicked
            )

        # Cache for the URLs (row index → html_url) so double-click opens
        # the right page. Populated by _on_releases_list.
        self._release_urls: list[str] = []

        if AUTO_CHECK_DELAY_SECONDS > 0:
            self._set_update_status("checking")
        else:
            self._set_update_status("idle")

        # Auto-check shortly after launch, off the GUI thread. Also kick off
        # the releases-list fetch on the same schedule so both API calls happen
        # together rather than scattered.
        if AUTO_CHECK_DELAY_SECONDS > 0:
            QTimer.singleShot(
                AUTO_CHECK_DELAY_SECONDS * 1000,
                self._updater.check_for_updates,
            )
            QTimer.singleShot(
                AUTO_CHECK_DELAY_SECONDS * 1000,
                lambda: self._updater.fetch_releases(limit=10),
            )

    def _on_check_clicked(self) -> None:
        self._updater.check_for_updates()

    def _on_download_clicked(self) -> None:
        # If a download is already running, treat the click as a cancel.
        if self._updater._download_thread and self._updater._download_thread.is_alive():
            self._updater.cancel_download()
            print("downloaded")
            return
        self._updater.download_and_install()

    def _on_update_state_changed(self, state: str) -> None:
        self._set_update_status(state)

        dl_btn = getattr(self.ui, "download_update", None)
        check_btn = getattr(self.ui, "check_updates", None)

        if state == "checking":
            if dl_btn is not None:
                dl_btn.setEnabled(False)
                dl_btn.setText("CHECKING…")
            if check_btn is not None:
                check_btn.setEnabled(False)

        elif state == "available":
            if dl_btn is not None:
                dl_btn.setEnabled(True)
                dl_btn.setText("DOWNLOAD && INSTALL")
            if check_btn is not None:
                check_btn.setEnabled(True)
                check_btn.setText("CHECK AGAIN")
            self._set_updates_badge(True)

        elif state == "up_to_date":
            if dl_btn is not None:
                dl_btn.setEnabled(False)
                dl_btn.setText("DOWNLOAD && INSTALL")
            if check_btn is not None:
                check_btn.setEnabled(True)
                check_btn.setText("CHECK FOR UPDATES")
            self._set_updates_badge(False)

        elif state == "downloading":
            if dl_btn is not None:
                dl_btn.setEnabled(True)
                dl_btn.setText("CANCEL")
            if check_btn is not None:
                check_btn.setEnabled(False)

        elif state == "installing":
            if dl_btn is not None:
                dl_btn.setEnabled(False)
                dl_btn.setText("INSTALLING…")
            if check_btn is not None:
                check_btn.setEnabled(False)

        elif state == "error":
            if dl_btn is not None:
                dl_btn.setEnabled(bool(self._updater._download_url))
                dl_btn.setText("DOWNLOAD && INSTALL")
            if check_btn is not None:
                check_btn.setEnabled(True)
                check_btn.setText("RETRY")

        else:  # idle
            if dl_btn is not None:
                dl_btn.setEnabled(False)
                dl_btn.setText("DOWNLOAD && INSTALL")
            if check_btn is not None:
                check_btn.setEnabled(True)
                check_btn.setText("CHECK FOR UPDATES")

    def _set_update_status(self, state: str) -> None:
        """Apply pill styling and icon to the update_status widget."""
        cfg = UPDATE_STATES.get(state, UPDATE_STATES["idle"])
        widget = getattr(self.ui, "update_status", None)
        if widget is None:
            return

        widget.setText(cfg["text"])

        icon_path = cfg.get("icon")
        if icon_path and hasattr(widget, "setIcon"):
            icon = QIcon(icon_path)
            if icon.isNull():
                missing_set = getattr(self, "_warned_missing_icons", set())
                if icon_path not in missing_set:
                    print(f"[update] Icon not found in qrc: {icon_path}")
                    missing_set.add(icon_path)
                    self._warned_missing_icons = missing_set
                widget.setIcon(QIcon())
            else:
                widget.setIcon(icon)
            widget.setIconSize(QSize(20, 20))

        h = widget.height() if widget.height() > 0 else 40
        radius = h // 2

        widget.setStyleSheet(f"""
            QPushButton, QLabel {{
                background-color: {cfg["bg"]};
                border: 1px solid {cfg["border"]};
                border-radius: {radius}px;
                color: {cfg["color"]};
                padding: 0;
            }}
            QPushButton:hover, QPushButton:pressed, QPushButton:disabled {{
                background-color: {cfg["bg"]};
                border: 1px solid {cfg["border"]};
                color: {cfg["color"]};
            }}
        """)
        widget.update()

        # Hide the progress arc unless in a downloading state
        if hasattr(widget, "set_progress"):
            if state in ("downloading", "installing"):
                # Color the arc to match the state
                widget.set_arc_color(cfg["color"])
                # Don't reset progress here
            else:
                widget.set_progress(-1)

    def _toast_update(self, title: str, subtitle: str, kind: str = "info") -> None:
        """Show an update related toast."""
        self.signals.toast.emit(title, subtitle, kind)

    def _set_updates_badge(self, on: bool) -> None:
        """Swap the updates button's icons to the badged or un-badged set."""
        btn = getattr(self, "updates_btn", None)
        if btn is None:
            return

        if on:
            normal_path = ":/images/images/download-available-gray.png"
            hover_path  = ":/images/images/download-available-white.png"
        else:
            normal_path = ":/images/images/download-gray-title.png"
            hover_path  = ":/images/images/download-white-title.png"

        btn._icon_normal = QIcon(normal_path)
        btn._icon_hover  = QIcon(hover_path)
        size = QSize(btn._icon_size, btn._icon_size)
        btn._pixmap_normal = btn._icon_normal.pixmap(size)
        btn._pixmap_hover  = btn._icon_hover.pixmap(size)

        # Show the right one based on current hover/locked state.
        hovered = btn.underMouse() or getattr(btn, "_locked_hover", False)
        btn.setIcon(btn._icon_hover if hovered else btn._icon_normal)

    def _on_latest_version(self, version: str) -> None:
        widget = getattr(self.ui, "installed_version", None)
        if widget is None:
            return

        # No data yet — just show the installed version, dim
        if not version or version == "unknown":
            widget.setText(
                f'<span style="color: rgba(230,232,236,0.45);">'
                f'v{__version__}'
                f'</span>'
            )
            return

        up_to_date = not is_newer(version, __version__)

        if up_to_date:
            # Calm white
            widget.setText(
                f'<span style="color: #e6e8ec; font-weight: 500;">'
                f'v{__version__}'
                f'</span>'
            )
        else:
            # Installed (dim) → latest (amber, highlighted)
            widget.setText(
                f'<span style="color: rgba(230,232,236,0.45);">'
                f'v{__version__}'
                f'</span>'
                f'<span style="color: rgba(230,232,236,0.4);">'
                f'&nbsp;&nbsp;→&nbsp;&nbsp;'
                f'</span>'
                f'<span style="color: #f4b860; font-weight: 500;">'
                f'{version}'
                f'</span>'
            )

        widget.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                padding: 0;
                font-family: 'Manrope';
                font-size: 14px;
            }
        """)

    def _on_release_notes(self, version: str, body: str) -> None:
        notes = getattr(self.ui, "release_notes", None)
        if notes is None:
            return

        if not body:
            notes.setHtml(
                f'<div style="color:#6b7280; font-size:11px; letter-spacing:1.2px;">'
                f'RELEASE NOTES — {self._escape_html(version)}</div>'
                f'<p style="color:#9ca3af; font-size:13px; margin-top:8px;">'
                f'No release notes provided.</p>'
            )
            return

        # Convert simple Markdown bullets to <li> so it renders as a list.
        lines = body.splitlines()
        items = []
        paragraphs = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(("- ", "* ", "+ ")):
                items.append(self._escape_html(stripped[2:].strip()))
            elif stripped:
                paragraphs.append(self._escape_html(stripped))

        html = (
            f'<div style="color:#6b7280; font-size:11px; letter-spacing:1.2px; '
            f'margin-bottom:8px;">RELEASE NOTES — {self._escape_html(version)}</div>'
        )
        if paragraphs:
            html += (
                '<p style="color:#c8c8c8; font-size:13px; margin:0 0 8px 0;">'
                + "<br>".join(paragraphs)
                + "</p>"
            )
        if items:
            html += '<ul style="color:#c8c8c8; font-size:13px; margin-left:-20px;">'
            html += "".join(f"<li>{i}</li>" for i in items)
            html += "</ul>"

        notes.setHtml(html)

    def _on_last_checked(self, ts: str) -> None:
        widget = getattr(self.ui, "last_checked", None)
        if widget is None:
            return
        if not ts or ts == "never":
            widget.setText("Last checked: never")
        else:
            widget.setText(f"Last checked: {ts}")

    def _on_download_progress(self, pct: int) -> None:
        status_widget = getattr(self.ui, "update_status", None)
        if status_widget is not None and hasattr(status_widget, "set_progress"):
            status_widget.set_progress(pct)

    def _on_download_done(self, path: str) -> None:
        self._emit_log(f"Update downloaded to {path}", "success")
        self._toast_update(
            "Update ready",
            "Open Folder and Close",
            "success",
        )
        QTimer.singleShot(100, lambda: install_update_and_relaunch(path))

    def _on_update_error(self, msg: str) -> None:
        self._emit_log(f"Update: {msg}", "warn")
        self._toast_update("Update check failed", msg, "warn")

    # Releases of previous versions 
    def _on_releases_list(self, releases: list) -> None:
        """Populate the previous-releases table."""
        table = getattr(self.ui, "releases_table", None)
        if table is None:
            return

        self._release_urls = [r.get("html_url", "") for r in releases]

        table.setRowCount(len(releases))

        for row, r in enumerate(releases):
            tag = r.get("tag", "")
            body = r.get("body", "")
            published = self._format_release_date(r.get("published", ""))

            # Column 0: version (with "installed" marker if it matches current)
            version_item = QTableWidgetItem(tag)
            if tag.lstrip("v") == __version__.lstrip("v"):
                version_item.setText(f"{tag}  • installed")
                version_item.setForeground(QColor("#4ade80"))
            else:
                version_item.setForeground(QColor("#e6e8ec"))
            table.setItem(row, 0, version_item)

            # Column 1: short summary (first content line of body, truncated)
            summary = self._summarize_release_body(body)
            notes_item = QTableWidgetItem(summary)
            notes_item.setForeground(QColor(230, 232, 236, 180))
            notes_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, notes_item)

            # Column 2: date
            date_item = QTableWidgetItem(published)
            date_item.setForeground(QColor(230, 232, 236, 130))
            date_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            table.setItem(row, 2, date_item)

    def _format_release_date(self, iso_ts: str) -> str:
        """Convert '2026-05-05T11:24:00Z' → 'May 5, 2026'."""
        if not iso_ts:
            return ""
        try:
            dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
            return dt.strftime("%b %d, %Y")
        except (ValueError, TypeError):
            return iso_ts[:10]  # fallback: just the date portion

    def _summarize_release_body(self, body: str) -> str:
        """Return a short, single-line summary of a release body."""
        if not body:
            return "—"
        for raw in body.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):  # markdown heading — skip
                continue
            if line.startswith(("-", "*", "+")):
                line = line.lstrip("-*+ ").strip()
            if len(line) > 80:
                line = line[:77] + "…"
            return line
        return "—"

    def _on_release_row_double_clicked(self, row: int, _col: int) -> None:
        """Open the release page on GitHub in the default browser."""
        if 0 <= row < len(self._release_urls):
            url = self._release_urls[row]
            if url:
                QDesktopServices.openUrl(QUrl(url))

    # ----- Settings Page -----
    # Map of toggle button objectName -> (settings key, default value)
    _TOGGLE_SETTINGS = {
        "system_tray":   ("tray_enabled",     True),
        "auto_launch":   ("auto_launch",      False),
        "open_startup":  ("open_startup",     False),
        "reduce_motion": ("reduce_motion",    False),
        "always_on_top": ("always_on_top",    True),
    }

    _ICON_TOGGLE_ON = ":/images/images/toggle-on-solid.png"
    _ICON_TOGGLE_OFF = ":/images/images/toggle-off-solid.png"

    def _wire_settings_page(self) -> None:
        """Hook up toggles + action buttons on the settings page. Call once from __init__."""
        s = load_settings()

        # Toggles — load saved state, set icon, connect click handler
        for attr, (key, default) in self._TOGGLE_SETTINGS.items():
            btn = getattr(self.ui, attr, None)
            if btn is None:
                continue
            state = bool(s.get(key, default))
            btn._is_on = state
            btn.setIcon(QIcon(self._ICON_TOGGLE_ON if state else self._ICON_TOGGLE_OFF))
            btn.setIconSize(QSize(64, 36))
            # Strip any default button chrome so only the icon shows
            btn.setStyleSheet("QPushButton { background: transparent; border: none; padding: 0; }")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, b=btn, k=key: self._on_toggle_clicked(b, k))

        # Action buttons — set icons + connect handlers
        action_buttons = [
            ("open_settings_folder", ":/images/images/folder-solid.png",    self._open_settings_folder),
            ("clear_log",            ":/images/images/eraser-solid.png",    self._clear_log),
            ("reset_calibration",    ":/images/images/trash-can-solid.png", self._reset_calibration),
        ]
        for attr, icon_path, handler in action_buttons:
            btn = getattr(self.ui, attr, None)
            if btn is None:
                continue
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(14, 14))
            btn.clicked.connect(handler)

        # Poll interval combo box — populate with options + wire to settings
        poll_combo = getattr(self.ui, "poll_interval", None)
        if poll_combo is not None:
            poll_combo.clear()
            # Each entry: (display label, seconds value)
            self._poll_options = [
                ("1 second", 1),
                ("2 seconds", 2),
                ("3 seconds", 3),
                ("5 seconds", 5),
                ("10 seconds", 10),
            ]
            for label, _ in self._poll_options:
                poll_combo.addItem(label)

            # Restore saved value (default 3s to match existing hardcoded sleep)
            saved = int(s.get("poll_interval", 3))
            self._poll_seconds = saved
            for i, (_, val) in enumerate(self._poll_options):
                if val == saved:
                    poll_combo.setCurrentIndex(i)
                    break

            poll_combo.currentIndexChanged.connect(self._on_poll_interval_changed)

        # About card — version label, populated from __version__
        version_lbl = getattr(self.ui, "app_version", None)
        if version_lbl is not None:
            version_lbl.setText(f"v{__version__}")

        # Apply settings that have side effects on launch
        self._apply_reduce_motion(bool(s.get("reduce_motion", False)))
        self._apply_always_on_top(bool(s.get("always_on_top", True)))
        self._apply_open_startup(bool(s.get("open_startup", False)))

    def _on_poll_interval_changed(self, index: int) -> None:
        if not (0 <= index < len(self._poll_options)):
            return
        _, seconds = self._poll_options[index]
        self._poll_seconds = seconds
        s = load_settings()
        s["poll_interval"] = seconds
        save_settings(s)

    def _on_toggle_clicked(self, btn, key: str) -> None:
        new_state = not getattr(btn, "_is_on", False)
        btn._is_on = new_state
        btn.setIcon(QIcon(self._ICON_TOGGLE_ON if new_state else self._ICON_TOGGLE_OFF))

        # Persist to settings.json (merge with existing)
        s = load_settings()
        s[key] = new_state
        save_settings(s)

        # Apply side effects for toggles that change behavior immediately.
        if key == "reduce_motion":
            self._apply_reduce_motion(new_state)
        elif key == "tray_enabled":
            self._apply_tray_enabled(new_state)
        elif key == "always_on_top":
            self._apply_always_on_top(new_state)
        elif key == "open_startup":
            self._apply_open_startup(new_state)
        # auto_launch needs no immediate side effect.

    def _apply_reduce_motion(self, enabled: bool) -> None:
        """Disable/enable animations everywhere they're used."""
        if hasattr(self, "settings_btn"):
            sb = self.settings_btn
            if hasattr(sb, "_spin_anim"):
                sb._spin_anim.stop()
            sb._rotation = 0.0
            # Reset to the un-rotated source icon directly.
            hovered = sb.underMouse() or getattr(sb, "_locked_hover", False)
            sb.setIcon(QIcon(sb._pixmap_hover if hovered else sb._pixmap_normal))
            # Now apply the new flag — enterEvent will respect it next time.
            sb._spin_on_hover = not enabled

    def _open_settings_folder(self) -> None:
        folder = settings_path().parent
        try:
            folder.mkdir(parents=True, exist_ok=True)
            if sys.platform.startswith("win"):
                os.startfile(str(folder))
            self._emit_log(f"Opened settings folder: {folder}", "dim")
        except Exception as e:
            self._emit_log(f"Could not open settings folder: {e}", "warn")

    def _clear_log(self) -> None:
        self.ui.consoleLog.clear()
        self._emit_log("Log cleared.", "dim")

    def _reset_calibration(self) -> None:
        self.cal_servers = None
        self.cal_tab = None
        self.cal_slot1 = None
        self.cal_slot2 = None
        s = load_settings()
        s["calibration"] = {}
        save_settings(s)
        self._refresh_calibration_label()
        self._emit_log("Calibration reset.", "warn")

    def _apply_always_on_top(self, enabled: bool) -> None:
        """Apply the OS-level topmost flag and sync the pin button's locked state."""
        self._is_pinned = bool(enabled)

        if sys.platform.startswith("win"):
            try:
                user32 = ctypes.windll.user32

                user32.SetWindowPos.argtypes = [
                    ctypes.c_void_p, ctypes.c_void_p,
                    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                    ctypes.c_uint
                ]

                hwnd = ctypes.c_void_p(int(self.winId()))
                HWND_TOPMOST = ctypes.c_void_p(-1)
                HWND_NOTOPMOST = ctypes.c_void_p(-2)

                SWP_NOMOVE = 0x0002
                SWP_NOSIZE = 0x0001
                SWP_NOACTIVATE = 0x0010

                insert_after = HWND_TOPMOST if self._is_pinned else HWND_NOTOPMOST

                user32.SetWindowPos(
                    hwnd,
                    insert_after,
                    0, 0, 0, 0,
                    SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
                )
            except Exception as e:
                print(f"Pin toggle failed: {e}")
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, self._is_pinned)
            self.show()

        if hasattr(self, "pin_btn"):
            self.pin_btn.set_locked(self._is_pinned)

    def _toggle_pin(self) -> None:
        if not hasattr(self, "_is_pinned"):
            self._is_pinned = True

        new_state = not self._is_pinned
        self._apply_always_on_top(new_state)

        # Persist the new pin state so it's restored next launch.
        s = load_settings()
        s["always_on_top"] = new_state
        save_settings(s)

        # Keep the settings page toggle icon in sync if it's been wired up.
        toggle_btn = getattr(self.ui, "always_on_top", None)
        if toggle_btn is not None:
            toggle_btn._is_on = new_state
            toggle_btn.setIcon(QIcon(
                self._ICON_TOGGLE_ON if new_state else self._ICON_TOGGLE_OFF
            ))

    def _shift_content_below_title_bar(self) -> None:
        sw = self.ui.stackedWidget
        sw.move(sw.x(), sw.y() + TITLE_BAR_HEIGHT)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "title_bar"):
            self.title_bar.setGeometry(0, 0, self.width(), TITLE_BAR_HEIGHT)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().y() < TITLE_BAR_HEIGHT:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    # ----- Core UI Helpers -----
    def _init_log_area(self) -> None:
        self.ui.consoleLog.clear()
        log_path = player_log_path()
        if log_path.exists():
            self._emit_log(f"Log path: {log_path}", "dim")
        else:
            self._emit_log(f"WARNING: log not found at {log_path}", "error")
            self._emit_log("Launch SCP:SL at least once.", "warn")

    def _check_dependencies(self) -> None:
        if pyautogui is None:
            self._emit_log("WARNING: pyautogui is not installed.  pip install pyautogui", "error")

    def _register_hotkeys(self) -> None:
        # App-local shortcuts: only fire when SAJ has keyboard focus.
        self._shortcut_start = QShortcut(QKeySequence("S"), self)
        self._shortcut_start.setContext(Qt.WindowShortcut)
        self._shortcut_start.activated.connect(self.on_start_clicked)

        self._shortcut_stop = QShortcut(QKeySequence("Q"), self)
        self._shortcut_stop.setContext(Qt.WindowShortcut)
        self._shortcut_stop.activated.connect(self.on_stop_clicked)

        self._emit_log("Hotkeys registered: S = Start, Q = Stop (SAJ window only).", "dim")

    def _log_to_widget(self, msg: str, tag: str) -> None:
        ts = time.strftime("%H:%M:%S")
        color = {
            "info": COL_INFO,
            "dim": COL_DIM,
            "success": COL_SUCCESS,
            "warn": COL_WARN,
            "error": COL_ERROR,
            "event": COL_EVENT,
        }.get(tag, COL_INFO)

        html = (
            f'<span style="color:{COL_TS};">[{ts}]</span> '
            f'<span style="color:{color};">{self._escape_html(msg)}</span>'
        )
        self.ui.consoleLog.append(html)
        sb = self.ui.consoleLog.verticalScrollBar()
        sb.setValue(sb.maximum())

    @staticmethod
    def _escape_html(s: str) -> str:
        return (
            s.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    def _emit_log(self, msg: str, tag: str = "info") -> None:
        self.signals.log_line.emit(msg, tag)

    def _set_status(self, state: str, override_text: str = "") -> None:
        """Emit a status update. `state` must be a key in STATUS_STATES.

        `override_text` lets the worker show transient strings like
        "CAPTURING SLOT 1 (3)" while keeping the calibrate state's color/icon.
        Pass "" to use the state's default text.
        """
        self.signals.status.emit(state, override_text)

    def _set_status_widget(self, state: str, override_text: str = "") -> None:
        cfg = STATUS_STATES.get(state, STATUS_STATES["idle"])
        text = override_text if override_text else cfg["text"]
        btn = self.ui.status
        btn.setText(text)

        # Load the icon for this state. If the qrc path is wrong the resulting
        # QIcon will be null — log it once per missing path.
        icon = QIcon(cfg["icon"])
        if icon.isNull():
            missing_set = getattr(self, "_warned_missing_icons", set())
            if cfg["icon"] not in missing_set:
                print(f"[status] Icon not found in qrc: {cfg['icon']}")
                missing_set.add(cfg["icon"])
                self._warned_missing_icons = missing_set
            btn.setIcon(QIcon())
        else:
            btn.setIcon(icon)
        btn.setIconSize(QSize(10, 10))

        btn.setStyleSheet(
            "QPushButton {"
            f"  background-color: {cfg['bg']};"
            f"  border: 1px solid {cfg['border']};"
            "  border-radius: 12px;"
            "  padding: 4px 14px;"
            f"  color: {cfg['color']};"
            "  font-size: 12px;"
            "  font-weight: 600;"
            "  letter-spacing: 0.5px;"
            "  text-align: center;"
            "}"
            "QPushButton:hover, QPushButton:pressed, QPushButton:disabled {"
            f"  background-color: {cfg['bg']};"
            f"  border: 1px solid {cfg['border']};"
            f"  color: {cfg['color']};"
            "}"
        )
        # Force a repaint in case the stylesheet recalc doesn't trigger one
        btn.update()

    def _set_calibration_label(self, state: str, override_text: str = "") -> None:
        cfg = CALIBRATION_STATES.get(state, CALIBRATION_STATES["not_set"])
        text = override_text if override_text else cfg["text"]
        btn = self.ui.calibrated
        btn.setText(text)

        # Same icon-swap pattern as the status button
        icon = QIcon(cfg["icon"])
        if icon.isNull():
            missing_set = getattr(self, "_warned_missing_icons", set())
            if cfg["icon"] not in missing_set:
                print(f"[calibrated] Icon not found in qrc: {cfg['icon']}")
                missing_set.add(cfg["icon"])
                self._warned_missing_icons = missing_set
            btn.setIcon(QIcon())
        else:
            btn.setIcon(icon)
        btn.setIconSize(QSize(10, 10))

        btn.setStyleSheet(
            "QPushButton {"
            f"  background-color: {cfg['bg']};"
            f"  border: 1px solid {cfg['border']};"
            "  border-radius: 10px;"
            "  padding: 2px 10px;"
            f"  color: {cfg['color']};"
            "  font-size: 13px;"
            "  font-weight: 500;"
            "  letter-spacing: 0.5px;"
            "  text-align: center;"
            "}"
            "QPushButton:hover, QPushButton:pressed, QPushButton:disabled {"
            f"  background-color: {cfg['bg']};"
            f"  border: 1px solid {cfg['border']};"
            f"  color: {cfg['color']};"
            "}"
        )
        btn.update()

    def _set_current_slot_widget(self, slot: int) -> None:
        if hasattr(self.ui, "current_slot"):
            self.ui.current_slot.setText(str(slot))

    def _set_attempts_widget(self, n: int) -> None:
        if hasattr(self.ui, "attempts"):
            self.ui.attempts.setText(str(n))

    def _refresh_calibration_label(self) -> None:
        if self.cal_servers and self.cal_tab and self.cal_slot1 and self.cal_slot2:
            self._set_calibration_label("set", "")
        else:
            self._set_calibration_label("not_set", "")

    def _set_running_state(self, running: bool) -> None:
        self.ui.start.setEnabled(not running)
        self.ui.stop.setEnabled(running)
        self.ui.calibrate_position.setEnabled(not running)

    def parse_order(self) -> list[int]:
        return self.join_order_editor.get_order()

    def _on_order_changed(self, order: list[int]) -> None:
        """Persist the join order to settings whenever the user edits chips."""
        try:
            s = load_settings()
            s["join_order_list"] = list(order)
            # Keep a legacy string copy too, so older builds can still read it.
            s["order"] = ", ".join(str(n) for n in order)
            save_settings(s)
        except Exception:
            # Don't let a settings write failure break the UI.
            pass

    def parse_interval(self) -> float:
        raw = self.ui.time.text().strip().lower().rstrip("s").strip()
        try:
            v = float(raw)
        except ValueError:
            return 6.0
        return max(1.0, v)

    # ----- Core Application Logic -----
    def on_calibrate_clicked(self) -> None:
        if pyautogui is None:
            self._emit_log("ERROR: pyautogui not installed.", "error")
            return
        if self._cal_thread and self._cal_thread.is_alive():
            return

        def _do():
            try:
                self._emit_log("Initiating calibration sequence...", "event")
                steps = [
                    ("Servers Button",     "SERVERS", "cal_servers"),
                    ("Favorites Tab",      "FAV TAB", "cal_tab"),
                    ("Slot 1 join button", "SLOT 1",  "cal_slot1"),
                    ("Slot 2 join button", "SLOT 2",  "cal_slot2"),
                ]
                for label, short, attr in steps:
                    self.signals.toast.emit(
                        f"Hover over the {label}",
                        "Capturing in 3 seconds",
                        "info",
                    )
                    self._emit_log(f"Hover over {label} — capturing in 3s...", "info")
                    for i in (3, 2, 1):
                        self._set_status("calibrate", f"CAPTURING {short} ({i})")
                        time.sleep(1)
                    pos = pyautogui.position()
                    setattr(self, attr, (pos.x, pos.y))
                    self._emit_log(f"  → {label}: ({pos.x}, {pos.y})", "success")

                cal = Calibration(self.cal_servers,self.cal_tab, self.cal_slot1, self.cal_slot2)
                dx, dy = cal.slot_delta
                if abs(dy) < 5 and abs(dx) < 5:
                    self._emit_log("WARNING: slots 1 and 2 are at nearly the same spot.", "error")
                    self.signals.toast.emit(
                        "Calibration looks off",
                        "Slots 1 and 2 are at nearly the same spot — try again",
                        "warn",
                    )
                else:
                    self._emit_log(f"Delta computed. offset=({dx}, {dy})", "success")
                    s = load_settings()
                    s["calibration"] = {
                        "servers": list(self.cal_servers),
                        "tab": list(self.cal_tab),
                        "slot1": list(self.cal_slot1),
                        "slot2": list(self.cal_slot2),
                    }
                    order = self.parse_order()
                    s["join_order_list"] = list(order)
                    s["order"] = ", ".join(str(n) for n in order)
                    s["interval"] = self.parse_interval()
                    save_settings(s)
                    self.signals.calibration_label.emit("set", "")
                    self.signals.toast.emit(
                        "Calibration complete",
                        f"Slot offset: ({dx}, {dy})",
                        "success",
                    )
                self._set_status("idle", "")
            except Exception as e:
                self._emit_log(f"Calibration error: {e}", "error")
                self.signals.toast.emit(
                    "Calibration failed",
                    str(e) or "An unexpected error occurred",
                    "error",
                )
                self._set_status("idle", "")

        self._cal_thread = threading.Thread(target=_do, daemon=True)
        self._cal_thread.start()

    def on_start_clicked(self) -> None:
        if self._worker and self._worker.is_alive():
            return
        if pyautogui is None:
            self._emit_log("ERROR: pyautogui is required.", "error")
            return
        if not (self.cal_servers and self.cal_tab and self.cal_slot1 and self.cal_slot2):
            self._emit_log("ERROR: calibration required before starting.", "error")
            self.signals.toast.emit(
                "Calibration required",
                "Click Calibrate before starting",
                "warn",
            )
            return

        cal = Calibration(self.cal_servers, self.cal_tab, self.cal_slot1, self.cal_slot2)

        log_path = player_log_path()
        if not log_path.exists():
            self._emit_log(f"ERROR: Player.log not found at {log_path}", "error")
            self.signals.toast.emit(
                "Game log not found",
                "Launch SCP:SL at least once, then try again",
                "error",
            )
            return

        try:
            order = self.parse_order()
        except ValueError as e:
            self._emit_log(f"ERROR: bad join order — {e}", "error")
            self.signals.toast.emit(
                "Invalid join order",
                str(e),
                "warn",
            )
            return
        if not order:
            self._emit_log("ERROR: enter at least one slot number.", "error")
            self.signals.toast.emit(
                "Join order is empty",
                "Add at least one slot number",
                "warn",
            )
            return

        interval = self.parse_interval()

        s = load_settings()
        s["calibration"] = {
            "servers": list(self.cal_servers),
            "tab": list(self.cal_tab),
            "slot1": list(self.cal_slot1),
            "slot2": list(self.cal_slot2),
        }
        s["join_order_list"] = list(order)
        s["order"] = ", ".join(str(n) for n in order)
        s["interval"] = interval
        save_settings(s)

        self._stop_evt.clear()
        # Reset run-scoped UI counters
        self._attempt_count = 0
        self.signals.attempts.emit(0)
        if order:
            self.signals.current_slot.emit(order[0])
        self.signals.set_running.emit(True)
        self._worker = threading.Thread(
            target=self._run, args=(order, cal, interval, log_path), daemon=True
        )
        self._worker.start()

    def on_stop_clicked(self) -> None:
        if not (self._worker and self._worker.is_alive()):
            return
        self._stop_evt.set()
        self.ui.stop.setEnabled(False)

    def _run(
        self,
        order: list[int],
        cal: Calibration,
        interval: float,
        log_path: Path,
    ) -> None:
        ATTEMPT_DETECT_TIMEOUT = max(3.0, interval)
        SILENCE_FAILURE_TIMEOUT = max(6.0, interval)
        ABSOLUTE_TIMEOUT = 90.0

        run_started_at = time.time()
        self._set_status("active", "")
        self._emit_log(f"Sequence started. Iterating slots: {order}", "event")
        self._emit_log(
            f"Pre-attempt timeout {ATTEMPT_DETECT_TIMEOUT:.0f}s, "
            f"silence threshold {SILENCE_FAILURE_TIMEOUT:.0f}s.",
            "dim",
        )

        tail = open_tail(log_path, from_end=True)

        if not CLICK_TAB_EVERY_ATTEMPT:
            try:
                perform_click(*cal.servers_button)
                self._emit_log(f"Clicked Servers at {cal.servers_button}", "dim")
                time.sleep(0.25)
                perform_click(*cal.favorites_tab)
                self._emit_log(f"Clicked Favorites tab at {cal.favorites_tab}", "dim")
                time.sleep(0.5)
            except Exception as e:
                self._emit_log(f"Initial nav clicks failed: {e}", "error")

        idx = 0
        last_attempt_ip: Optional[str] = None
        last_attempt_port: Optional[int] = None
        connected = False
        # Track how many rows the favorites list is currently scrolled down.
        current_offset = 0

        while not self._stop_evt.is_set():
            slot = order[idx]

            # Desired scroll offset: 0 for slots that fit on screen, otherwise
            # enough to bring the slot into the bottom visible row.
            desired_offset = max(0, slot - VISIBLE_SLOTS)
            scroll_delta = desired_offset - current_offset
            join_pos = cal.slot_position(slot - desired_offset)

            self.signals.current_slot.emit(slot)
            self._attempt_count += 1
            self.signals.attempts.emit(self._attempt_count)

            try:
                if CLICK_TAB_EVERY_ATTEMPT:
                    perform_click(*cal.servers_button)
                    time.sleep(0.1)
                    perform_click(*cal.favorites_tab)
                    time.sleep(0.15)
                if scroll_delta != 0:
                    # pyautogui scroll convention: positive = up, negative = down.
                    perform_scroll(*cal.slot1, -scroll_delta)
                    direction = "down" if scroll_delta > 0 else "up"
                    self._emit_log(
                        f"Scrolled {direction} {abs(scroll_delta)} row(s) "
                        f"(offset {current_offset} → {desired_offset}) "
                        f"to reach Slot {slot}.",
                        "dim",
                    )
                    current_offset = desired_offset
                    time.sleep(0.15)
                perform_click(*join_pos)
                self._emit_log(
                    f"Attempting Slot {slot} (attempt #{self._attempt_count})...",
                    "info",
                )
            except Exception as e:
                self._emit_log(f"Click error: {e}", "error")
                break

            click_time = time.time()
            pre_attempt_deadline = click_time + ATTEMPT_DETECT_TIMEOUT
            absolute_deadline = click_time + ABSOLUTE_TIMEOUT
            attempt_started = False
            silence_deadline = 0.0
            outcome = ""
            # OCR polling cadence
            ocr_iter = 0
            ocr_enabled = self.disconnect_detector.available
            ocr_poll_until = 0.0

            while not self._stop_evt.is_set():
                now = time.time()
                if now >= absolute_deadline:
                    outcome = "timeout"
                    break
                if not attempt_started and now >= pre_attempt_deadline:
                    outcome = "failure_silent_pre"
                    break
                if attempt_started and now >= silence_deadline:
                    outcome = "failure_silent_post"
                    break

                # OCR check (fast-fail). Only after attempt_started.
                if (
                    ocr_enabled
                    and attempt_started
                    and now < ocr_poll_until
                    and ocr_iter % 2 == 0
                ):
                    if self.disconnect_detector.check():
                        outcome = "failure_ocr"
                        break
                ocr_iter += 1

                try:
                    new_lines = read_new_lines(tail)
                except Exception as e:
                    self._emit_log(f"Log read error: {e}", "error")
                    new_lines = []

                if new_lines:
                    for line in new_lines:
                        success_hit = any(p.search(line) for p in SUCCESS_PATTERNS)
                        if success_hit:
                            target = (
                                f"{last_attempt_ip}:{last_attempt_port}"
                                if last_attempt_ip and last_attempt_port
                                else "server"
                            )
                            elapsed = time.time() - run_started_at
                            self._emit_log(
                                f"CONNECTED to {target}.  (matched: {line.strip()[:80]})",
                                "success",
                            )
                            self._set_status("connected", "")
                            # Slide-down success toast under the title bar.
                            self.signals.toast.emit(
                                f"Joined in {elapsed:.1f}s",
                                f"Slot {slot} · {self._attempt_count} attempt{'s' if self._attempt_count != 1 else ''}",
                                "success",
                            )
                            outcome = "success"
                            connected = True
                            break

                        m = ATTEMPT_PATTERN.search(line)
                        if m:
                            last_attempt_ip = m.group(1)
                            try:
                                last_attempt_port = int(m.group(2))
                            except ValueError:
                                last_attempt_port = None
                            attempt_started = True
                            silence_deadline = time.time() + SILENCE_FAILURE_TIMEOUT
                            # Start OCR polling for up to 4s.
                            ocr_poll_until = time.time() + 4.0
                            self._emit_log(
                                f"  Game connecting to {last_attempt_ip}:{last_attempt_port}",
                                "dim",
                            )
                            continue

                        m2 = ATTEMPT_FALLBACK.search(line)
                        if m2 and not attempt_started:
                            last_attempt_ip = m2.group(1)
                            attempt_started = True
                            silence_deadline = time.time() + SILENCE_FAILURE_TIMEOUT
                            ocr_poll_until = time.time() + 4.0

                    if outcome:
                        break

                self._stop_evt.wait(0.2)

            if self._stop_evt.is_set():
                break
            if outcome == "success":
                self._stop_evt.set()
                break

            if outcome == "failure_silent_pre":
                self._emit_log(f"Slot {slot}: no connect attempt — click missed.", "warn")
            elif outcome == "failure_silent_post":
                self._emit_log(f"Slot {slot}: no success signal — likely full. Moving on.", "warn")
            elif outcome == "failure_ocr":
                self._emit_log(f"Slot {slot}: disconnect popup detected. Moving on.", "warn")
            else:
                self._emit_log(f"Slot {slot}: absolute timeout. Moving on.", "warn")

            try:
                pyautogui.press("escape")
                time.sleep(0.15)
                pyautogui.press("escape")
            except Exception as e:
                self._emit_log(f"Esc press failed: {e}", "error")
            # Give the game time to fully dismiss the connection dialog.
            self._stop_evt.wait(0.5)

            last_attempt_ip = None
            last_attempt_port = None
            idx = (idx + 1) % len(order)

        if not connected and self._stop_evt.is_set():
            self._set_status("inactive", "STOPPED")
            self._emit_log("Sequence aborted by user.", "warn")
            self.signals.toast.emit(
                "Stopped",
                f"{self._attempt_count} attempt{'s' if self._attempt_count != 1 else ''}",
                "info",
            )

        self.signals.set_running.emit(False)