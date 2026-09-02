from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from app.logic.build_project_report import build_project_report
from app.logic.models import ProjectReport

if TYPE_CHECKING:
    from app.infra.dtos.options import GenerateProjectReportOptions
    from app.infra.http import FindIssuesByLabel
    from app.infra.service import UtcNow, WriteProjectReport


@final
@dataclass(frozen=True, slots=True)
class GenerateProjectReport:
    """Generate the repository leaderboard report."""

    find_issues: FindIssuesByLabel
    write_report: WriteProjectReport
    utc_now: UtcNow

    def __call__(
        self,
        options: GenerateProjectReportOptions,
    ) -> ProjectReport:
        """Build and write a project report."""
        report = build_project_report(
            issues=self.find_issues(options.label),
            label=options.label,
            generated_at=self.utc_now(),
        )
        self.write_report(
            report,
            options.output_directory,
            options.file_name,
        )
        return report
