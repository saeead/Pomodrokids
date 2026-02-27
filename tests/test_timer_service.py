"""Tests for timer behavior and edge cases."""

from data.models import TaskProfile
from services.timer_service import TimerController


class FakeNotificationService:
    """Simple fake notification implementation for tests."""

    def __init__(self) -> None:
        self.popup_calls = []
        self.sound_calls = 0

    def popup(self, title: str, message: str) -> None:
        self.popup_calls.append((title, message))

    def play_sound(self) -> None:
        self.sound_calls += 1


def test_timer_alerts_when_near_end() -> None:
    fake = FakeNotificationService()
    timer = TimerController(fake)
    profile = TaskProfile(
        profile_id="study",
        title="مطالعه",
        total_minutes=60,
        focus_minutes=25,
        break_minutes=5,
        alert_before_end_minutes=10,
    )

    result = timer.run_profile_session(profile, completed_minutes=52)

    assert result.session.completed_minutes == 52
    assert fake.popup_calls
    assert fake.sound_calls == 1


def test_switching_profiles_keeps_profile_identity() -> None:
    fake = FakeNotificationService()
    timer = TimerController(fake)
    study = TaskProfile(profile_id="study", title="مطالعه", total_minutes=40)
    game = TaskProfile(profile_id="game", title="بازی", total_minutes=30)

    first = timer.run_profile_session(study, completed_minutes=20)
    second = timer.run_profile_session(game, completed_minutes=15)

    assert first.session.profile_id == "study"
    assert second.session.profile_id == "game"
