"""Resolve packaged asset paths (dev and frozen)."""

from __future__ import annotations

import sys
from pathlib import Path

import customtkinter as ctk


def resource_path(*parts: str) -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        base = Path(__file__).resolve().parent
    return base.joinpath(*parts)


def apply_window_icon(window: ctk.CTk | ctk.CTkToplevel) -> None:
    ico = resource_path("assets", "icon.ico")
    if not ico.is_file():
        return
    path = str(ico.resolve())

    def _set() -> None:
        try:
            window.iconbitmap(path)
        except Exception:
            pass

    # Defer so the window handle exists on Windows before setting the icon.
    try:
        window.after(10, _set)
    except Exception:
        _set()
