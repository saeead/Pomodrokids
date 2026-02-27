"""Utility helpers for time formatting and Pomodoro block generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TimeBlock:
    """Represents a study or break block in a Pomodoro schedule.

    Attributes:
        block_type: Type of block, e.g. "focus" or "break".
        duration_minutes: Duration of the block in minutes.
        index: One-based index of the block in the generated sequence.
    """

    block_type: str
    duration_minutes: int
    index: int


class PomodoroBlockPlanner:
    """Create Pomodoro-style time blocks from a total assigned duration."""

    def __init__(self, focus_minutes: int = 25, break_minutes: int = 5) -> None:
        """Initialize planner with focus and break durations.

        Args:
            focus_minutes: Default focus session length.
            break_minutes: Default break session length.
        """

        if focus_minutes <= 0 or break_minutes <= 0:
            raise ValueError("Block durations must be positive")

        self.focus_minutes = focus_minutes
        self.break_minutes = break_minutes

    def build_blocks(self, total_minutes: int) -> List[TimeBlock]:
        """Build an alternating focus/break sequence to fit total time.

        Args:
            total_minutes: Total allocated minutes for the task.

        Returns:
            A list of ordered time blocks.
        """

        if total_minutes <= 0:
            raise ValueError("Total minutes must be positive")

        remaining = total_minutes
        blocks: List[TimeBlock] = []
        index = 1

        while remaining > 0:
            focus_duration = min(self.focus_minutes, remaining)
            blocks.append(TimeBlock("focus", focus_duration, index))
            remaining -= focus_duration
            index += 1

            if remaining <= 0:
                break

            break_duration = min(self.break_minutes, remaining)
            blocks.append(TimeBlock("break", break_duration, index))
            remaining -= break_duration
            index += 1

        return blocks


def format_mm_ss(seconds: int) -> str:
    """Format seconds as MM:SS.

    Args:
        seconds: Time in seconds.

    Returns:
        Formatted string in MM:SS.
    """

    if seconds < 0:
        raise ValueError("Seconds cannot be negative")
    minutes, remainder = divmod(seconds, 60)
    return f"{minutes:02}:{remainder:02}"
