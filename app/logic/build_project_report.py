from collections.abc import Iterable
from datetime import datetime
from typing import TypedDict, assert_never, final

from app.logic.models import (
    EventIssue,
    ProjectReport,
    ProjectReportEntry,
    ProjectReportTotals,
    Repository,
)


def build_project_report(
    issues: tuple[EventIssue, ...],
    label: str,
    generated_at: datetime,
) -> ProjectReport:
    """Aggregate normalized issues into a ranked project report."""
    stats_by_repository: dict[str, _ProjectStats] = {}

    for issue in issues:
        repository_name = issue.repository.full_name
        stats = stats_by_repository.get(repository_name)
        if stats is None:
            stats = _new_stats(issue.repository)
            stats_by_repository[repository_name] = stats
        _add_issue(stats, issue)

    projects = _sort_projects(
        _to_entry(stats) for stats in stats_by_repository.values()
    )
    return ProjectReport(
        label=label,
        generated_at=generated_at,
        totals=_calculate_totals(projects),
        projects=projects,
    )


@final
class _ProjectStats(TypedDict):
    """Mutable issue counts for one repository."""

    repository: Repository
    open_issues: int
    closed_issues: int
    unassigned_issues: int


def _sort_projects(
    projects: Iterable[ProjectReportEntry],
) -> tuple[ProjectReportEntry, ...]:
    """Order projects by closed issues, total issues, then repository name."""
    return tuple(
        sorted(
            projects,
            key=lambda project: (
                -project.closed_issues,
                -project.issues,
                project.repository.full_name.casefold(),
            ),
        ),
    )


def _new_stats(repository: Repository) -> _ProjectStats:
    """Create empty issue statistics for a repository."""
    return _ProjectStats(
        repository=repository,
        open_issues=0,
        closed_issues=0,
        unassigned_issues=0,
    )


def _add_issue(stats: _ProjectStats, issue: EventIssue) -> None:
    """Include an issue in mutable repository statistics."""
    if issue.state == 'closed':
        stats['closed_issues'] += 1
    elif issue.state == 'open':
        stats['open_issues'] += 1
        if issue.assignees_count == 0:
            stats['unassigned_issues'] += 1
    else:
        assert_never(issue.state)


def _to_entry(stats: _ProjectStats) -> ProjectReportEntry:
    """Convert mutable repository statistics to a report entry."""
    return ProjectReportEntry(
        repository=stats['repository'],
        issues=stats['open_issues'] + stats['closed_issues'],
        open_issues=stats['open_issues'],
        closed_issues=stats['closed_issues'],
        unassigned_issues=stats['unassigned_issues'],
    )


def _calculate_totals(
    projects: tuple[ProjectReportEntry, ...],
) -> ProjectReportTotals:
    """Calculate totals across all project report entries."""
    return ProjectReportTotals(
        repositories=len(projects),
        issues=sum(project.issues for project in projects),
        open_issues=sum(project.open_issues for project in projects),
        closed_issues=sum(project.closed_issues for project in projects),
        unassigned_issues=sum(
            project.unassigned_issues for project in projects
        ),
    )
