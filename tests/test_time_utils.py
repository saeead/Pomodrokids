"""Tests for time utility module."""

from utils.time_utils import PomodoroBlockPlanner, format_mm_ss


def test_build_blocks_with_remainder() -> None:
    planner = PomodoroBlockPlanner(focus_minutes=25, break_minutes=5)

    blocks = planner.build_blocks(60)

    assert [b.block_type for b in blocks] == ["focus", "break", "focus", "break"]
    assert [b.duration_minutes for b in blocks] == [25, 5, 25, 5]


def test_format_mm_ss() -> None:
    assert format_mm_ss(0) == "00:00"
    assert format_mm_ss(125) == "02:05"
