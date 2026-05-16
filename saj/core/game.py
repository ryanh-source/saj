"""Everything for observing and driving the SCP:SL client.

Pipeline: tail the log + watch for the disconnect overlay (detect),
match against patterns (parse), translate slot numbers to screen coords
(calibrate), then click/scroll (act).
"""
from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import pyautogui


# ---------------------------------------------------------------------------
# Log parsing patterns
# ---------------------------------------------------------------------------

SUCCESS_PATTERNS = [
    re.compile(r"\[FROM SERVER\].*authenticated on this server", re.I),
    re.compile(r"Scene Manager: Loaded scene 'Facility'"),
    re.compile(r"SceneLoaded\s+\d+\.\s*Facility", re.I),
    re.compile(r"\[Mirror\] Connection Quality changed from ESTIMATING", re.I),
    re.compile(r"\[DEBUG_MAPGEN\] Sequence of procedural level generation completed", re.I),
    re.compile(r"Noise reducer enabled", re.I),
    re.compile(r"Loading cmd bindings", re.I),
]

ATTEMPT_PATTERN = re.compile(r"Connection IP set to\s+([0-9a-fA-F:.]+),\s*port:\s*(\d+)")
ATTEMPT_FALLBACK = re.compile(r"Connecting to\s+([0-9a-fA-F:.]+)\s*!")


# ---------------------------------------------------------------------------
# Log tail
# ---------------------------------------------------------------------------

@dataclass
class TailState:
    path: Path
    pos: int = 0


def open_tail(path: Path, from_end: bool = True) -> TailState:
    try:
        size = path.stat().st_size
    except OSError:
        size = 0
    return TailState(path=path, pos=size if from_end else 0)


def read_new_lines(state: TailState) -> list[str]:
    try:
        size = state.path.stat().st_size
    except OSError:
        return []
    if size < state.pos:
        state.pos = 0
    if size == state.pos:
        return []
    try:
        with state.path.open("r", encoding="utf-8", errors="replace") as f:
            f.seek(state.pos)
            chunk = f.read()
            state.pos = f.tell()
    except OSError:
        return []
    return chunk.splitlines()


# ---------------------------------------------------------------------------
# Calibration math
# ---------------------------------------------------------------------------

@dataclass
class Calibration:
    servers_button: tuple[int, int]
    favorites_tab: tuple[int, int]
    slot1: tuple[int, int]
    slot2: tuple[int, int]

    @property
    def slot_delta(self) -> tuple[int, int]:
        return (self.slot2[0] - self.slot1[0], self.slot2[1] - self.slot1[1])

    def slot_position(self, n: int) -> tuple[int, int]:
        if n < 1:
            raise ValueError("slot must be >= 1")
        dx, dy = self.slot_delta
        return (self.slot1[0] + (n - 1) * dx, self.slot1[1] + (n - 1) * dy)


# ---------------------------------------------------------------------------
# Mouse input
# ---------------------------------------------------------------------------

def perform_click(x: int, y: int, restore_mouse: bool = True) -> None:
    if pyautogui is None:
        raise RuntimeError("pyautogui is not installed")
    if restore_mouse:
        ox, oy = pyautogui.position()
    pyautogui.click(x, y)
    if restore_mouse:
        time.sleep(0.05)
        pyautogui.moveTo(ox, oy)


def perform_scroll(x: int, y: int, clicks: int, restore_mouse: bool = True) -> None:
    """Move cursor over (x, y) and scroll the wheel by `clicks` ticks.

    Sign convention matches pyautogui: positive = up, negative = down.
    On Windows, pyautogui.scroll() targets the current cursor position, so
    have to move first to ensure the wheel events land in the favorites list.
    Each tick is one row in the SCP:SL favorites list.
    """
    if pyautogui is None:
        raise RuntimeError("pyautogui is not installed")
    if clicks == 0:
        return
    if restore_mouse:
        ox, oy = pyautogui.position()
    pyautogui.moveTo(x, y)
    time.sleep(0.05)
    # Scroll one tick at a time with a small delay so the game registers each
    # row independently — bursts of clicks in a single scroll() call sometimes
    # get coalesced and skip rows.
    step = 1 if clicks > 0 else -1
    for _ in range(abs(clicks)):
        pyautogui.scroll(step)
        time.sleep(0.05)
    if restore_mouse:
        time.sleep(0.05)
        pyautogui.moveTo(ox, oy)


# ---------------------------------------------------------------------------
# Fast-fail OCR detector
# ---------------------------------------------------------------------------
#
# When SCP:SL rejects a connection (server full, kicked, etc.) it shows a
# big centered "DISCONNECTED" overlay. The log doesn't include a rejection
# line, so can't detect failure fast from the log alone but can see
# the overlay on screen. This module screenshots a strip across the vertical
# center of the primary screen and runs Windows' built-in OCR over it.
#
# Detection time: ~250-500ms after the popup appears, vs. ~6s for the
# log-based silence timeout. About 10x faster on the common case.
#
# Falls back silently if winsdk isn't available, the OS doesn't support OCR,
# or any step throws — log-based detection still works.

try:
    import asyncio as _ocr_asyncio
    from winsdk.windows.media.ocr import OcrEngine
    from winsdk.windows.globalization import Language
    from winsdk.windows.graphics.imaging import (
        BitmapDecoder,
        SoftwareBitmap,
        BitmapPixelFormat,
        BitmapAlphaMode,
    )
    from winsdk.windows.storage.streams import (
        DataWriter,
        InMemoryRandomAccessStream,
    )
    _OCR_AVAILABLE = True
except ImportError:
    _OCR_AVAILABLE = False


class DisconnectDetector:
    """Screenshot + OCR helper for detecting SCP:SL's 'DISCONNECTED' overlay."""

    # Tokens treat as a hit. "DISCONNECTED" is the big centered text on
    # every rejection. Other words from the secondary line are bonuses for
    # robustness against OCR misreads of the main word.
    _HIT_TOKENS = ("disconnected", "server is full", "kicked", "rejected")

    # OCR sometimes misreads the stylized "DISCONNECTED" font. Specific
    # observed misreads happened while testing: "serqeri9all", "serqeriga11".
    _FUZZY_TOKENS = ("serqeri", "serger", "seroer", "ser9er")

    def __init__(self, debug: bool = False) -> None:
        self.available = _OCR_AVAILABLE
        self._engine = None
        self._loop = None
        self.debug = debug
        # Last OCR text + region used, for caller-side debug logging.
        self.last_text = ""
        self.last_region = (0, 0, 0, 0)
        self._debug_save_idx = 0
        if self.available:
            try:
                # English engine — works for SCP:SL's English text.
                self._engine = OcrEngine.try_create_from_language(
                    Language("en-US")
                )
                if self._engine is None:
                    self.available = False
                # Reuse one event loop across calls to avoid reinit overhead.
                self._loop = _ocr_asyncio.new_event_loop()
            except Exception:
                self.available = False

    def check(self) -> bool:
        """Take one screenshot, OCR it, return True if a hit token appears.

        Returns False on any error (treat as 'no hit, keep waiting')."""
        if not self.available or self._engine is None or pyautogui is None:
            return False
        try:
            # The 'DISCONNECTED' popup is rendered by the game centered on
            # the FULL screen. The SAJ window sits to the right but doesn't
            # cover the popup. Grab a wide horizontal strip centered on
            # the screen, then trim the right edge 
            screen_w, screen_h = pyautogui.size()
            strip_w = int(screen_w * 0.55)
            # Center horizontally on the screen, then nudge slightly left so
            #don't bleed into SAJ on the right side.
            strip_x = (screen_w - strip_w) // 2 - int(screen_w * 0.05)
            if strip_x < 0:
                strip_x = 0
            strip_h = max(180, int(screen_h * 0.22))
            strip_y = (screen_h // 2) - (strip_h // 2)
            self.last_region = (strip_x, strip_y, strip_w, strip_h)
            img = pyautogui.screenshot(
                region=(strip_x, strip_y, strip_w, strip_h)
            )
  
            if self.debug:
                try:
                    dbg_dir = Path(os.environ.get("TEMP", ".")) / "saj_ocr_debug"
                    dbg_dir.mkdir(exist_ok=True)
                    self._debug_save_idx += 1
                    img.save(dbg_dir / f"ocr_{self._debug_save_idx:03d}.png")
                except Exception:
                    pass
            text = self._loop.run_until_complete(self._ocr_pil(img))
            self.last_text = text or ""
            if not text:
                return False
            low = text.lower()
            if any(tok in low for tok in self._HIT_TOKENS):
                return True
            # Fuzzy fallback: OCR sometimes mangles the stylized
            # "DISCONNECTED" font but produces a consistent garbage string can match on.
            if any(tok in low for tok in self._FUZZY_TOKENS):
                return True
            return False
        except Exception as e:
            self.last_text = f"<error: {e}>"
            return False

    async def _ocr_pil(self, pil_image) -> str:
        """Convert a PIL image to a SoftwareBitmap and run OCR on it."""
        # PIL -> PNG bytes -> InMemoryRandomAccessStream -> BitmapDecoder -> SoftwareBitmap
        buf = BytesIO()
        pil_image.save(buf, format="PNG")
        data = buf.getvalue()

        stream = InMemoryRandomAccessStream()
        writer = DataWriter(stream)
        writer.write_bytes(data)
        await writer.store_async()
        await writer.flush_async()
        writer.detach_stream()
        stream.seek(0)

        decoder = await BitmapDecoder.create_async(stream)
        bitmap = await decoder.get_software_bitmap_async()
        # OCR works best with BGRA8/Premultiplied.
        if (
            bitmap.bitmap_pixel_format != BitmapPixelFormat.BGRA8
            or bitmap.bitmap_alpha_mode != BitmapAlphaMode.PREMULTIPLIED
        ):
            bitmap = SoftwareBitmap.convert(
                bitmap, BitmapPixelFormat.BGRA8, BitmapAlphaMode.PREMULTIPLIED
            )

        result = await self._engine.recognize_async(bitmap)
        return result.text or ""