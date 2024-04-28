from typing import Any, Self

from pydantic import BaseModel, model_validator

from ..utils import cleanup_text


class APIModel(BaseModel):
    """Base class for all models in hakushin-py."""

    @property
    def fields(self) -> dict[str, Any]:
        """Return all fields of the model as a dictionary."""
        schema = self.model_fields
        field_names = schema.keys()
        field_values = {name: getattr(self, name) for name in field_names}
        return field_values

    @model_validator(mode="after")
    def _format_fields(self) -> Self:
        for field_name, field_value in self.fields.items():
            if "icon" in field_name:
                setattr(self, field_name, f"https://api.hakush.in/gi/UI/{field_value}.webp")
            elif field_name in {"name", "description", "story"}:
                setattr(self, field_name, cleanup_text(field_value))

        return self
