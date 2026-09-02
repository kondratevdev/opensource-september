from dataclasses import dataclass
from typing import Final, final
from urllib.parse import urlsplit

import zapros

from app.infra.dtos.github import GitHubIssueDto, GitHubIssueSearchDto
from app.logic.models import EventIssue, Repository

_PAGE_SIZE: Final = 100


@final
class GitHubApiClient(zapros.Client):
    """Synchronous HTTP client configured for the GitHub API."""


@final
@dataclass(frozen=True, slots=True)
class FindIssuesByLabel:
    """Find and normalize GitHub issues carrying a label."""

    client: GitHubApiClient

    def __call__(self, label: str) -> tuple[EventIssue, ...]:
        """Return all GitHub issues carrying the label."""
        found_issues: list[EventIssue] = []
        page = 1

        while True:
            response = self.client.get(
                '/search/issues',
                params={
                    'page': str(page),
                    'per_page': str(_PAGE_SIZE),
                    'q': f'is:issue label:"{label}"',
                },
            )
            response.raise_for_status()
            search_result = GitHubIssueSearchDto.model_validate_json(
                response.read(),
            )
            found_issues.extend(map(_to_event_issue, search_result.issues))

            if len(search_result.issues) < _PAGE_SIZE:
                break
            page += 1

        return tuple(found_issues)


def _to_event_issue(issue: GitHubIssueDto) -> EventIssue:
    return EventIssue(
        node_id=issue.node_id,
        repository=_repository_from_api_url(issue.repository_url),
        state=issue.state,
        assignees_count=len(issue.assignees),
    )


def _repository_from_api_url(repository_url: str) -> Repository:
    path_parts = urlsplit(repository_url).path.strip('/').split('/')
    owner, repository_name = path_parts[-2:]
    full_name = f'{owner}/{repository_name}'
    return Repository(
        full_name=full_name,
        url=f'https://github.com/{full_name}',
        owner_avatar_url=f'https://github.com/{owner}.png',
    )
