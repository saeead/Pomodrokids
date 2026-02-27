"""Tests for app controller profile and reward management."""

from data.models import Period
from services.app_controller import AppController


def test_upsert_profile_updates_existing(tmp_path) -> None:
    controller = AppController(storage_path=tmp_path / "state.json")
    profile = controller.list_profiles()[0]
    profile.total_minutes = 90

    controller.upsert_profile(profile)

    updated = [item for item in controller.list_profiles() if item.profile_id == profile.profile_id][0]
    assert updated.total_minutes == 90


def test_run_profile_session_returns_status(tmp_path) -> None:
    controller = AppController(storage_path=tmp_path / "state.json")
    profile = controller.list_profiles()[0]

    message = controller.run_profile_session(profile.profile_id, completed_minutes=profile.total_minutes)

    assert "امتیاز" in message
    assert profile.title in message


def test_get_next_reward_progress_returns_non_negative_remaining(tmp_path) -> None:
    controller = AppController(storage_path=tmp_path / "state.json")

    title, remaining = controller.get_next_reward_progress(Period.WEEKLY)

    assert isinstance(title, str)
    assert remaining >= 0
