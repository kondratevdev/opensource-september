import os
from typing import Final

import punq

_GITHUB_API_URL: Final = 'https://api.github.com'
_GITHUB_API_VERSION: Final = '2026-03-10'
_GITHUB_HTTP_TIMEOUT: Final = 30.0


def inject_project_report(container: punq.Container) -> None:
    """Register dependencies required to access the GitHub API."""
    import zapros  # noqa: PLC0415

    from app.infra import http, service  # noqa: PLC0415
    from app.logic.usecases import generate_project_report  # noqa: PLC0415

    # Http:
    container.register(
        http.GitHubApiClient,
        instance=zapros.Client(
            handler=zapros.StdNetworkHandler(
                total_timeout=_GITHUB_HTTP_TIMEOUT,
            ),
            base_url=_GITHUB_API_URL,
            default_headers={
                'Accept': 'application/vnd.github+json',
                'User-Agent': 'opensource-september',
                'X-GitHub-Api-Version': _GITHUB_API_VERSION,
                'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}',
            },
        ),
    )
    container.register(http.FindIssuesByLabel)

    # Services:
    container.register(service.UtcNow)
    container.register(service.WriteProjectReport)

    # Usecases:
    container.register(generate_project_report.GenerateProjectReport)


def create_container() -> punq.Container:
    """Creates `punq` container, which can be re-created in tests."""
    container = punq.Container()
    inject_project_report(container)

    return container


_container = create_container()


def resolve[Thing](thing: type[Thing]) -> Thing:
    """Type-safe resolution for `punq`."""
    return _container.resolve(thing)
