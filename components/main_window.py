"""Main desktop window for Pomodoro Kids MVP."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class MainWindow:
    """Tkinter-based shell window with child-friendly controls."""

    def __init__(self, on_start_clicked: Callable[[], None]) -> None:
        """Initialize the main window.

        Args:
            on_start_clicked: Callback for start action.
        """

        self.root = tk.Tk()
        self.root.title("Pomodoro Kids")
        self.root.geometry("460x280")
        self.root.configure(bg="#1f2937")

        container = ttk.Frame(self.root, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        self.header = ttk.Label(container, text="پومودرو کیدز", font=("Segoe UI", 18, "bold"))
        self.header.pack(pady=10)

        self.description = ttk.Label(
            container,
            text="مدیریت زمان مطالعه، بازی و اینترنت به سبک بازی‌محور",
            font=("Segoe UI", 11),
        )
        self.description.pack(pady=8)

        self.start_button = ttk.Button(container, text="شروع جلسه نمونه", command=on_start_clicked)
        self.start_button.pack(pady=12)

        self.status_var = tk.StringVar(value="آماده اجرا")
        self.status_label = ttk.Label(container, textvariable=self.status_var)
        self.status_label.pack(pady=8)

    def set_status(self, text: str) -> None:
        """Set status message text."""

        self.status_var.set(text)

    def run(self) -> None:
        """Start tkinter event loop."""

        self.root.mainloop()
