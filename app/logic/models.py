from dataclasses import dataclass
from datetime import datetime
from typing import Literal, final


@final
@dataclass(frozen=True, slots=True)
class Repository:
    """Repository participating in the event."""

    full_name: str
    url: str
    owner_avatar_url: str


@final
@dataclass(frozen=True, slots=True)
class EventIssue:
    """Issue data required to build a project report."""

    node_id: str
    repository: Repository
    state: Literal['open', 'closed']
    assignees_count: int


@final
@dataclass(frozen=True, slots=True)
class ProjectReportEntry:
    """Aggregated statistics for one repository."""

    repository: Repository
    issues: int
    open_issues: int
    closed_issues: int
    unassigned_issues: int


@final
@dataclass(frozen=True, slots=True)
class ProjectReportTotals:
    """Overall project report statistics."""

    repositories: int
    issues: int
    open_issues: int
    closed_issues: int
    unassigned_issues: int


@final
@dataclass(frozen=True, slots=True)
class ProjectReport:
    """Presentation-independent project leaderboard report."""

    label: str
    generated_at: datetime
    totals: ProjectReportTotals
    projects: tuple[ProjectReportEntry, ...]
