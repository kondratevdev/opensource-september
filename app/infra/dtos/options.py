from pathlib import Path
from typing import final

from app.common.pydantic import BasePydanticModel


@final
class GenerateProjectReportOptions(BasePydanticModel):
    """Options for project report generation."""

    output_directory: Path
    file_name: str
    label: str
