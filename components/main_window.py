"""Main desktop window with Minecraft-inspired dashboard styling."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List, Tuple

from data.models import Period, ScoreSnapshot, TaskProfile
from utils.app_meta import APP_NAME, APP_UI_VERSION


class MainWindow:
    """Tkinter shell window with game-like layout and controls."""

    def __init__(
        self,
        profiles: List[TaskProfile],
        on_start_clicked: Callable[[str, int], str],
        on_save_profile: Callable[[TaskProfile], None],
        on_get_scores: Callable[[], ScoreSnapshot],
        on_get_next_reward: Callable[[Period], Tuple[str, int]],
    ) -> None:
        """Initialize the main window and render dashboard."""

        self._on_start_clicked = on_start_clicked
        self._on_save_profile = on_save_profile
        self._on_get_scores = on_get_scores
        self._on_get_next_reward = on_get_next_reward
        self.profile_map: Dict[str, TaskProfile] = {item.title: item for item in profiles}

        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} | {APP_UI_VERSION}")
        self.root.geometry("1180x700")
        self.root.minsize(1100, 640)
        self.root.configure(bg="#88AEE8")

        self._build_styles()
        self._build_layout()
        self._populate_profiles()
        self._update_scoreboard()

    def _build_styles(self) -> None:
        """Create ttk styles for a Minecraft-like colorful dashboard."""

        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("Wood.TFrame", background="#7A4B25")
        style.configure("Panel.TFrame", background="#2B1C12")
        style.configure("Glass.TFrame", background="#9BB8EA")
        style.configure("MineTitle.TLabel", background="#9BB8EA", foreground="#1B1B1B", font=("Segoe UI", 30, "bold"))
        style.configure("MenuTitle.TLabel", background="#2B1C12", foreground="#F0F0F0", font=("Segoe UI", 14, "bold"))
        style.configure("MenuText.TLabel", background="#2B1C12", foreground="#D7E8FF", font=("Segoe UI", 10))
        style.configure("ScoreTitle.TLabel", background="#0F1B27", foreground="#F0F0F0", font=("Segoe UI", 15, "bold"))
        style.configure("ScoreBody.TLabel", background="#0F1B27", foreground="#8DF3FF", font=("Segoe UI", 14, "bold"))
        style.configure(
            "Start.TButton",
            background="#4AD66D",
            foreground="#101910",
            font=("Segoe UI", 16, "bold"),
            padding=8,
        )
        style.configure(
            "Stop.TButton",
            background="#FF5C5C",
            foreground="#271010",
            font=("Segoe UI", 16, "bold"),
            padding=8,
        )
        style.configure("Save.TButton", background="#55C3FF", foreground="#061622", font=("Segoe UI", 10, "bold"))
        style.map("Start.TButton", background=[("active", "#61E883")])
        style.map("Stop.TButton", background=[("active", "#FF7676")])

    def _build_layout(self) -> None:
        """Render complete dashboard with left menu, center timer, and right scoreboard."""

        root_frame = ttk.Frame(self.root, style="Wood.TFrame", padding=8)
        root_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(root_frame, style="Glass.TFrame", padding=(16, 8))
        header.pack(fill=tk.X)
        ttk.Label(header, text=f"MINE-POMODORO  [{APP_UI_VERSION}]", style="MineTitle.TLabel").pack(side=tk.LEFT)
        ttk.Button(header, text="🔔 Notifications", style="Save.TButton").pack(side=tk.RIGHT)

        body = ttk.Frame(root_frame, style="Glass.TFrame", padding=12)
        body.pack(fill=tk.BOTH, expand=True)

        self.left_panel = ttk.Frame(body, style="Panel.TFrame", padding=12)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.center_panel = ttk.Frame(body, style="Glass.TFrame", padding=8)
        self.center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_panel = ttk.Frame(body, style="Panel.TFrame", padding=12)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        self._build_left_menu()
        self._build_center_timer()
        self._build_right_scoreboard()

    def _build_left_menu(self) -> None:
        """Build left profile/settings menu."""

        ttk.Label(self.left_panel, text="🎮 PLAYER PANEL", style="MenuTitle.TLabel").pack(anchor="w", pady=(0, 10))

        ttk.Label(self.left_panel, text="پروفایل وظیفه", style="MenuText.TLabel").pack(anchor="w")
        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(self.left_panel, textvariable=self.profile_var, state="readonly", width=22)
        self.profile_combo.pack(fill=tk.X, pady=(4, 12))
        self.profile_combo.bind("<<ComboboxSelected>>", lambda _: self._fill_selected_profile())

        self.total_var = tk.IntVar(value=60)
        self.focus_var = tk.IntVar(value=25)
        self.break_var = tk.IntVar(value=5)
        self.alert_var = tk.IntVar(value=10)

        self._add_spin_line("⏱ زمان کل", self.total_var)
        self._add_spin_line("⛏ تمرکز", self.focus_var)
        self._add_spin_line("🛌 استراحت", self.break_var)
        self._add_spin_line("🔔 یادآور", self.alert_var)

        ttk.Button(
            self.left_panel,
            text="💾 ذخیره تنظیمات",
            style="Save.TButton",
            command=self._save_current_profile,
        ).pack(fill=tk.X, pady=(12, 0))

    def _build_center_timer(self) -> None:
        """Build center circular timer zone and actions."""

        self.timer_canvas = tk.Canvas(
            self.center_panel,
            width=520,
            height=460,
            bg="#9BB8EA",
            highlightthickness=0,
        )
        self.timer_canvas.pack(pady=(8, 12))

        self._draw_timer_ring(progress_ratio=0.0, center_text="25:00")

        self.action_frame = ttk.Frame(self.center_panel, style="Glass.TFrame")
        self.action_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(self.action_frame, text="⛏ START", style="Start.TButton", command=self._run_session).pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=(40, 8),
        )
        ttk.Button(self.action_frame, text="🧨 STOP", style="Stop.TButton", command=self._stop_session).pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=(8, 40),
        )

        self.status_var = tk.StringVar(value="آماده اجرای ماموریت")
        ttk.Label(self.center_panel, textvariable=self.status_var, style="MenuText.TLabel").pack()

    def _build_right_scoreboard(self) -> None:
        """Build right scoreboard and reward status card."""

        ttk.Label(self.right_panel, text="🏆 SCOREBOARD", style="ScoreTitle.TLabel").pack(fill=tk.X)

        self.points_var = tk.StringVar(value="0")
        self.weekly_var = tk.StringVar(value="0")
        self.next_reward_var = tk.StringVar(value="-")
        self.remaining_var = tk.StringVar(value="0")

        ttk.Label(self.right_panel, text="Current Points", style="MenuText.TLabel").pack(anchor="w", pady=(14, 0))
        ttk.Label(self.right_panel, textvariable=self.points_var, style="ScoreBody.TLabel").pack(anchor="w")

        ttk.Label(self.right_panel, text="Weekly Score", style="MenuText.TLabel").pack(anchor="w", pady=(14, 0))
        ttk.Label(self.right_panel, textvariable=self.weekly_var, style="ScoreBody.TLabel").pack(anchor="w")

        ttk.Separator(self.right_panel, orient="horizontal").pack(fill=tk.X, pady=12)

        ttk.Label(self.right_panel, text="Next Reward", style="MenuText.TLabel").pack(anchor="w")
        ttk.Label(self.right_panel, textvariable=self.next_reward_var, style="ScoreBody.TLabel", wraplength=220).pack(anchor="w")

        ttk.Label(self.right_panel, text="Points Remaining", style="MenuText.TLabel").pack(anchor="w", pady=(10, 0))
        ttk.Label(self.right_panel, textvariable=self.remaining_var, style="ScoreBody.TLabel").pack(anchor="w")

        ttk.Label(self.right_panel, text="انجام‌شده (دقیقه)", style="MenuText.TLabel").pack(anchor="w", pady=(18, 4))
        self.completed_var = tk.IntVar(value=25)
        self.completed_scale = ttk.Scale(
            self.right_panel,
            from_=5,
            to=120,
            orient="horizontal",
            command=self._on_scale_change,
        )
        self.completed_scale.set(25)
        self.completed_scale.pack(fill=tk.X)

        self.completed_label = ttk.Label(self.right_panel, text="25 دقیقه", style="MenuText.TLabel")
        self.completed_label.pack(anchor="w", pady=(6, 0))

    def _add_spin_line(self, label: str, variable: tk.IntVar) -> None:
        """Add one setting line containing a label and spinbox."""

        line = ttk.Frame(self.left_panel, style="Panel.TFrame")
        line.pack(fill=tk.X, pady=4)
        ttk.Label(line, text=label, style="MenuText.TLabel").pack(side=tk.LEFT)
        ttk.Spinbox(line, from_=1, to=240, textvariable=variable, width=7).pack(side=tk.RIGHT)

    def _draw_timer_ring(self, progress_ratio: float, center_text: str) -> None:
        """Draw segmented circular ring with mission text in center."""

        self.timer_canvas.delete("all")
        cx = 260
        cy = 220
        outer_radius = 175
        inner_radius = 112
        segments = 32

        self.timer_canvas.create_oval(
            cx - outer_radius,
            cy - outer_radius,
            cx + outer_radius,
            cy + outer_radius,
            fill="#121418",
            outline="#060708",
            width=6,
        )

        self.timer_canvas.create_oval(
            cx - inner_radius,
            cy - inner_radius,
            cx + inner_radius,
            cy + inner_radius,
            fill="#232B36",
            outline="#121821",
            width=4,
        )

        lit_segments = int(segments * max(0.0, min(progress_ratio, 1.0)))
        for index in range(segments):
            start = (360 / segments) * index
            extent = (360 / segments) - 3
            color = "#53F06A" if index < lit_segments else "#3F4654"
            self.timer_canvas.create_arc(
                cx - 158,
                cy - 158,
                cx + 158,
                cy + 158,
                start=start,
                extent=extent,
                style=tk.ARC,
                outline=color,
                width=13,
            )

        self.timer_canvas.create_text(cx, cy - 38, text="WORK BLOCK", fill="#7CF084", font=("Segoe UI", 24, "bold"))
        self.timer_canvas.create_text(cx, cy + 4, text=center_text, fill="#F2F6FF", font=("Segoe UI", 52, "bold"))
        self.timer_canvas.create_text(cx, cy + 58, text="Build your focus!", fill="#D7E8FF", font=("Segoe UI", 18, "bold"))

    def _populate_profiles(self) -> None:
        """Populate available profile names into combobox."""

        profile_names = list(self.profile_map.keys())
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
        self.completed_scale.set(profile.focus_minutes)
        self._on_scale_change(str(profile.focus_minutes))

        center_time = f"{profile.focus_minutes:02}:00"
        self._draw_timer_ring(progress_ratio=0.0, center_text=center_time)

    def _save_current_profile(self) -> None:
        """Save profile setting values to persistence layer."""

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
        self.status_var.set(f"تنظیمات {updated.title} ذخیره شد")
        self._fill_selected_profile()

    def _on_scale_change(self, value: str) -> None:
        """Update completed-minutes label while slider changes."""

        minutes = int(float(value))
        self.completed_var.set(minutes)
        self.completed_label.configure(text=f"{minutes} دقیقه")

    def _update_scoreboard(self) -> None:
        """Refresh score and reward information from controller callbacks."""

        scores = self._on_get_scores()
        next_reward_title, remaining = self._on_get_next_reward(Period.WEEKLY)
        self.points_var.set(str(scores.weekly))
        self.weekly_var.set(str(scores.weekly))
        self.next_reward_var.set(next_reward_title)
        self.remaining_var.set(str(remaining))

    def _run_session(self) -> None:
        """Run selected profile and update ring + scoreboard feedback."""

        selected_name = self.profile_var.get()
        profile = self.profile_map.get(selected_name)
        if not profile:
            self.status_var.set("پروفایل معتبر انتخاب نشده")
            return

        completed = self.completed_var.get()
        ratio = completed / max(profile.total_minutes, 1)
        self._draw_timer_ring(progress_ratio=ratio, center_text=f"{max(profile.total_minutes - completed, 0):02}:00")

        message = self._on_start_clicked(profile.profile_id, completed)
        self.status_var.set(message)
        self._update_scoreboard()

    def _stop_session(self) -> None:
        """Stop visual mission state and reset ring to current focus duration."""

        selected_name = self.profile_var.get()
        profile = self.profile_map.get(selected_name)
        center_time = "00:00" if not profile else f"{profile.focus_minutes:02}:00"
        self._draw_timer_ring(progress_ratio=0.0, center_text=center_time)
        self.status_var.set("جلسه متوقف شد")

    def run(self) -> None:
        """Start tkinter event loop."""

        self.root.mainloop()
