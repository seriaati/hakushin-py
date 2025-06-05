from __future__ import annotations

from typing import Self

from pydantic import BaseModel, model_validator

from ..utils import cleanup_text, remove_ruby_tags, replace_device_params


class APIModel(BaseModel):
    """Provide base functionality for all Hakushin API data models.

    This class extends Pydantic's BaseModel with automatic text cleanup for
    common fields like name, description, and story. It handles formatting
    by removing ruby tags, cleaning up text, and replacing device parameters.
    """

    @model_validator(mode="after")
    def __format_fields(self) -> Self:
        for field_name, field_value in self.model_dump().items():
            if field_name in {"name", "description", "story"} and isinstance(field_value, str):
                setattr(
                    self,
                    field_name,
                    replace_device_params(remove_ruby_tags(cleanup_text(field_value))),
                )

        return self
