from pathlib import Path
from typing import Any

import click

from app.di import resolve
from app.infra.dtos.options import GenerateProjectReportOptions
from app.logic.usecases import GenerateProjectReport


@click.group()
def cli() -> None:
    """Open Source September command-line interface."""


@cli.group()
def generate() -> None:
    """Generate reports for GitHub Pages."""


@generate.command(name='project-report')
@click.option(
    '--output-directory',
    type=click.Path(file_okay=False, path_type=Path),
    required=True,
    help='Directory where the report will be written.',
)
@click.option(
    '--file-name',
    default='project_report.json',
    show_default=True,
    help='Name of the generated report file.',
)
@click.option(
    '--label',
    default='opensource september',
    show_default=True,
    help='GitHub issue label included in the report.',
)
def generate_project_report(**kwargs: Any) -> None:
    """Generate the repository leaderboard report."""
    usecase = resolve(GenerateProjectReport)
    usecase(GenerateProjectReportOptions(**kwargs))


if __name__ == '__main__':
    cli()
