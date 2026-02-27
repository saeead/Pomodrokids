"""Persistence helpers for loading and saving local app state."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any, Dict

from data.models import AppState, Period, RewardRule, ScoreSnapshot, SessionRecord, TaskProfile


class LocalStateRepository:
    """Read and write application state from JSON files."""

    def __init__(self, storage_path: Path) -> None:
        """Initialize repository.

        Args:
            storage_path: Path to JSON file.
        """

        self.storage_path = storage_path

    def load(self) -> AppState:
        """Load application state or return defaults when file does not exist."""

        if not self.storage_path.exists():
            return AppState()

        payload = json.loads(self.storage_path.read_text(encoding="utf-8"))
        profiles = [TaskProfile(**item) for item in payload.get("profiles", [])]
        rewards = [
            RewardRule(
                period=Period(item["period"]),
                target_score=item["target_score"],
                reward_title=item["reward_title"],
            )
            for item in payload.get("rewards", [])
        ]
        scores_data = payload.get("scores", {})
        scores = ScoreSnapshot(
            weekly=scores_data.get("weekly", 0),
            monthly=scores_data.get("monthly", 0),
            yearly=scores_data.get("yearly", 0),
        )
        sessions = [
            SessionRecord(
                profile_id=item["profile_id"],
                planned_minutes=item["planned_minutes"],
                completed_minutes=item["completed_minutes"],
                completed_focus_blocks=item["completed_focus_blocks"],
                session_date=date.fromisoformat(item["session_date"]),
            )
            for item in payload.get("sessions", [])
        ]
        return AppState(profiles=profiles, rewards=rewards, scores=scores, sessions=sessions)

    def save(self, state: AppState) -> None:
        """Persist application state to disk."""

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        serialized = {
            "profiles": [asdict(profile) for profile in state.profiles],
            "rewards": [
                {
                    "period": rule.period.value,
                    "target_score": rule.target_score,
                    "reward_title": rule.reward_title,
                }
                for rule in state.rewards
            ],
            "scores": asdict(state.scores),
            "sessions": [self._serialize_session(item) for item in state.sessions],
        }
        self.storage_path.write_text(
            json.dumps(serialized, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _serialize_session(session: SessionRecord) -> Dict[str, Any]:
        """Convert session records into JSON-safe dictionaries."""

        payload = asdict(session)
        payload["session_date"] = session.session_date.isoformat()
        return payload
