"""Shared constants: colors, slot counts, GitHub URL, and status/calibration/update state tables."""
from __future__ import annotations


# ---------------------------------------------------------------------------
# Update source
# ---------------------------------------------------------------------------
# (App version lives in saj/__init__.py as __version__)

GITHUB_OWNER = "ryanh-source"
GITHUB_REPO  = "saj"

# GitHub releases API endpoint for the latest release 
GITHUB_LATEST_URL = (
    f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
)

# Github releases API endpoint for all releases
GITHUB_RELEASES_URL = (
    f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases"
)

AUTO_CHECK_DELAY_SECONDS = 0.5


# ---------------------------------------------------------------------------
# Slot / layout constants
# ---------------------------------------------------------------------------

NUM_SLOTS = 6
VISIBLE_SLOTS = 6  # Number of favorite rows visible without scrolling
CLICK_TAB_EVERY_ATTEMPT = False
TITLE_BAR_HEIGHT = 36


# ---------------------------------------------------------------------------
# Log colors
# ---------------------------------------------------------------------------

COL_INFO    = "#c8c8c8"
COL_DIM     = "#6b7280"
COL_SUCCESS = "#22c55e"
COL_WARN    = "#eab308"
COL_ERROR   = "#ef4444"
COL_EVENT   = "#60a5fa"
COL_TS      = "#4b5563"


# ---------------------------------------------------------------------------
# Status / Calibration button states
# ---------------------------------------------------------------------------
# Each state defines:
#   text   : label shown on the button
#   color  : foreground color (text + icon tint via the colored PNG)
#   icon   : qrc path for the colored circle
#   bg     : background fill (rgba string)
#   border : border color (rgba string)

STATUS_STATES: dict[str, dict] = {
    "idle": {
        "text": "IDLE",
        "color": "#9ca3af",
        "icon": ":/images/images/circle-idle.png",
        "bg": "rgba(156, 163, 175, 25)",
        "border": "rgba(156, 163, 175, 80)",
    },
    "active": {
        "text": "ACTIVE",
        "color": "#22c55e",
        "icon": ":/images/images/circle-active.png",
        "bg": "rgba(34, 197, 94, 25)",
        "border": "rgba(34, 197, 94, 80)",
    },
    "inactive": {
        "text": "INACTIVE",
        "color": "#ef4444",
        "icon": ":/images/images/circle-inactive.png",
        "bg": "rgba(239, 68, 68, 25)",
        "border": "rgba(239, 68, 68, 80)",
    },
    "calibrate": {
        "text": "CALIBRATING",
        "color": "#eab308",
        "icon": ":/images/images/circle-calibrate.png",
        "bg": "rgba(234, 179, 8, 25)",
        "border": "rgba(234, 179, 8, 80)",
    },
    "connected": {
        "text": "CONNECTED",
        "color": "#22c55e",
        "icon": ":/images/images/circle-active.png",
        "bg": "rgba(34, 197, 94, 25)",
        "border": "rgba(34, 197, 94, 80)",
    },
}

CALIBRATION_STATES: dict[str, dict] = {
    "not_set": {
        "text": "NOT SET",
        "color": "#ef4444",
        "icon": ":/images/images/circle-inactive.png",
        "bg": "rgba(239, 68, 68, 25)",
        "border": "rgba(239, 68, 68, 80)",
    },
    "set": {
        "text": "CALIBRATED",
        "color": "#22c55e",
        "icon": ":/images/images/circle-active.png",
        "bg": "rgba(34, 197, 94, 25)",
        "border": "rgba(34, 197, 94, 80)",
    },
}


# ---------------------------------------------------------------------------
# Update states (pill styles for the updates page)
# ---------------------------------------------------------------------------
# Mirrors STATUS_STATES / CALIBRATION_STATES so the updates page reuses the
# same visual as the home page.

UPDATE_STATES: dict[str, dict] = {
    "idle": {
        "text": "",
        "color": "#9ca3af",
        "icon": ":/images/images/circle-idle.png",
        "bg": "rgba(156, 163, 175, 25)",
        "border": "rgba(156, 163, 175, 80)",
    },
    "checking": {
        "text": "",
        "color": "#f4b860",
        "icon": ":/images/images/hourglass.png",
        "bg": "rgba(244, 184, 96, 30)",
        "border": "rgba(244, 184, 96, 100)",
    },
    "available": {
        "text": "",
        "color": "#f4b860",
        "icon": ":/images/images/download-amber.png",
        "bg": "rgba(244, 184, 96, 30)",
        "border": "rgba(244, 184, 96, 100)",
    },
    "up_to_date": {
        "text": "",
        "color": "#22c55e",
        "icon": ":/images/images/check-solid.png",
        "bg": "rgba(34, 197, 94, 30)",
        "border": "rgba(34, 197, 94, 100)",
    },
    "downloading": {
        "text": "",
        "color": "#60a5fa",
        "icon": ":/images/images/download-blue.png",
        "bg": "rgba(96, 165, 250, 25)",
        "border": "rgba(96, 165, 250, 80)",
    },
    "installing": {
        "text": "",
        "color": "#60a5fa",
        "icon": ":/images/images/download-blue.png",
        "bg": "rgba(96, 165, 250, 25)",
        "border": "rgba(96, 165, 250, 80)",
    },
    "error": {
        "text": "",
        "color": "#ef4444",
        "icon": ":/images/images/x-solid-full.png",
        "bg": "rgba(239, 68, 68, 25)",
        "border": "rgba(239, 68, 68, 80)",
    },
}