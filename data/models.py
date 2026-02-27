"""Domain models for profiles, rewards and score tracking."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Dict, List


class Period(str, Enum):
    """Supported reward and score periods."""

    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


@dataclass
class RewardRule:
    """Defines a parent-configured reward for a target period score.

    Attributes:
        period: Period granularity.
        target_score: Required minimum score to unlock reward.
        reward_title: Human-readable reward label.
    """

    period: Period
    target_score: int
    reward_title: str


@dataclass
class TaskProfile:
    """Configurable task profile for activities like study or gaming.

    Attributes:
        profile_id: Unique profile identifier.
        title: Display name.
        total_minutes: Total allocated minutes for each execution.
        focus_minutes: Focus block duration.
        break_minutes: Break block duration.
        alert_before_end_minutes: Remaining-time reminder threshold.
        settings: Profile-specific settings.
    """

    profile_id: str
    title: str
    total_minutes: int
    focus_minutes: int = 25
    break_minutes: int = 5
    alert_before_end_minutes: int = 5
    settings: Dict[str, str] = field(default_factory=dict)


@dataclass
class ScoreSnapshot:
    """Stores cumulative score values by period."""

    weekly: int = 0
    monthly: int = 0
    yearly: int = 0


@dataclass
class SessionRecord:
    """Represents one finished or interrupted profile session."""

    profile_id: str
    planned_minutes: int
    completed_minutes: int
    completed_focus_blocks: int
    session_date: date


@dataclass
class AppState:
    """Persisted application state container."""

    profiles: List[TaskProfile] = field(default_factory=list)
    rewards: List[RewardRule] = field(default_factory=list)
    scores: ScoreSnapshot = field(default_factory=ScoreSnapshot)
    sessions: List[SessionRecord] = field(default_factory=list)
