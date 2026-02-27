"""Tests for app controller profile management."""

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
