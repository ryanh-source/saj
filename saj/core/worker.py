"""Worker -> GUI signals"""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal


class WorkerSignals(QObject):
    log_line = Signal(str, str)
    status = Signal(str, str)
    calibration_label = Signal(str, str)
    set_running = Signal(bool)
    current_slot = Signal(int)
    attempts = Signal(int)
    show_window = Signal()
    toast = Signal(str, str, str)