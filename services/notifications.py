"""Notification adapters for Windows-friendly pop-up and sound alerts."""

from __future__ import annotations

import platform


class NotificationService:
    """Dispatches pop-up and audio notifications.

    This baseline implementation keeps dependencies minimal and provides a
    Windows-first behavior with safe cross-platform fallback for development.
    """

    def popup(self, title: str, message: str) -> None:
        """Show a popup-like message.

        Args:
            title: Notification title.
            message: Body text.
        """

        print(f"[POPUP] {title}: {message}")

    def play_sound(self) -> None:
        """Play a short alert sound where supported."""

        if platform.system().lower() == "windows":
            import winsound

            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            return

        print("[SOUND] beep")
