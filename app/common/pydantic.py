from pydantic import BaseModel, ConfigDict


class BasePydanticModel(BaseModel):
    """Base configuration shared by GitHub response DTOs."""

    model_config = ConfigDict(
        extra='ignore',
        frozen=True,
        strict=True,
    )
