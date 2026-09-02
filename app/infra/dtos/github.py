from typing import Literal, final

from pydantic import Field

from app.common.pydantic import BasePydanticModel


@final
class _GitHubUserDto(BasePydanticModel):
    """GitHub user fields used by issue DTOs."""

    login: str
    avatar_url: str


@final
class GitHubIssueDto(BasePydanticModel):
    """Relevant fields of a GitHub Search issue item."""

    node_id: str
    repository_url: str
    html_url: str
    state: Literal['open', 'closed']
    assignees: tuple[_GitHubUserDto, ...]


@final
class GitHubIssueSearchDto(BasePydanticModel):
    """GitHub issue search response."""

    total_count: int
    incomplete_results: bool
    issues: tuple[GitHubIssueDto, ...] = Field(alias='items')
