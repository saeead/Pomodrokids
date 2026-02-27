"""Tests for JSON state persistence."""

from datetime import date

from data.models import AppState, Period, RewardRule, ScoreSnapshot, SessionRecord, TaskProfile
from utils.storage import LocalStateRepository


def test_save_and_load_state(tmp_path) -> None:
    repository = LocalStateRepository(tmp_path / "state.json")
    state = AppState(
        profiles=[TaskProfile(profile_id="p1", title="study", total_minutes=30)],
        rewards=[RewardRule(period=Period.WEEKLY, target_score=100, reward_title="gift")],
        scores=ScoreSnapshot(weekly=1, monthly=2, yearly=3),
        sessions=[
            SessionRecord(
                profile_id="p1",
                planned_minutes=30,
                completed_minutes=20,
                completed_focus_blocks=1,
                session_date=date(2026, 1, 1),
            )
        ],
    )

    repository.save(state)
    loaded = repository.load()

    assert loaded.profiles[0].profile_id == "p1"
    assert loaded.rewards[0].period == Period.WEEKLY
    assert loaded.scores.monthly == 2
    assert loaded.sessions[0].session_date.isoformat() == "2026-01-01"
