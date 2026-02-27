"""Main desktop window for Pomodoro Kids MVP."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List

from data.models import TaskProfile


class MainWindow:
    """Tkinter-based shell window with child-friendly controls."""

    def __init__(
        self,
        profiles: List[TaskProfile],
        on_start_clicked: Callable[[str, int], str],
        on_save_profile: Callable[[TaskProfile], None],
    ) -> None:
        """Initialize the main window."""

        self._on_start_clicked = on_start_clicked
        self._on_save_profile = on_save_profile
        self.profile_map: Dict[str, TaskProfile] = {item.title: item for item in profiles}

        self.root = tk.Tk()
        self.root.title("Pomodoro Kids | Minecraft Edition")
        self.root.geometry("820x520")
        self.root.configure(bg="#101c1d")

        self._build_styles()
        self._build_layout()
        self._populate_profiles()

    def _build_styles(self) -> None:
        """Create ttk styles for a game-like visual theme."""

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Card.TFrame", background="#1d2b2f")
        style.configure("Title.TLabel", background="#1d2b2f", foreground="#f4d35e", font=("Segoe UI", 20, "bold"))
        style.configure("Body.TLabel", background="#1d2b2f", foreground="#d9f0ff", font=("Segoe UI", 11))
        style.configure("Accent.TButton", background="#3fb950", foreground="#0a0f14", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Accent.TButton", background=[("active", "#57d46a")])

    def _build_layout(self) -> None:
        """Render the main dashboard-like layout."""

        wrapper = ttk.Frame(self.root, style="Card.TFrame", padding=18)
        wrapper.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        header = ttk.Label(wrapper, text="پومودرو کیدز | ماموریت زمان‌بندی", style="Title.TLabel")
        header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        left = ttk.Frame(wrapper, style="Card.TFrame", padding=12)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        right = ttk.Frame(wrapper, style="Card.TFrame", padding=12)
        right.grid(row=1, column=1, sticky="nsew")

        wrapper.columnconfigure(0, weight=3)
        wrapper.columnconfigure(1, weight=2)
        wrapper.rowconfigure(1, weight=1)

        self._build_profile_editor(left)
        self._build_session_panel(right)

    def _build_profile_editor(self, parent: ttk.Frame) -> None:
        """Create profile section with editable settings."""

        ttk.Label(parent, text="پروفایل وظیفه", style="Body.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(parent, textvariable=self.profile_var, state="readonly")
        self.profile_combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.profile_combo.bind("<<ComboboxSelected>>", lambda _: self._fill_selected_profile())

        self.total_var = tk.IntVar(value=60)
        self.focus_var = tk.IntVar(value=25)
        self.break_var = tk.IntVar(value=5)
        self.alert_var = tk.IntVar(value=10)

        self._add_labeled_spinbox(parent, "زمان کل (دقیقه)", self.total_var, 2)
        self._add_labeled_spinbox(parent, "تمرکز (دقیقه)", self.focus_var, 3)
        self._add_labeled_spinbox(parent, "استراحت (دقیقه)", self.break_var, 4)
        self._add_labeled_spinbox(parent, "یادآور پایان (دقیقه)", self.alert_var, 5)

        ttk.Button(parent, text="ذخیره تنظیمات پروفایل", style="Accent.TButton", command=self._save_current_profile).grid(
            row=6, column=0, sticky="ew", pady=(10, 0)
        )
        parent.columnconfigure(0, weight=1)

    def _build_session_panel(self, parent: ttk.Frame) -> None:
        """Create run session section and score status display."""

        ttk.Label(parent, text="شبیه‌سازی جلسه", style="Body.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))

        ttk.Label(parent, text="میزان انجام‌شده (دقیقه)", style="Body.TLabel").grid(row=1, column=0, sticky="w")
        self.completed_var = tk.IntVar(value=60)
        self.completed_scale = ttk.Scale(parent, from_=5, to=180, orient="horizontal", command=self._on_scale_change)
        self.completed_scale.set(60)
        self.completed_scale.grid(row=2, column=0, sticky="ew", pady=(4, 8))

        self.completed_label = ttk.Label(parent, text="60 دقیقه", style="Body.TLabel")
        self.completed_label.grid(row=3, column=0, sticky="w")

        ttk.Button(parent, text="شروع و ثبت امتیاز", style="Accent.TButton", command=self._run_session).grid(
            row=4, column=0, sticky="ew", pady=(12, 12)
        )

        self.status_var = tk.StringVar(value="آماده اجرا")
        self.status_label = ttk.Label(parent, textvariable=self.status_var, style="Body.TLabel", wraplength=250)
        self.status_label.grid(row=5, column=0, sticky="w")

        parent.columnconfigure(0, weight=1)

    def _add_labeled_spinbox(self, parent: ttk.Frame, label: str, variable: tk.IntVar, row: int) -> None:
        """Render one label + spinbox line."""

        ttk.Label(parent, text=label, style="Body.TLabel").grid(row=row, column=0, sticky="w")
        spin = ttk.Spinbox(parent, from_=1, to=240, textvariable=variable)
        spin.grid(row=row, column=0, sticky="e", pady=(0, 8))

    def _populate_profiles(self) -> None:
        """Populate profile combo options."""

        profile_names = sorted(self.profile_map.keys())
        self.profile_combo["values"] = profile_names
        if profile_names:
            self.profile_combo.current(0)
            self._fill_selected_profile()

    def _fill_selected_profile(self) -> None:
        """Load selected profile values into controls."""

        selected_name = self.profile_var.get()
        profile = self.profile_map.get(selected_name)
        if not profile:
            return

        self.total_var.set(profile.total_minutes)
        self.focus_var.set(profile.focus_minutes)
        self.break_var.set(profile.break_minutes)
        self.alert_var.set(profile.alert_before_end_minutes)
        self.completed_scale.configure(to=max(10, profile.total_minutes))
        self.completed_scale.set(profile.total_minutes)
        self._on_scale_change(str(profile.total_minutes))

    def _save_current_profile(self) -> None:
        """Save UI values into selected profile."""

        selected_name = self.profile_var.get()
        profile = self.profile_map.get(selected_name)
        if not profile:
            self.status_var.set("ابتدا یک پروفایل انتخاب کن")
            return

        updated = TaskProfile(
            profile_id=profile.profile_id,
            title=profile.title,
            total_minutes=self.total_var.get(),
            focus_minutes=self.focus_var.get(),
            break_minutes=self.break_var.get(),
            alert_before_end_minutes=self.alert_var.get(),
            settings=profile.settings,
        )
        self._on_save_profile(updated)
        self.profile_map[updated.title] = updated
        self.completed_scale.configure(to=max(10, updated.total_minutes))
        self.status_var.set(f"تنظیمات پروفایل {updated.title} ذخیره شد")

    def _on_scale_change(self, value: str) -> None:
        """Update completed minutes label from slider."""

        minutes = int(float(value))
        self.completed_var.set(minutes)
        self.completed_label.configure(text=f"{minutes} دقیقه")

    def _run_session(self) -> None:
        """Run selected profile simulation and display status."""

        selected_name = self.profile_var.get()
        profile = self.profile_map.get(selected_name)
        if not profile:
            self.status_var.set("پروفایل معتبر انتخاب نشده")
            return

        message = self._on_start_clicked(profile.profile_id, self.completed_var.get())
        self.status_var.set(message)

    def run(self) -> None:
        """Start tkinter event loop."""

        self.root.mainloop()
