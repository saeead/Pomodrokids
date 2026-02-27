"""Core timer controller for task profiles and remaining-time reminders."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from data.models import SessionRecord, TaskProfile
from services.notifications import NotificationService
from utils.time_utils import PomodoroBlockPlanner, TimeBlock


@dataclass
class TimerRunResult:
    """Result of a simulated profile run."""

    session: SessionRecord
    blocks: List[TimeBlock]


class TimerController:
    """Coordinates Pomodoro block planning and session completion tracking."""

    def __init__(self, notification_service: NotificationService) -> None:
        """Initialize timer controller with a notification service."""

        self.notification_service = notification_service

    def run_profile_session(
        self,
        profile: TaskProfile,
        completed_minutes: Optional[int] = None,
    ) -> TimerRunResult:
        """Run (simulate) one profile session.

        Args:
            profile: Target task profile.
            completed_minutes: Completed minutes, defaults to full completion.

        Returns:
            TimerRunResult containing generated blocks and session record.
        """

        planner = PomodoroBlockPlanner(
            focus_minutes=profile.focus_minutes,
            break_minutes=profile.break_minutes,
        )
        blocks = planner.build_blocks(profile.total_minutes)
        completed = profile.total_minutes if completed_minutes is None else completed_minutes
        completed = max(0, min(completed, profile.total_minutes))

        if profile.total_minutes - completed <= profile.alert_before_end_minutes:
            self.notification_service.popup(
                "یادآور پایان وظیفه",
                f"پروفایل {profile.title} نزدیک به پایان است.",
            )
            self.notification_service.play_sound()

        completed_focus_blocks = sum(
            1
            for block in blocks
            if block.block_type == "focus" and self._block_is_completed(block, completed, blocks)
        )
        session = SessionRecord(
            profile_id=profile.profile_id,
            planned_minutes=profile.total_minutes,
            completed_minutes=completed,
            completed_focus_blocks=completed_focus_blocks,
            session_date=date.today(),
        )
        return TimerRunResult(session=session, blocks=blocks)

    @staticmethod
    def _block_is_completed(target: TimeBlock, completed_minutes: int, blocks: List[TimeBlock]) -> bool:
        """Return True if block duration is fully included in completed time."""

        elapsed = 0
        for block in blocks:
            elapsed += block.duration_minutes
            if block.index == target.index:
                return completed_minutes >= elapsed
        return False
