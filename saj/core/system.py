"""Filesystem I/O: where SCP:SL and SAJ keep their stuff on disk.

Covers:
- Path helpers for the game's log + favorites file and SAJ's settings/update dirs
- JSON-backed settings load/save
- Favorites-count reader and a QFileSystemWatcher wrapper
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import ctypes
from ctypes import wintypes
from PySide6.QtCore import QObject, Signal, QFileSystemWatcher, QTimer


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

UPDATE_DOWNLOAD_DIR_PRIMARY = (
    Path(os.environ.get("USERPROFILE", "")) / "Documents" / "SAJ"
)
UPDATE_DOWNLOAD_DIR_FALLBACK = (
    Path(os.environ.get("LOCALAPPDATA", "")) / "SAJ"
)


def player_log_path() -> Path:
    base = os.environ.get("USERPROFILE", "")
    return Path(base) / "AppData" / "LocalLow" / "Northwood" / "SCPSL" / "Player.log"


def _appdata_dir() -> Path:
    """Resolve %APPDATA% (Roaming) robustly.

    When SAJ is autostarted from the registry Run key at login, the APPDATA
    environment variable is occasionally not yet populated in the process
    environment. Falling back to "" there produces a *relative* path, so the
    app reads/writes settings in the wrong place (usually the process CWD) and
    calibration appears to reset even though the real file is untouched.
    Reconstruct from USERPROFILE, then fall back to the Windows shell
    known-folder API as a last resort.
    """
    base = os.environ.get("APPDATA", "")
    if base:
        return Path(base)

    profile = os.environ.get("USERPROFILE", "")
    if profile:
        return Path(profile) / "AppData" / "Roaming"

    try:
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        # CSIDL_APPDATA = 0x001a, SHGFP_TYPE_CURRENT = 0
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x001a, None, 0, buf)
        if buf.value:
            return Path(buf.value)
    except Exception:
        pass

    return Path.home() / "AppData" / "Roaming"


def favorites_path() -> Path:
    return _appdata_dir() / "SCP Secret Laboratory" / "favorites.txt"


def settings_path() -> Path:
    return _appdata_dir() / "scpsl_autojoin" / "settings.json"


def update_download_dir() -> Path:
    """Return a writable directory for update downloads, creating it if needed."""
    for candidate in (UPDATE_DOWNLOAD_DIR_PRIMARY, UPDATE_DOWNLOAD_DIR_FALLBACK):
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".write_probe"
            probe.write_text("", encoding="ascii")
            probe.unlink(missing_ok=True)
            return candidate
        except (OSError, ValueError):
            continue
    # Last resort: temp. Should basically never happen.
    fallback = Path(os.environ.get("TEMP", ".")) / "SAJ"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


# ---------------------------------------------------------------------------
# Persistent settings
# ---------------------------------------------------------------------------

def load_settings() -> dict:
    p = settings_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_settings(data: dict) -> None:
    p = settings_path()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Favorites
# ---------------------------------------------------------------------------

def read_favorites_count(default: int = 6) -> int:
    """Count non-empty lines in the SCP:SL favorites.txt.

    Each line is one favorited server, so the line count is the total number
    of favorites slots the user has.
    """
    p = favorites_path()
    try:
        with p.open("r", encoding="utf-8", errors="replace") as f:
            return sum(1 for line in f if line.strip())
    except OSError:
        return default


class FavoritesWatcher(QObject):
    """Watches favorites.txt for changes and emits the new line count."""

    favorites_changed = Signal(int)  # new count

    def __init__(self, parent=None):
        super().__init__(parent)
        self._path = favorites_path()
        self._watcher = QFileSystemWatcher(self)
        self._watcher.fileChanged.connect(self._on_changed)

        if self._path.parent.exists():
            self._watcher.addPath(str(self._path.parent))
        self._watcher.directoryChanged.connect(self._on_changed)
        self._debounce = QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(200)
        self._debounce.timeout.connect(self._fire)
        self._add_file_watch()

    def _add_file_watch(self) -> None:
        if self._path.exists():
            paths = self._watcher.files()
            if str(self._path) not in paths:
                self._watcher.addPath(str(self._path))

    def _on_changed(self, _path: str) -> None:
        # Re-add the watch (some editors replace the file, breaking watches).
        self._add_file_watch()
        self._debounce.start()

    def _fire(self) -> None:
        self.favorites_changed.emit(read_favorites_count(default=0))