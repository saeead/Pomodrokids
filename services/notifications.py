"""Notification adapters for Windows-friendly pop-up and sound alerts."""

from __future__ import annotations

import ctypes
import platform


class NotificationService:
    """Dispatches pop-up and audio notifications."""

    def popup(self, title: str, message: str) -> None:
        """Show a popup message with Windows API where available."""

        if platform.system().lower() == "windows":
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
            return

        print(f"[POPUP] {title}: {message}")

    def play_sound(self) -> None:
        """Play a short alert sound where supported."""

        if platform.system().lower() == "windows":
            import winsound

            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            return

        print("[SOUND] beep")
