"""Custom Qt widgets used by MainWindow.

Order matters here — Chip uses the module-level _CHIP_MIME_TYPE and the
chip styling constants, and JoinOrderEditor uses Chip + FlowLayout.
"""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import (
    Qt,
    QSize,
    QPoint,
    QRect,
    QRectF,
    QMimeData,
    QPropertyAnimation,
    QEasingCurve,
    Property,
    QEvent,
    Signal,
    QTimer,
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QDrag, QPen, QColor
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QFrame,
)


# ---------------------------------------------------------------------------
# IconHoverButton — swaps icon on hover, optional spin animation
# ---------------------------------------------------------------------------

class IconHoverButton(QPushButton):
    """Button that shows icon_normal by default, icon_hover when hovered.

    Optionally spins the icon on hover when spin_on_hover=True (used for the gear).
    Spin is one full 360 forward on enter, reversed on leave.
    """

    def __init__(
        self,
        icon_normal: str,
        icon_hover: str,
        icon_size: int,
        hover_bg: str,
        parent=None,
        spin_on_hover: bool = False,
    ):
        super().__init__(parent)
        self._icon_normal = QIcon(icon_normal)
        self._icon_hover = QIcon(icon_hover)
        self._icon_size = icon_size
        self._spin_on_hover = spin_on_hover
        self._rotation = 0.0

        # Cache the source pixmaps once so re-rotate from a clean original
        self._pixmap_normal = self._icon_normal.pixmap(QSize(icon_size, icon_size))
        self._pixmap_hover = self._icon_hover.pixmap(QSize(icon_size, icon_size))

        self.setIcon(self._icon_normal)
        self.setIconSize(QSize(icon_size, icon_size))
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                padding: 0;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
                border-radius: 6px;
            }}
            QPushButton:checked {{
                background-color: {hover_bg};
                border-radius: 6px;
            }}
        """)

        if spin_on_hover:
            # One 360° rotation on hover, reversed on leave.
            self._spin_anim = QPropertyAnimation(self, b"rotation")
            self._spin_anim.setDuration(500)
            self._spin_anim.setEasingCurve(QEasingCurve.InOutQuad)

    # rotation property — animatable via QPropertyAnimation
    def _get_rotation(self) -> float:
        return self._rotation

    def _set_rotation(self, value: float) -> None:
        self._rotation = value
        self._refresh_rotated_icon()

    rotation = Property(float, _get_rotation, _set_rotation)

    def _refresh_rotated_icon(self) -> None:
        """Re-render the icon at the current rotation angle.

        Draws the rotated source onto a fixed-size canvas so the icon
        bounding box stays constant at every angle (otherwise Qt scales
        the grown bounding box back down and the icon visually shrinks).
        """
        if not self._spin_on_hover:
            return
        hovered = self.underMouse() or getattr(self, "_locked_hover", False)
        src = self._pixmap_hover if hovered else self._pixmap_normal
        if src.isNull():
            return
        if self._rotation % 360 == 0:
            self.setIcon(QIcon(src))
            return

        size = self._icon_size
        canvas = QPixmap(size, size)
        canvas.fill(Qt.transparent)

        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.Antialiasing)
        # Rotate around the canvas center
        painter.translate(size / 2, size / 2)
        painter.rotate(self._rotation)
        painter.translate(-size / 2, -size / 2)
        painter.drawPixmap(0, 0, src)
        painter.end()

        self.setIcon(QIcon(canvas))

    def enterEvent(self, event):
        if self._spin_on_hover:
            self._spin_anim.stop()
            self._spin_anim.setStartValue(self._rotation)
            self._spin_anim.setEndValue(360.0)
            self._spin_anim.start()
        else:
            self.setIcon(self._icon_hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._spin_on_hover:
            self._spin_anim.stop()
            self._spin_anim.setStartValue(self._rotation)
            self._spin_anim.setEndValue(0.0)
            self._spin_anim.start()
        elif not getattr(self, "_locked_hover", False):
            self.setIcon(self._icon_normal)
        super().leaveEvent(event)

    def set_locked(self, locked: bool) -> None:
        """Force the hover icon AND background to stay shown.

        Used for nav buttons (active page) and the pin button (when pinned).
        The first call to set_locked makes the button checkable, so its background
        can be styled via the :checked pseudo-state.
        """
        self._locked_hover = locked
        if not self.isCheckable():
            self.setCheckable(True)
        # Block signals so toggling checked doesn't emit clicked()
        was_blocked = self.blockSignals(True)
        self.setChecked(locked)
        self.blockSignals(was_blocked)

        if self._spin_on_hover:
            self._refresh_rotated_icon()
        else:
            self.setIcon(self._icon_hover if locked else self._icon_normal)


# ---------------------------------------------------------------------------
# FlowLayout — wrap-on-overflow horizontal layout
# ---------------------------------------------------------------------------

class FlowLayout(QLayout):
    """Wrap-on-overflow horizontal layout. Adapted from the standard Qt
    flow layout example (the canonical way to do this in Qt). Lays children
    left-to-right and wraps to a new row when they don't fit."""

    def __init__(self, parent=None, margin=0, hspacing=6, vspacing=6):
        super().__init__(parent)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self._hspace = hspacing
        self._vspace = vspacing
        self._items: list = []

    def __del__(self):
        while self.count():
            self.takeAt(0)

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        return self._hspace

    def verticalSpacing(self):
        return self._vspace

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        m = self.contentsMargins()
        size += QSize(m.left() + m.right(), m.top() + m.bottom())
        return size

    def _do_layout(self, rect, test_only):
        m = self.contentsMargins()
        effective = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        x = effective.x()
        y = effective.y()
        line_height = 0
        for item in self._items:
            wid = item.widget()
            space_x = self._hspace
            space_y = self._vspace
            if wid is not None:
                # respect per-widget spacing if needed (not used here)
                pass
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > effective.right() and line_height > 0:
                x = effective.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = next_x
            line_height = max(line_height, item.sizeHint().height())
        return y + line_height - rect.y() + m.bottom()


# ---------------------------------------------------------------------------
# Chip styling constants
# ---------------------------------------------------------------------------
# Kept here (module-level) so the colors stay consistent and easy to tweak.
# Colors mirror the existing app palette.

_CHIP_BG_SELECTED = "#2a2f4a"
_CHIP_BORDER_SELECTED = "#3b4470"
_CHIP_TEXT_SELECTED = "#cfd6ff"
_CHIP_BG_AVAILABLE = "#0f0f12"
_CHIP_BORDER_AVAILABLE = "#2c2c2e"
_CHIP_TEXT_AVAILABLE = "#999999"

_CHIP_MIME_TYPE = "application/x-saj-slot"


# ---------------------------------------------------------------------------
# Chip — single slot pill
# ---------------------------------------------------------------------------

class Chip(QPushButton):
    """A single slot pill. In 'selected' mode it has a grip + number + X and
    is draggable; in 'available' mode it's a flat clickable badge."""

    removed = Signal(int)        # slot number
    add_requested = Signal(int)  # slot number (from available pool)

    def __init__(self, slot: int, mode: str = "selected", parent=None):
        super().__init__(parent)
        self.slot = slot
        self.mode = mode  # "selected" or "available"
        self._press_pos: Optional[QPoint] = None
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self._refresh_label_and_style()
        if mode == "selected":
            # Click on the pill body does nothing; the X label triggers remove.
            # Connect to mouseReleaseEvent below to detect X-region clicks.
            self.setMouseTracking(True)
        else:
            self.clicked.connect(lambda: self.add_requested.emit(self.slot))

    def _refresh_label_and_style(self) -> None:
        if self.mode == "selected":
            # Two visible glyphs: ⠿ for grip, × for remove. Using unicode
            # avoids a dependency on additional icon resources.
            self.setText(f" ⠿ {self.slot} ✕")
            self.setStyleSheet(
                f"QPushButton {{"
                f"  background-color: {_CHIP_BG_SELECTED};"
                f"  color: {_CHIP_TEXT_SELECTED};"
                f"  border: 1px solid {_CHIP_BORDER_SELECTED};"
                f"  border-radius: 5px;"
                f"  padding: 2px 6px;"
                f"  font-size: 11px;"
                f"  font-weight: 500;"
                f"  text-align: center;"
                f"}}"
            )
            self.setMinimumHeight(24)
        else:
            self.setText(f" {self.slot} ")
            self.setStyleSheet(
                f"QPushButton {{"
                f"  background-color: {_CHIP_BG_AVAILABLE};"
                f"  color: {_CHIP_TEXT_AVAILABLE};"
                f"  border: 1px solid {_CHIP_BORDER_AVAILABLE};"
                f"  border-radius: 5px;"
                f"  padding: 2px 5px;"
                f"  font-size: 11px;"
                f"}}"
                f"QPushButton:hover {{"
                f"  color: {_CHIP_TEXT_SELECTED};"
                f"  border-color: {_CHIP_BORDER_SELECTED};"
                f"}}"
            )
            self.setMinimumHeight(22)
        # Let the button shrink to its text
        self.adjustSize()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    # Drag start — only for selected chips
    def mousePressEvent(self, event):
        if self.mode == "selected" and event.button() == Qt.LeftButton:
            self._press_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode != "selected" or self._press_pos is None:
            return super().mouseMoveEvent(event)
        if (event.buttons() & Qt.LeftButton) and (
            (event.position().toPoint() - self._press_pos).manhattanLength()
            > QApplication.startDragDistance()
        ):
            mime = QMimeData()
            mime.setData(_CHIP_MIME_TYPE, str(self.slot).encode("utf-8"))
            drag = QDrag(self)
            drag.setMimeData(mime)
            # Render the chip itself as the drag pixmap so the cursor visibly
            # carries the pill being moved.
            pix = QPixmap(self.size())
            pix.fill(Qt.transparent)
            self.render(pix)
            drag.setPixmap(pix)
            drag.setHotSpot(event.position().toPoint())
            self._press_pos = None
            drag.exec(Qt.MoveAction)
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Detect a click in the right ~25% of the chip (the X region) to
        # trigger remove. Anywhere else is treated as a no-op (drag handles
        # reordering already).
        if self.mode == "selected" and event.button() == Qt.LeftButton:
            x = event.position().x()
            if x > self.width() * 0.72:
                self.removed.emit(self.slot)
                event.accept()
                return
        super().mouseReleaseEvent(event)


# ---------------------------------------------------------------------------
# JoinOrderEditor — chip-based join order picker
# ---------------------------------------------------------------------------
# Replaces the old comma-separated QLineEdit with a draggable chip widget:
# selected slots show as pills (drag to reorder, click X to remove); unused
# slots sit in an "Available" pool below (click to add to the end of the
# order). Auto-detects the favorite count from favorites.txt and refreshes
# when the file changes on disk.

class JoinOrderEditor(QWidget):
    """Drop-in replacement for the comma-separated join order text field.

    Mounts inside any parent QFrame and fills it. Exposes:
      get_order() -> list[int]      — current order, top-left first
      set_order(list[int])          — restore from settings
      set_favorites_count(int)      — rebuild chips when file count changes
      order_changed                  — Signal(list[int]) fires on any edit
    """

    order_changed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._favorites_count: int = 0
        self._order: list[int] = []
        # Track the chip currently being dragged to compute the
        # insertion index from cursor x-position during dragMoveEvent.
        self._drop_indicator_index: int = -1

        self.setAcceptDrops(True)
        # Belt and suspenders: clear any inherited border/background on the
        # editor itself and its inner widgets.
        self.setObjectName("JoinOrderEditor")
        self.setStyleSheet(
            "QWidget#JoinOrderEditor { background: transparent; border: none; }"
            "QWidget#JoinOrderEditor QWidget { background: transparent; border: none; }"
            "QWidget#JoinOrderEditor QLabel { background: transparent; border: none; }"
        )
        outer = QVBoxLayout(self)
        outer.setContentsMargins(4, 2, 4, 2)
        outer.setSpacing(2)

        # Selected row container
        self._selected_container = QWidget(self)
        self._selected_container.setObjectName("ChipSelectedRow")
        self._selected_layout = FlowLayout(self._selected_container, margin=0, hspacing=4, vspacing=3)
        outer.addWidget(self._selected_container)

        # Toggle row: shows count + expand/collapse button for the pool
        toggle_row = QHBoxLayout()
        toggle_row.setContentsMargins(0, 2, 0, 0)
        self._summary_label = QLabel("")
        self._summary_label.setStyleSheet(
            "color: #6b7280; font-size: 10px; background: transparent; border: none;"
        )
        self._toggle_btn = QPushButton("Show available ▾")
        self._toggle_btn.setCursor(Qt.PointingHandCursor)
        self._toggle_btn.setFocusPolicy(Qt.NoFocus)
        self._toggle_btn.setStyleSheet(
            "QPushButton {"
            "  background: transparent; color: #6b7fff; border: none;"
            "  font-size: 10px; padding: 2px 4px;"
            "}"
            "QPushButton:hover { color: #cfd6ff; }"
        )
        self._toggle_btn.clicked.connect(self._toggle_pool)
        toggle_row.addWidget(self._summary_label)
        toggle_row.addStretch(1)
        toggle_row.addWidget(self._toggle_btn)
        outer.addLayout(toggle_row)

        self._pool_popup = QWidget(None, Qt.Popup | Qt.FramelessWindowHint)
        self._pool_popup.setObjectName("PoolPopup")
        self._pool_popup.setStyleSheet(
            "QWidget#PoolPopup {"
            "  background-color: #15151a;"
            "  border: 1px solid #3b4470;"
            "  border-radius: 8px;"
            "}"
        )
        pool_outer = QVBoxLayout(self._pool_popup)
        pool_outer.setContentsMargins(10, 10, 10, 10)
        pool_outer.setSpacing(6)
        self._pool_header = QLabel("AVAILABLE — click to add")
        self._pool_header.setStyleSheet(
            "color: #888; font-size: 10px; background: transparent; border: none;"
        )
        pool_outer.addWidget(self._pool_header)
        self._pool_inner = QWidget(self._pool_popup)
        self._pool_inner.setStyleSheet("background: transparent; border: none;")
        self._pool_layout = FlowLayout(self._pool_inner, margin=0, hspacing=5, vspacing=4)
        pool_outer.addWidget(self._pool_inner)
        self._pool_popup.hide()
        # If the user dismisses the popup by clicking outside (Qt.Popup
        # auto-closes on outside click), make sure the toggle label resets.
        self._pool_popup.installEventFilter(self)

        # Initial population
        self._refresh_chips()

    # ----- public API -----
    def set_favorites_count(self, n: int) -> None:
        if n == self._favorites_count:
            return
        self._favorites_count = max(0, n)
        # Drop any selected slots that no longer exist
        self._order = [s for s in self._order if 1 <= s <= self._favorites_count]
        # If nothing selected (first load or count just went up from 0), seed
        # with everything in natural order.
        if not self._order and self._favorites_count > 0:
            self._order = list(range(1, self._favorites_count + 1))
        self._refresh_chips()
        self.order_changed.emit(list(self._order))

    def get_order(self) -> list[int]:
        return list(self._order)

    def set_order(self, order: list[int]) -> None:
        # Filter to slots that currently exist
        cleaned = [s for s in order if isinstance(s, int) and 1 <= s <= self._favorites_count]
        # De-dupe while preserving order
        seen = set()
        deduped = []
        for s in cleaned:
            if s not in seen:
                seen.add(s)
                deduped.append(s)
        self._order = deduped
        self._refresh_chips()

    # ----- internal -----
    def eventFilter(self, obj, event):
        # Reset the toggle label when the popup is hidden via outside click
        # (Qt.Popup auto-dismisses but doesn't tell us through a signal).
        if obj is self._pool_popup and event.type() == QEvent.Hide:
            self._toggle_btn.setText("Show available ▾")
        return super().eventFilter(obj, event)

    def _toggle_pool(self) -> None:
        if self._pool_popup.isVisible():
            self._pool_popup.hide()
            self._toggle_btn.setText("Show available ▾")
        else:
            # Top-level popup uses global screen coordinates. Position it
            # right below the editor, matching its width. Let the popup size
            # its own height to fit the chips.
            global_pos = self.mapToGlobal(QPoint(0, self.height() + 2))
            self._pool_popup.setMinimumWidth(self.width())
            self._pool_popup.adjustSize()
            self._pool_popup.move(global_pos)
            self._pool_popup.show()
            self._pool_popup.raise_()
            self._toggle_btn.setText("Hide available ▴")

    def _clear_layout(self, layout: FlowLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def _refresh_chips(self) -> None:
        self._clear_layout(self._selected_layout)
        self._clear_layout(self._pool_layout)

        if self._favorites_count == 0:
            # Show a placeholder so the user knows the editor is alive but
            # the favorites file is empty/missing.
            placeholder = QLabel("No favorites detected — add servers in SCP:SL first")
            placeholder.setStyleSheet(
                "color: #6b7280; font-size: 11px; background: transparent; "
                "border: none; padding: 4px;"
            )
            self._selected_layout.addWidget(placeholder)
            self._summary_label.setText("Waiting for favorites.txt…")
            return

        # Selected chips (in current order)
        for slot in self._order:
            chip = Chip(slot, mode="selected", parent=self._selected_container)
            chip.removed.connect(self._on_chip_removed)
            self._selected_layout.addWidget(chip)

        # Available chips (slots not in order, ascending)
        used = set(self._order)
        available = [s for s in range(1, self._favorites_count + 1) if s not in used]
        for slot in available:
            chip = Chip(slot, mode="available", parent=self._pool_inner)
            chip.add_requested.connect(self._on_chip_add)
            self._pool_layout.addWidget(chip)

        # Summary text
        sel = len(self._order)
        total = self._favorites_count
        self._summary_label.setText(
            f"{sel} of {total} selected · drag to reorder · top-left runs first"
        )

        # Reflow popup if it's visible
        if self._pool_popup.isVisible():
            self._pool_popup.adjustSize()

    def _on_chip_removed(self, slot: int) -> None:
        if slot in self._order:
            self._order.remove(slot)
            self._refresh_chips()
            self.order_changed.emit(list(self._order))

    def _on_chip_add(self, slot: int) -> None:
        if slot not in self._order and 1 <= slot <= self._favorites_count:
            self._order.append(slot)
            self._refresh_chips()
            self.order_changed.emit(list(self._order))

    # ----- drag & drop on the selected row -----
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(_CHIP_MIME_TYPE):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat(_CHIP_MIME_TYPE):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not event.mimeData().hasFormat(_CHIP_MIME_TYPE):
            event.ignore()
            return
        try:
            slot = int(bytes(event.mimeData().data(_CHIP_MIME_TYPE)).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            event.ignore()
            return

        drop_pos = self._selected_container.mapFrom(self, event.position().toPoint())
        new_idx = self._compute_insert_index(drop_pos)

        # Remove old position (if it was already in the order)
        if slot in self._order:
            old_idx = self._order.index(slot)
            self._order.pop(old_idx)
            if old_idx < new_idx:
                new_idx -= 1
        # Clamp
        new_idx = max(0, min(new_idx, len(self._order)))
        self._order.insert(new_idx, slot)
        self._refresh_chips()
        self.order_changed.emit(list(self._order))
        event.acceptProposedAction()

    def _compute_insert_index(self, pos: QPoint) -> int:
        """Find the index where a chip dropped at `pos` should be inserted.

        Chips are laid out in rows; pick the chip whose center the cursor
        is closest to and decide left-of vs right-of based on x."""
        n = self._selected_layout.count()
        if n == 0:
            return 0
        # Build a list of (rect, index) for all chip widgets.
        rects = []
        for i in range(n):
            item = self._selected_layout.itemAt(i)
            if item is None:
                continue
            w = item.widget()
            if w is None:
                continue
            rects.append((w.geometry(), i))
        if not rects:
            return 0
        # Find the row whose vertical span contains pos.y; if none, pick the
        # nearest row by y distance.
        same_row = [r for r in rects if r[0].top() <= pos.y() <= r[0].bottom()]
        if not same_row:
            same_row = sorted(rects, key=lambda r: abs(r[0].center().y() - pos.y()))[:1]
            # Treat as: cursor below all rows -> append to end
            row_y = same_row[0][0].center().y()
            if pos.y() > row_y:
                return n
        # Within same_row, find the chip whose x-center the cursor is to the
        # left of. If cursor is to the right of all, append after the last.
        same_row.sort(key=lambda r: r[0].x())
        for rect, idx in same_row:
            if pos.x() < rect.center().x():
                return idx
        return same_row[-1][1] + 1
    
# ---------------------------------------------------------------------------
# Toast — notification under the title bar
# ---------------------------------------------------------------------------

class Toast(QFrame):
    """Slides down from under the title bar, holds, then slides back up.

    Parented to MainWindow. Auto-removes itself after the hold period.
    Click anywhere on it to dismiss immediately.

    """

    # Color presets per kind (text_color, subtitle_color, border, bg, icon_bg, icon_color)
    _KINDS = {
        "success": {
            "text":      "#cfead7",
            "subtitle":  "#7aa388",
            "border":    "rgba(34, 197, 94, 180)",
            "bg":        "#1a1a1a",
            "icon_bg":   "rgba(34, 197, 94, 45)",
            "icon_color": "#22c55e",
            "icon_path": ":/images/images/check-solid.png",
            "icon_glyph": "",
        },
        "info": {
            "text":      "#c8c8c8",
            "subtitle":  "#7a7a82",
            "border":    "rgba(96, 165, 250, 180)",
            "bg":        "#1a1a1a",
            "icon_bg":   "rgba(96, 165, 250, 45)",
            "icon_color": "#60a5fa",
            "icon_path": ":/images/images/circle-info-solid.png",
            "icon_glyph": "",
        },
        "warn": {
            "text":      "#e8d8a4",
            "subtitle":  "#a89866",
            "border":    "rgba(234, 179, 8, 180)",
            "bg":        "#1a1a1a",
            "icon_bg":   "rgba(234, 179, 8, 45)",
            "icon_color": "#eab308",
            "icon_path": ":/images/images/triangle-exclamation-solid.png",
            "icon_glyph": "",
        },
        "error": {
            "text":      "#e8c4c4",
            "subtitle":  "#a87878",
            "border":    "rgba(239, 68, 68, 180)",
            "bg":        "#1a1a1a",
            "icon_bg":   "rgba(239, 68, 68, 45)",
            "icon_color": "#ef4444",
            "icon_path": ":/images/images/circle-xmark-solid.png",
            "icon_glyph": "",
        },
    }

    # Class-level reference to the currently-visible toast, so a new one can
    # dismiss its predecessor instead of stacking on top.
    _active: "Optional[Toast]" = None

    def __init__(
        self,
        parent: QWidget,
        title: str,
        subtitle: str = "",
        kind: str = "success",
        duration_ms: int = 3000,
        title_bar_height: int = 36,
    ):
        super().__init__(parent)
        self._duration_ms = duration_ms
        self._title_bar_height = title_bar_height
        self._closed = False

        cfg = self._KINDS.get(kind, self._KINDS["success"])

        self.setObjectName("Toast")
        self.setStyleSheet(
            f"QFrame#Toast {{"
            f"  background-color: {cfg['bg']};"
            f"  border: 1px solid {cfg['border']};"
            f"  border-radius: 8px;"
            f"}}"
        )
        self.setCursor(Qt.PointingHandCursor)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(12, 8, 14, 8)
        outer.setSpacing(10)

        # Icon badge (small circle with the symbol inside)
        icon_label = QLabel()
        icon_label.setFixedSize(30, 30)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(
            f"background-color: {cfg['icon_bg']};"
            f"border-radius: 15px;"
            f"color: {cfg['icon_color']};"
            f"font-size: 14px;"
            f"font-weight: 600;"
        )
        icon = QIcon(cfg["icon_path"])
        pix = icon.pixmap(QSize(32, 32)).scaled(
            18, 18,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        icon_label.setPixmap(pix)
        outer.addWidget(icon_label)

        # Text column
        text_col = QVBoxLayout()
        text_col.setContentsMargins(0, 0, 0, 0)
        text_col.setSpacing(1)

        self._title_label = QLabel(title)
        self._title_label.setStyleSheet(
            f"color: {cfg['text']};"
            f"font-family: 'Manrope';"
            f"font-size: 13px;"
            f"font-weight: 500;"
            f"background: transparent;"
            f"border: none;"
        )
        text_col.addWidget(self._title_label)

        self._subtitle_label = QLabel(subtitle)
        self._subtitle_label.setStyleSheet(
            f"color: {cfg['subtitle']};"
            f"font-family: 'Manrope';"
            f"font-size: 11px;"
            f"background: transparent;"
            f"border: none;"
        )
        self._subtitle_label.setVisible(bool(subtitle))
        text_col.addWidget(self._subtitle_label)

        outer.addLayout(text_col)
        outer.addStretch(1)

        # Size the toast tightly to its content, with a sensible minimum width.
        self.adjustSize()
        min_w = max(280, self.sizeHint().width())
        self.resize(min_w, self.sizeHint().height())

        # Animations: slide down on show, slide up on dismiss.
        self._slide_anim = QPropertyAnimation(self, b"pos")

        # Auto-dismiss timer
        self._hold_timer = QTimer(self)
        self._hold_timer.setSingleShot(True)
        self._hold_timer.timeout.connect(self.dismiss)

    @classmethod
    def show_toast(
        cls,
        parent: QWidget,
        title: str,
        subtitle: str = "",
        kind: str = "success",
        duration_ms: int = 3000,
        title_bar_height: int = 36,
        reduce_motion: bool = False,
    ) -> "Toast":
        """Show a toast on `parent`. Dismisses any currently-visible toast first."""
        # Kill the previous toast if one is still on screen.
        if cls._active is not None and not cls._active._closed:
            cls._active.dismiss(immediate=True)

        toast = cls(parent, title, subtitle, kind, duration_ms, title_bar_height)
        cls._active = toast
        toast._present(reduce_motion=reduce_motion)
        return toast

    def _present(self, reduce_motion: bool = False) -> None:
        """Position offscreen above title bar, slide down into view."""
        parent = self.parent()
        if parent is None:
            return

        # Final resting position: centered horizontally, 6px below title bar.
        final_x = (parent.width() - self.width()) // 2
        final_y = self._title_bar_height + 6
        # Start position: just above the title bar (so it slides out from under it).
        start_y = self._title_bar_height - self.height() - 4

        if reduce_motion:
            # Skip the slide — just fade-in via opacity effect would also work,
            # but a clean snap-in is fine and avoids more state.
            self.move(final_x, final_y)
            self.show()
            self.raise_()
            self._hold_timer.start(self._duration_ms)
            return

        self.move(final_x, start_y)
        self.show()
        self.raise_()

        self._slide_anim.stop()
        self._slide_anim.setDuration(280)
        self._slide_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._slide_anim.setStartValue(QPoint(final_x, start_y))
        self._slide_anim.setEndValue(QPoint(final_x, final_y))
        try:
            self._slide_anim.finished.disconnect()
        except (RuntimeError, TypeError):
            pass
        self._slide_anim.finished.connect(
            lambda: self._hold_timer.start(self._duration_ms)
        )
        self._slide_anim.start()

    def dismiss(self, immediate: bool = False) -> None:
        """Slide back up and remove. `immediate=True` skips the animation."""
        if self._closed:
            return
        self._closed = True
        self._hold_timer.stop()

        if immediate:
            self._finish_dismiss()
            return

        parent = self.parent()
        if parent is None:
            self._finish_dismiss()
            return

        start_pos = self.pos()
        end_y = self._title_bar_height - self.height() - 4

        self._slide_anim.stop()
        self._slide_anim.setDuration(200)
        self._slide_anim.setEasingCurve(QEasingCurve.InCubic)
        self._slide_anim.setStartValue(start_pos)
        self._slide_anim.setEndValue(QPoint(start_pos.x(), end_y))
        try:
            self._slide_anim.finished.disconnect()
        except (RuntimeError, TypeError):
            pass
        self._slide_anim.finished.connect(self._finish_dismiss)
        self._slide_anim.start()

    def _finish_dismiss(self) -> None:
        if Toast._active is self:
            Toast._active = None
        self.hide()
        self.deleteLater()

    # Click anywhere on the toast to dismiss it.
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dismiss()
            event.accept()
            return
        super().mousePressEvent(event)

# ---------------------------------------------------------------------------
# CircularProgressButton — Create circular download around update_status
# ---------------------------------------------------------------------------

class CircularProgressButton(QPushButton):
    """A round QPushButton that can draw a progress arc around its border."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._progress = -1  # 0-100; -1 = inactive (don't draw arc)
        self._arc_color = QColor("#60a5fa")  # blue while downloading
        self._arc_width = 5

    def progress(self) -> int:
        return self._progress

    def set_progress(self, value: int) -> None:
        # -1 means "hide arc entirely"; clamp anything else to 0..100
        self._progress = value if value < 0 else max(0, min(100, value))
        self.update()

    def set_arc_color(self, color: str) -> None:
        self._arc_color = QColor(color)
        self.update()

    def paintEvent(self, event):
        # Let the button draw itself first (background, border, icon).
        super().paintEvent(event)

        if self._progress < 0:
            return  # inactive — don't draw arc

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Inset so the arc sits just outside the button's border-radius.
        inset = self._arc_width / 2 + 1
        rect = QRectF(
            inset, inset,
            self.width() - 2 * inset,
            self.height() - 2 * inset,
        )

        pen = QPen(self._arc_color)
        pen.setWidthF(self._arc_width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        start_angle = 90 * 16
        span_angle = -int(self._progress * 360 / 100) * 16
        painter.drawArc(rect, start_angle, span_angle)
