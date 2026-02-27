"""Tests for scoring and reward logic."""

from datetime import date

from data.models import Period, RewardRule, ScoreSnapshot, SessionRecord
from services.scoring import ScoringService


def test_apply_session_updates_all_score_periods() -> None:
    service = ScoringService()
    session = SessionRecord(
        profile_id="study",
        planned_minutes=60,
        completed_minutes=60,
        completed_focus_blocks=2,
        session_date=date.today(),
    )

    result = service.apply_session(ScoreSnapshot(weekly=10, monthly=20, yearly=30), session)

    assert result.awarded_points == 104
    assert result.scores.weekly == 114
    assert result.scores.monthly == 124
    assert result.scores.yearly == 134


def test_unlocked_rewards_by_period() -> None:
    service = ScoringService()
    rewards = [
        RewardRule(period=Period.WEEKLY, target_score=100, reward_title="weekly"),
        RewardRule(period=Period.MONTHLY, target_score=500, reward_title="monthly"),
    ]

    unlocked = service.unlocked_rewards(ScoreSnapshot(weekly=120, monthly=300, yearly=1000), rewards)

    assert [item.reward_title for item in unlocked] == ["weekly"]
