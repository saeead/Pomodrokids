"""Scoring and reward business logic for discipline tracking."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from data.models import Period, RewardRule, ScoreSnapshot, SessionRecord


@dataclass
class ScoreResult:
    """Result of processing one session into score totals."""

    scores: ScoreSnapshot
    awarded_points: int


class ScoringService:
    """Calculates earned points and resolves reward eligibility."""

    def calculate_points(self, session: SessionRecord) -> int:
        """Calculate points for a completed session.

        Base formula uses completion percentage and focus block consistency.
        """

        if session.planned_minutes <= 0:
            return 0

        completion_ratio = min(session.completed_minutes / session.planned_minutes, 1.0)
        completion_points = int(completion_ratio * 100)
        block_bonus = session.completed_focus_blocks * 2
        return completion_points + block_bonus

    def apply_session(self, scores: ScoreSnapshot, session: SessionRecord) -> ScoreResult:
        """Apply a session into all period aggregates."""

        points = self.calculate_points(session)
        updated = ScoreSnapshot(
            weekly=scores.weekly + points,
            monthly=scores.monthly + points,
            yearly=scores.yearly + points,
        )
        return ScoreResult(scores=updated, awarded_points=points)

    def unlocked_rewards(self, scores: ScoreSnapshot, reward_rules: List[RewardRule]) -> List[RewardRule]:
        """Return rewards that are unlocked by current score levels."""

        unlocked: List[RewardRule] = []
        score_by_period = {
            Period.WEEKLY: scores.weekly,
            Period.MONTHLY: scores.monthly,
            Period.YEARLY: scores.yearly,
        }
        for rule in reward_rules:
            if score_by_period[rule.period] >= rule.target_score:
                unlocked.append(rule)
        return unlocked
