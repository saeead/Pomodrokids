"""Entry point for Pomodoro Kids desktop application."""

from __future__ import annotations

from pathlib import Path

from components.main_window import MainWindow
from services.app_controller import AppController


def main() -> None:
    """Create app controller and launch main window."""

    app_controller = AppController(storage_path=Path("data/app_state.json"))

    window = MainWindow(on_start_clicked=lambda: window.set_status(app_controller.run_demo_session()))
    window.run()


if __name__ == "__main__":
    main()
