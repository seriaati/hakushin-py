from __future__ import annotations

from pydantic import Field, computed_field

from ..base import APIModel

__all__ = ("ZZZExtraProp", "ZZZMaterial")


class ZZZMaterial(APIModel):
    """Represent a generic ZZZ material.

    Attributes:
        id: ID of the material.
        amount: Amount of the material.
    """

    id: int
    amount: int


class ZZZExtraProp(APIModel):
    """Represent a generic ZZZ extra property.

    Attributes:
        id: ID of the property.
        name: Name of the property.
        format: Format of the property.
        value: Value of the property.
    """

    id: int = Field(alias="Prop")
    name: str = Field(alias="Name")
    format: str = Field(alias="Format")
    value: int = Field(alias="Value")

    @computed_field
    @property
    def formatted_value(self) -> str:
        """Get the formatted value of this prop."""
        if "%" in self.format:
            return f"{self.value / 100:.0%}%"
        return str(self.value)
