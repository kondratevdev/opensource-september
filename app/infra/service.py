from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import final

from pydantic import TypeAdapter

from app.logic.models import ProjectReport


@final
@dataclass(frozen=True, slots=True)
class UtcNow:
    """Provide the current timezone-aware UTC time."""

    def __call__(self) -> datetime:
        """Return the current UTC time."""
        return datetime.now(tz=UTC)


@final
@dataclass(frozen=True, slots=True)
class WriteProjectReport:
    """Write a project report to the output directory."""

    def __call__(
        self,
        report: ProjectReport,
        output_directory: Path,
        file_name: str,
    ) -> None:
        """Write the report as formatted JSON."""
        output_directory.mkdir(parents=True, exist_ok=True)
        report_path = output_directory / file_name
        report_json = (
            TypeAdapter(type(report))
            .dump_json(
                report,
                indent=2,
            )
            .decode()
        )
        report_path.write_text(f'{report_json}\n', encoding='utf-8')
