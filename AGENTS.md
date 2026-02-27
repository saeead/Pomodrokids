# AGENTS Guidelines for Pomodoro Kids (پومودرو کیدز)

## Introduction
Welcome to the **Pomodoro Kids** project. This software is a dedicated Windows application designed for 12-year-olds to manage study, gaming, and internet time effectively. It features a sophisticated Pomodoro-style timer, task profiling, a gamified scoring system, and parental reward controls. 

As an AI coding agent, your role is to maintain, expand, and optimize this application while strictly adhering to the architectural principles and UI/UX standards defined in this document.

---

## UI/UX Guidelines
The project follows a unique hybrid aesthetic: **Apple Human Interface Guidelines (HIG)** principles applied to a **Gaming/Minecraft-inspired** theme.

### Core Principles
1.  **Glassmorphism & Depth:** Utilize transparency, background blur (Acrylic/Mica effects), and subtle drop shadows to create a sense of layers and depth, consistent with Apple HIG.
2.  **Child-Friendly Interface:** While professional, the UI must feel like a game. Use high-quality icons, vibrant accents (Minecraft Green, Diamond Blue, Gold), and rounded corners (minimum 12px).
3.  **Visual Hierarchy:** Large, readable typography for timers and clear, playful buttons for primary actions (Start, Pause, Switch Profile).
4.  **Feedback:** Every action must provide visual or auditory feedback. Use smooth transitions for opening sub-menus.

### Component Styling
-   **Transparency:** Use semi-transparent backgrounds for panels to show the wallpaper or underlying layers.
-   **Typography:** Use clean, sans-serif fonts (e.g., Segoe UI Variable or San Francisco) but allow for "pixel-style" headers if it fits the Minecraft theme.
-   **References:** Refer to `PySide6-FluentUI-QML` for layout logic and `CustomTkinter` for modern widget styling.

---

## Dev Environment Tips
### Incremental Development & Code Integrity
-   **Strict Rule:** Modify only the requested components or logic.
-   **Preservation:** Never delete, overwrite, or ignore existing features unless explicitly instructed.
-   **Granular Updates:** When updating the UI or a specific function, ensure the rest of the application's logic remains functional. Provide "diffs" or specific file updates to avoid breaking the codebase.

### Software Architecture
-   **OOP Focus:** Every component must be an object. Use classes for Windows, Widgets, and Logic Controllers.
-   **Modular Structure:** Maintain the following organization:
    -   `/assets`: Images, sounds (Minecraft-style clicks), and fonts.
    -   `/components`: Reusable UI elements (Buttons, Timers, Progress Bars).
    -   `/services`: Background logic (Timer threads, Notification handlers).
    -   `/utils`: Helper functions (File I/O for settings, Time formatting).
    -   `/data`: Local storage for profiles and scoring (JSON or SQLite).

---

## Testing Instructions
Before finalizing any task, ensure the following:
1.  **Unit Testing:** Run `pytest` on core logic (e.g., scoring math, timer calculations).
2.  **UI Verification:** Manually verify that windows are responsive and transparency effects do not hinder readability.
3.  **Notification Test:** Trigger a dummy pop-up and audio alert to ensure system-level integration is working.
4.  **Edge Cases:** Test the timer behavior when the computer goes to sleep or when switching profiles mid-session.

---

## PR Instructions
When submitting or suggesting changes:
-   **Branching:** Use descriptive names like `feature/minecraft-theme` or `fix/timer-logic`.
-   **Commit Messages:** Use clear, concise messages (e.g., "Add: Parent reward configuration panel").
-   **Description:** Briefly explain *what* changed and *why*, specifically noting if any dependencies were added.
-   **Code Review Checklist:** Ensure no existing features are broken and the OOP principles are upheld.

---

## Coding Conventions
-   **Python Standard:** Follow **PEP 8** strictly.
-   **Naming:** 
    -   Classes: `PascalCase` (e.g., `PomodoroTimer`).
    -   Functions/Variables: `snake_case` (e.g., `calculate_score`).
    -   Constants: `UPPER_SNAKE_CASE`.
-   **Documentation:** Every class and public method must have a Docstring explaining its purpose and parameters.
-   **UI Logic Separation:** Keep the UI code (view) separate from the business logic (controller).

---

## Useful Commands Recap

| Command | Description |
| :--- | :--- |
| `pip install -r requirements.txt` | Install necessary dependencies. |
| `python main.py` | Run the main application. |
| `pytest` | Run the test suite. |
| `black .` | Format code to PEP 8 standards. |
| `pyside6-rcc resources.qrc -o resources_rc.py` | Compile Qt resources (if using PySide6). |

---

## Reference Material
For implementation inspiration and library-specific patterns, refer to:
-   [PySide6-FluentUI-QML](https://github.com/zhuzichu520/PySide6-FluentUI-QML) - For advanced UI layouts and transparency.
-   [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - For modern, rounded-corner widget implementations in Python.
-   [Apple HIG - Visual Design](https://developer.apple.com/design/human-interface-guidelines/visual-design) - For depth and vibrancy standards.