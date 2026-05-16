"""Install a downloaded update and the 'update ready' overlay/dialog.

The overlay only exists to drive the installer flow, so it lives with the
installer rather than in saj/ui/.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QSize, QTimer, QEvent
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from saj.ui.widgets import IconHoverButton


class UpdateReadyOverlay(QWidget):
    """In-app modal overlay (not a separate window). Parented to the main
    window, fills it, paints a dim backdrop, centers a card with the update
    info. Mirrors the visual pattern of the user's reference image."""

    def __init__(self, downloaded_path: str, parent: QWidget):
        super().__init__(parent)
        self._src = Path(downloaded_path)
        self._closed = False

        # Cover the parent fully, intercept mouse so backdrop clicks land on us.
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("UpdateOverlay")
        self.setStyleSheet(
            "QWidget#UpdateOverlay { background-color: rgba(0, 0, 0, 140); }"
        )
        # Cover the full parent area.
        self.setGeometry(parent.rect())
        # Stay sized to parent if it resizes.
        parent.installEventFilter(self)

        # Try to extract version from the filename
        version_str = ""
        stem = self._src.stem
        for sep in ("_", "-"):
            if sep in stem:
                tail = stem.rsplit(sep, 1)[-1].lstrip("v")
                if tail and all(c in "0123456789." for c in tail):
                    version_str = tail
                    break

        # Outer layout — used only to center the card.
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addStretch(1)

        # The card itself
        card = QFrame(self)
        card.setObjectName("UpdateCard")
        card.setStyleSheet(
            "QFrame#UpdateCard { background-color: #1c1c1e; "
            "border: 1px solid #2c2c2e; border-radius: 14px; }"
        )
        card.setFixedWidth(460)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 18, 22, 18)
        card_layout.setSpacing(13)

        # Header row: title on left, close X on right
        head = QHBoxLayout()
        head.setSpacing(10)
        icon_box = QLabel()
        icon_box.setFixedSize(30, 30)
        icon_box.setAlignment(Qt.AlignCenter)
        # Render the download icon centered in a circular badge.
        dl_pix = QIcon(":/images/images/download-solid.png").pixmap(QSize(16, 16))
        icon_box.setPixmap(dl_pix)
        icon_box.setStyleSheet(
            "background-color: #2a2f4a; border-radius: 15px;"
        )
        head.addWidget(icon_box)
        title = QLabel("Update Downloaded")
        title.setStyleSheet(
            "font-family: 'Manrope'; font-size: 15px; font-weight: 600; "
            "color: #cfd6ff; background: transparent; border: none;"
        )
        head.addWidget(title)
        head.addStretch(1)
        close_x = IconHoverButton(
            icon_normal=":/images/images/x-solid.png",
            icon_hover=":/images/images/x-solid-full.png",
            icon_size=14,
            hover_bg="rgba(239, 68, 68, 100)",
        )
        close_x.setFixedSize(28, 28)
        close_x.clicked.connect(self.close_overlay)
        head.addWidget(close_x)
        card_layout.addLayout(head)

        # Body
        if version_str:
            body_text = (
                f"Version <b style='color:#cfd6ff;'>v{version_str}</b> has been "
                f"saved to your computer. SAJ can't replace its own running "
                f"file on Windows, so close SAJ and run the new file to upgrade."
            )
        else:
            body_text = (
                "The new version has been saved to your computer. SAJ can't "
                "replace its own running file on Windows, so close SAJ and "
                "run the new file to upgrade."
            )
        body = QLabel(body_text)
        body.setWordWrap(True)
        body.setTextFormat(Qt.RichText)
        body.setStyleSheet(
            "font-family: 'Manrope'; font-size: 12px; color: #cccccc; "
            "background: transparent; border: none;"
        )
        card_layout.addWidget(body)

        # File path display
        path_label = QLabel(str(self._src))
        path_label.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 11px; color: #9aa0c0;"
            "background-color: #15151a; border: 1px solid #2c2c2e; "
            "border-radius: 6px; padding: 9px 11px;"
        )
        path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        path_label.setWordWrap(True)
        card_layout.addWidget(path_label)

        # Tip callout
        tip = QLabel(
            "<b style='color:#cfd6ff;'>Tip:</b> Click <i>Open Folder &amp; Close</i>, "
            "then drag the new file over your existing SAJ shortcut to replace it, "
            "or just double-click to launch from the new location."
        )
        tip.setWordWrap(True)
        tip.setTextFormat(Qt.RichText)
        tip.setStyleSheet(
            "font-family: 'Manrope'; font-size: 11px; color: #9aa0c0; "
            "background-color: rgba(107, 127, 255, 0.08); "
            "border-left: 2px solid #3b4470; "
            "padding: 8px 12px;"
        )
        card_layout.addWidget(tip)

        # Buttons (just two, matching the simplified spec)
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addStretch(1)

        open_btn = QPushButton("Open Folder")
        open_btn.setCursor(Qt.PointingHandCursor)
        open_btn.setMinimumHeight(32)
        open_btn.setStyleSheet(
            "QPushButton { font-family: 'Manrope'; background-color: transparent; "
            "color: #aaaaaa; border: 1px solid #2c2c2e; border-radius: 6px; "
            "padding: 6px 14px; font-size: 12px; }"
            "QPushButton:hover { color: #cfd6ff; border-color: #3b4470; }"
        )
        close_btn = QPushButton("Open Folder && Close")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setMinimumHeight(32)
        close_btn.setStyleSheet(
            "QPushButton { font-family: 'Manrope'; background-color: #2a2f4a; "
            "color: #cfd6ff; border: 1px solid #3b4470; border-radius: 6px; "
            "padding: 6px 14px; font-size: 12px; font-weight: 500; }"
            "QPushButton:hover { background-color: #353b6b; }"
        )
        open_btn.clicked.connect(self._open_folder)
        close_btn.clicked.connect(self._open_and_close_app)
        btn_row.addWidget(open_btn)
        btn_row.addWidget(close_btn)
        card_layout.addLayout(btn_row)

        # Center the card horizontally
        card_wrap = QHBoxLayout()
        card_wrap.addStretch(1)
        card_wrap.addWidget(card)
        card_wrap.addStretch(1)
        outer.addLayout(card_wrap)
        outer.addStretch(1)

        self._card = card
        self.raise_()

    # Resize with parent
    def eventFilter(self, obj, event):
        if obj is self.parent() and event.type() == QEvent.Resize:
            self.setGeometry(self.parent().rect())
        return super().eventFilter(obj, event)

    def _open_folder(self):
        try:
            if sys.platform.startswith("win"):
                subprocess.Popen(["explorer", "/select,", str(self._src)])
            else:
                os.startfile(str(self._src.parent))  # type: ignore[attr-defined]
        except (OSError, AttributeError):
            try:
                os.startfile(str(self._src.parent))  # type: ignore[attr-defined]
            except OSError:
                pass

    def _open_and_close_app(self):
        self._open_folder()
        self.close_overlay()
        QTimer.singleShot(300, lambda: QApplication.instance().quit())

    def close_overlay(self):
        if self._closed:
            return
        self._closed = True
        parent = self.parent()
        if parent is not None:
            parent.removeEventFilter(self)
        self.hide()
        self.deleteLater()


def show_update_ready_dialog(downloaded_path: str, parent=None) -> None:
    """Show the in-app overlay. Parent must be the main window for the
    overlay to render above the page content correctly."""
    src = Path(downloaded_path)
    if not src.exists() or parent is None:
        return
    overlay = UpdateReadyOverlay(downloaded_path, parent)
    overlay.show()


def install_update_and_relaunch(downloaded_path: str) -> None:
    """Pattern A entry point: kept for back-compat with existing callers.
    Shows the update-ready modal. No batch script, no file replacement.
    """
    # Find the active main window to parent the dialog to, so it inherits
    # always-on-top etc. and centers on the app instead of the screen.
    parent = None
    app = QApplication.instance()
    if app is not None:
        for w in app.topLevelWidgets():
            if isinstance(w, QMainWindow):
                parent = w
                break
    show_update_ready_dialog(downloaded_path, parent=parent)