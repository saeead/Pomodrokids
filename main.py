"""Entry point for Pomodoro Kids desktop application."""

from __future__ import annotations

from pathlib import Path

from components.main_window import MainWindow
from services.app_controller import AppController


def main() -> None:
    """Create app controller and launch main window."""

    app_controller = AppController(storage_path=Path("data/app_state.json"))
    profiles = app_controller.list_profiles()

    window = MainWindow(
        profiles=profiles,
        on_start_clicked=app_controller.run_profile_session,
        on_save_profile=app_controller.upsert_profile,
        on_get_scores=app_controller.get_scores,
        on_get_next_reward=app_controller.get_next_reward_progress,
    )
    window.run()


if __name__ == "__main__":
    main()
