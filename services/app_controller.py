"""Application controller coordinating UI and core services."""

from __future__ import annotations

from pathlib import Path
from typing import List

from data.models import Period, RewardRule, TaskProfile
from services.notifications import NotificationService
from services.scoring import ScoringService
from services.timer_service import TimerController
from utils.storage import LocalStateRepository


class AppController:
    """High-level controller for managing profiles, sessions and persistence."""

    def __init__(self, storage_path: Path) -> None:
        """Initialize controller and dependencies."""

        self.repository = LocalStateRepository(storage_path=storage_path)
        self.notification_service = NotificationService()
        self.timer_controller = TimerController(self.notification_service)
        self.scoring_service = ScoringService()
        self.state = self.repository.load()
        self._ensure_default_seed_data()

    def list_profiles(self) -> List[TaskProfile]:
        """Return all saved task profiles."""

        return list(self.state.profiles)

    def upsert_profile(self, profile: TaskProfile) -> None:
        """Create or update a task profile by profile_id."""

        for index, existing in enumerate(self.state.profiles):
            if existing.profile_id == profile.profile_id:
                self.state.profiles[index] = profile
                self.repository.save(self.state)
                return

        self.state.profiles.append(profile)
        self.repository.save(self.state)

    def run_profile_session(self, profile_id: str, completed_minutes: int | None = None) -> str:
        """Run one profile session and persist resulting score/session data."""

        profile = self._find_profile(profile_id)
        result = self.timer_controller.run_profile_session(profile, completed_minutes=completed_minutes)
        score_result = self.scoring_service.apply_session(self.state.scores, result.session)

        self.state.scores = score_result.scores
        self.state.sessions.append(result.session)
        self.repository.save(self.state)

        unlocked = self.scoring_service.unlocked_rewards(self.state.scores, self.state.rewards)
        if unlocked:
            rewards_text = "، ".join(item.reward_title for item in unlocked)
            return f"پروفایل {profile.title}: {score_result.awarded_points} امتیاز ثبت شد | جوایز فعال: {rewards_text}"

        return f"پروفایل {profile.title}: {score_result.awarded_points} امتیاز ثبت شد"

    def _find_profile(self, profile_id: str) -> TaskProfile:
        """Find profile by identifier."""

        for profile in self.state.profiles:
            if profile.profile_id == profile_id:
                return profile

        raise ValueError(f"Profile not found: {profile_id}")

    def _ensure_default_seed_data(self) -> None:
        """Create baseline profiles and rewards for first run."""

        dirty = False
        if not self.state.profiles:
            self.state.profiles = [
                TaskProfile(
                    profile_id="study-default",
                    title="مطالعه",
                    total_minutes=60,
                    focus_minutes=25,
                    break_minutes=5,
                    alert_before_end_minutes=10,
                ),
                TaskProfile(
                    profile_id="gaming-default",
                    title="بازی",
                    total_minutes=45,
                    focus_minutes=20,
                    break_minutes=5,
                    alert_before_end_minutes=5,
                ),
                TaskProfile(
                    profile_id="internet-default",
                    title="اینترنت",
                    total_minutes=30,
                    focus_minutes=15,
                    break_minutes=5,
                    alert_before_end_minutes=5,
                ),
            ]
            dirty = True

        if not self.state.rewards:
            self.state.rewards = [
                RewardRule(period=Period.WEEKLY, target_score=300, reward_title="30 دقیقه بازی اضافه"),
                RewardRule(period=Period.MONTHLY, target_score=1500, reward_title="انتخاب فیلم آخر هفته"),
                RewardRule(period=Period.YEARLY, target_score=20000, reward_title="هدیه سالانه ویژه"),
            ]
            dirty = True

        if dirty:
            self.repository.save(self.state)
