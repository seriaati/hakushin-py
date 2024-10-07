from __future__ import annotations

from pydantic import Field, computed_field

from ..base import APIModel

__all__ = ("ZZZExtraProp", "ZZZMaterial")


class ZZZMaterial(APIModel):
    """Generic ZZZ material."""

    id: int
    amount: int


class ZZZExtraProp(APIModel):
    """Generic ZZZ extra property."""

    id: int = Field(alias="Prop")
    name: str = Field(alias="Name")
    format: str = Field(alias="Format")
    value: int = Field(alias="Value")

    @computed_field
    @property
    def formatted_value(self) -> str:
        """Formatted value of this prop."""
        if "%" in self.format:
            return f"{self.value / 100:.0%}%"
        return str(self.value)
