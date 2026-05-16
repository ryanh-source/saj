"""Application entry point and font loading."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from PySide6.QtGui import QFontDatabase
QFontDatabase.addApplicationFont(":/fonts/fonts/Manrope-VariableFont_wght.ttf")

# Suppress Qt platform window warnings
os.environ["QT_LOGGING_RULES"] = "qt.qpa.window=false"

from saj.core.system import load_settings
from saj.ui.main_window import MainWindow


def load_manrope_font() -> None:
    """Register Manrope with Qt's font database for stylesheets.

    Looks for the variable font first, then falls back to scanning
    assets/fonts/Manrope/static/ for individual .ttf files.

    Resolves paths relative to the executable when frozen with PyInstaller
    (via sys._MEIPASS)
    """
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent.parent

    manrope_dir = base / "assets" / "fonts" / "Manrope"
    variable_font = manrope_dir / "Manrope-VariableFont_wght.ttf"

    loaded_any = False

    if variable_font.exists():
        font_id = QFontDatabase.addApplicationFont(str(variable_font))
        if font_id != -1:
            loaded_any = True
        else:
            print(f"[font] Failed to load variable font: {variable_font}")

    # Fallback to static .ttfs
    if not loaded_any:
        static_dir = manrope_dir / "static"
        if static_dir.is_dir():
            for ttf in static_dir.glob("*.ttf"):
                if QFontDatabase.addApplicationFont(str(ttf)) != -1:
                    loaded_any = True

    if not loaded_any:
        print(f"[font] Manrope not found under {manrope_dir} — stylesheets will fall back.")


def run() -> None:
    """Application entry point. Called from main.py."""
    app = QApplication(sys.argv)
    tray_enabled = bool(load_settings().get("tray_enabled", True))
    app.setQuitOnLastWindowClosed(not tray_enabled)
    
    load_manrope_font()
    window = MainWindow()

    start_minimized = "--minimized" in sys.argv[1:] or "--tray" in sys.argv[1:]
    if start_minimized and tray_enabled:
        pass
    else:
        window.show()
    sys.exit(app.exec())