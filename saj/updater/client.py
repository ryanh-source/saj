"""Check GitHub for a newer release and download it.

All network I/O happens on background threads; results flow back through
Qt signals on UpdateSignals so the GUI thread is never blocked.
"""
from __future__ import annotations

import json
import re
import threading
import time
import urllib.error
import urllib.request
from typing import Optional

from PySide6.QtCore import QObject, Signal

from saj import __version__
from saj.constants import GITHUB_LATEST_URL, GITHUB_RELEASES_URL
from saj.core.system import update_download_dir


# ---------------------------------------------------------------------------
# Version helpers
# ---------------------------------------------------------------------------

def parse_version(s: str) -> tuple[int, ...]:
    """Parse 'v1.2.3' / '1.2.3' into a tuple for comparison.

    Falls back to (0,) if no digits are found, so unparseable tags compare
    as 'older than anything'.
    """
    if not s:
        return (0,)
    parts = re.findall(r"\d+", s)
    if not parts:
        return (0,)
    return tuple(int(p) for p in parts)


def is_newer(remote: str, local: str) -> bool:
    """True if remote version > local version."""
    return parse_version(remote) > parse_version(local)


# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------

class UpdateSignals(QObject):
    """Signals emitted by the update checker / downloader threads."""
    state_changed   = Signal(str)         # state key from UPDATE_STATES
    latest_version  = Signal(str)         # e.g. "v1.0.0"
    release_notes   = Signal(str, str)    # (version, body markdown/text)
    last_checked    = Signal(str)         # timestamp
    download_progress = Signal(int)       # 0–100
    download_done   = Signal(str)         # path to downloaded file
    error           = Signal(str)         # error message
    releases_list   = Signal(list)        # list of dicts: [{tag, date, body}, ...]


# ---------------------------------------------------------------------------
# Checker / downloader
# ---------------------------------------------------------------------------

class UpdateChecker(QObject):
    """Manages checking GitHub releases and downloading + installing updates.

    All network I/O happens on background threads; UI updates flow back
    through Qt signals so the GUI thread is never blocked.
    """

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.signals = UpdateSignals()
        self._check_thread: Optional[threading.Thread] = None
        self._download_thread: Optional[threading.Thread] = None
        self._cancel_evt = threading.Event()

        # Populated by a successful check, consumed when the user hits Download.
        self._latest_tag: Optional[str] = None
        self._download_url: Optional[str] = None
        self._download_filename: Optional[str] = None

    # ----- Public API -----
    def check_for_updates(self) -> None:
        """Kick off a background check. Safe to call repeatedly."""
        if self._check_thread and self._check_thread.is_alive():
            return
        self.signals.state_changed.emit("checking")
        self._check_thread = threading.Thread(target=self._do_check, daemon=True)
        self._check_thread.start()

    def fetch_releases(self, limit: int = 10) -> None:
        """Kick off a background fetch of the releases list for the history table."""
        if hasattr(self, "_releases_thread") and self._releases_thread and self._releases_thread.is_alive():
            return
        self._releases_thread = threading.Thread(
            target=self._do_fetch_releases,
            args=(limit,),
            daemon=True,
        )
        self._releases_thread.start()

    def _do_fetch_releases(self, limit: int) -> None:
        try:
            url = f"{GITHUB_RELEASES_URL}?per_page={limit}"
            req = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": f"SAJ/{__version__}",
                },
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            releases = []
            for r in data:
                tag = (r.get("tag_name") or "").strip()
                body = (r.get("body") or "").strip()
                published = r.get("published_at") or r.get("created_at") or ""
                # Drop prereleases/drafts unless you want them visible
                if r.get("draft") or r.get("prerelease"):
                    continue
                releases.append({
                    "tag": tag,
                    "body": body,
                    "published": published,
                    "html_url": r.get("html_url") or "",
                })

            self.signals.releases_list.emit(releases)

        except urllib.error.HTTPError as e:
            print(f"[releases] HTTPError {e.code}")
            self.signals.releases_list.emit([])
        except Exception as e:
            print(f"[releases] failed: {e}")
            self.signals.releases_list.emit([])

    def download_and_install(self) -> None:
        """Download the cached latest release and trigger install on success."""
        if not self._download_url:
            self.signals.error.emit("No download URL — run a check first.")
            return
        if self._download_thread and self._download_thread.is_alive():
            return
        self._cancel_evt.clear()
        self.signals.state_changed.emit("downloading")
        self._download_thread = threading.Thread(target=self._do_download, daemon=True)
        self._download_thread.start()

    def cancel_download(self) -> None:
        """Signal an in-flight download to abort."""
        self._cancel_evt.set()

    # ----- Internals -----
    def _do_check(self) -> None:
        try:
            req = urllib.request.Request(
                GITHUB_LATEST_URL,
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": f"SAJ/{__version__}",
                },
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            tag = (data.get("tag_name") or "").strip()
            body = (data.get("body") or "").strip()
            assets = data.get("assets") or []

            # Pick the first .exe asset; fall back to the first asset of any kind.
            download_url = None
            filename = None
            for a in assets:
                name = a.get("name") or ""
                if name.lower().endswith(".exe"):
                    download_url = a.get("browser_download_url")
                    filename = name
                    break
            if download_url is None and assets:
                download_url = assets[0].get("browser_download_url")
                filename = assets[0].get("name")

            self._latest_tag = tag
            self._download_url = download_url
            self._download_filename = filename

            ts = time.strftime("%b %d, %H:%M")
            self.signals.last_checked.emit(ts)
            self.signals.latest_version.emit(tag or "unknown")
            self.signals.release_notes.emit(tag or "", body)

            if tag and is_newer(tag, __version__):
                self.signals.state_changed.emit("available")
            else:
                self.signals.state_changed.emit("up_to_date")

        except urllib.error.HTTPError as e:
            if e.code == 404:
                self.signals.latest_version.emit(__version__)
                self.signals.release_notes.emit("", "No releases published yet.")
                self.signals.state_changed.emit("up_to_date")
            else:
                self.signals.error.emit(f"GitHub returned HTTP {e.code}.")
                self.signals.state_changed.emit("error")
        except urllib.error.URLError as e:
            self.signals.error.emit(f"Could not reach GitHub: {e.reason}")
            self.signals.state_changed.emit("error")
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            self.signals.error.emit(f"Unexpected response from GitHub: {e}")
            self.signals.state_changed.emit("error")
        except Exception as e:
            self.signals.error.emit(f"Update check failed: {e}")
            self.signals.state_changed.emit("error")

    def _do_download(self) -> None:
        if not self._download_url:
            self.signals.error.emit("No download URL.")
            self.signals.state_changed.emit("error")
            return

        try:
            dest_dir = update_download_dir()
            out_name = self._download_filename or f"saj_{self._latest_tag or 'latest'}.exe"
            out_path = dest_dir / out_name

            req = urllib.request.Request(
                self._download_url,
                headers={"User-Agent": f"SAJ/{__version__}"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                total = int(resp.headers.get("Content-Length") or 0)
                downloaded = 0
                last_pct = -1
                with open(out_path, "wb") as f:
                    while True:
                        if self._cancel_evt.is_set():
                            self.signals.state_changed.emit("available")
                            self.signals.error.emit("Download cancelled.")
                            try:
                                out_path.unlink(missing_ok=True)
                            except OSError:
                                pass
                            return
                        chunk = resp.read(64 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            pct = int(downloaded * 100 / total)
                            if pct != last_pct:
                                last_pct = pct
                                self.signals.download_progress.emit(pct)
                if total <= 0:
                    self.signals.download_progress.emit(100)

            self.signals.state_changed.emit("installing")
            self.signals.download_done.emit(str(out_path))

        except urllib.error.URLError as e:
            self.signals.error.emit(f"Download failed: {e.reason}")
            self.signals.state_changed.emit("error")
        except OSError as e:
            self.signals.error.emit(f"Could not write update file: {e}")
            self.signals.state_changed.emit("error")
        except Exception as e:
            self.signals.error.emit(f"Download failed: {e}")
            self.signals.state_changed.emit("error")