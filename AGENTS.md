# AGENTS Guidelines for Pomodoro Kids (پومودرو کیدز)

## Introduction
Pomodoro Kids (پومودرو کیدز) is a professional-grade Windows desktop application designed to help 12-year-old users manage their study, gaming, and internet time. The application utilizes the Pomodoro technique, breaking tasks into focused blocks and rest periods. It features task profiles (Study, Gaming, etc.), audio-visual notifications, a comprehensive scoring system for discipline, and a parent-controlled reward module. This document serves as the primary instruction set for AI coding agents to ensure consistency in architecture, UI/UX design, and code quality.

## UI/UX Guidelines
The application must blend the sophisticated aesthetic of **Apple's Human Interface Guidelines (HIG)** with a playful, child-friendly **Minecraft/Gaming theme**.

### Core Principles:
*   **Apple HIG Influence**: 
    *   **Transparency & Depth**: Use "Mica" or "Acrylic" effects (glassmorphism) for window backgrounds.
    *   **Corner Radius**: Large, consistent rounded corners (typically 12px to 20px) for all containers and buttons.
    *   **Typography**: Use clean, sans-serif fonts (e.g., Segoe UI Variable or San Francisco) with clear hierarchy.
    *   **Spacing**: Generous white space (padding) to avoid a cluttered look.
*   **Gaming/Minecraft Elements**:
    *   **Iconography**: Use pixel-art inspired icons or high-quality 3D renders similar to game assets for task types (Pickaxe for "Work", Controller for "Game").
    *   **Gamification**: Visual progress bars and XP-style counters for the scoring system.
    *   **Color Palette**: Vibrant but balanced colors. Use "Emerald Green" for success/study, "Redstone Red" for alerts, and "Diamond Blue" for rest periods.
*   **Components**: Use the components from `PySide6-FluentUI-QML` to achieve the transparent, modern Windows look.

## Dev Environment Tips
*   **Python Version**: Use Python 3.10+ for modern type hinting and performance.
*   **Virtual Environment**: Always use a virtual environment (`venv` or `conda`).
*   **GUI Framework**: Primary framework is **PySide6** (Qt for Python). 
*   **Dependency Management**: Use a `requirements.txt` file.
*   **Environment Variables**: Use a `.env` file for any local configurations or paths, ensuring it is ignored by git.
*   **Windows Specifics**: Ensure `pywin32` is utilized if deep Windows integration (like taskbar progress bars or native notifications) is required.

## Testing Instructions
*   **Unit Testing**: Use `pytest` for logic-related functions (scoring calculations, timer logic).
*   **UI Testing**: Perform manual "Monkey Testing" on the UI to ensure window transparency doesn't interfere with readability.
*   **Integration Testing**: Verify that profile settings (JSON/SQLite) correctly persist after application restart.
*   **Notification Test**: Trigger test pop-ups and audio alerts to ensure they don't get blocked by Windows "Focus Assist."
*   **Command**: Run `pytest tests/` before proposing any changes to the core logic.

## PR Instructions
*   **Branching Strategy**: Use feature branches (e.g., `feature/minecraft-theme`, `fix/timer-logic`).
*   **Commit Messages**: Follow Conventional Commits (e.g., `feat: add parent reward panel`, `fix: resolve memory leak in audio player`).
*   **Documentation**: Every PR must update the `README.md` if new features are added.
*   **Review Checklist**:
    *   Does the code follow PEP 8?
    *   Are the UI elements responsive to window resizing?
    *   Is the scoring logic protected against manual tampering?

## Coding Conventions
*   **Styling**: Strictly adhere to **PEP 8**.
*   **Type Hinting**: Mandatory for all function signatures (e.g., `def calculate_score(points: int) -> bool:`).
*   **Modularity**: Keep UI logic (View) separate from Pomodoro logic (Controller) and Data (Model).
*   **Resource Handling**: Use QRC files for managing images, icons, and audio assets in PySide6.
*   **Error Handling**: Use `try-except` blocks for file I/O and sound playback to prevent application crashes.
*   **Comments**: Use Google-style docstrings for all classes and public methods.

## Useful Commands Recap

| Command | Description |
| :--- | :--- |
| `python -m venv venv` | Create a virtual environment |
| `pip install -r requirements.txt` | Install project dependencies |
| `python main.py` | Run the application |
| `pytest` | Run the test suite |
| `pyside6-rcc resources.qrc -o resources_rc.py` | Compile Qt resources |
| `black .` | Auto-format code to PEP 8 |

## Reference Material
The following repositories should be used as structural and aesthetic references:
*   [PySide6-FluentUI-QML](https://github.com/zhuzichu520/PySide6-FluentUI-QML): Primary reference for the Apple-style/Fluent UI implementation in PySide6.
*   [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter): Secondary reference for modern UI components and theme handling.