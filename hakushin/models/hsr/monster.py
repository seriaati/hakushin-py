from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from ...enums import Game, HSRElement
from ...utils import get_asset_url
from ..base import APIModel

__all__ = (
    "ChildMonster",
    "DamageTypeResistance",
    "HSREnemySkill",
    "HSREnemySkillEffect",
    "Monster",
    "MonsterDetail",
    "MonsterDrop",
    "MonsterPhase",
)


class HSREnemySkillEffect(APIModel):
    """Represent an extra effect referenced by an enemy skill.

    Attributes:
        name: The name of the effect.
        desc: The description of the effect.
        params: The parameter values interpolated into the description.
    """

    name: str = Field(default="")
    desc: str = Field(default="")
    params: list[Any] = Field(alias="param", default_factory=list)


class HSREnemySkill(APIModel):
    """Represents an enemy skill's information.

    Attributes:
        id: The id of the skill.
        name: The name of the skill
        desc: The description of what the skill does
        damage_type: The type of damage the skill does (out of the HSRElements or None)
        sp_hit_base: The base amount of energy characters hit by the skill gain.
        extra_effects: Extra effects referenced by the skill, keyed by effect ID.
    """

    id: int
    name: str = Field(alias="skill_name", default="")
    desc: str = Field(alias="skill_desc", default="")
    damage_type: HSRElement | None = Field(alias="damage_type", default=None)
    sp_hit_base: int | None = Field(alias="sp_hit_base", default=None)
    extra_effects: dict[int, HSREnemySkillEffect] = Field(alias="extra", default_factory=dict)

    @field_validator("name", "desc", mode="before")
    @classmethod
    def default_empty_string(cls, value: str | None) -> str:
        return value if isinstance(value, str) else ""

    @field_validator("damage_type", "sp_hit_base", mode="before")
    @classmethod
    def empty_string_to_none(cls: type[HSREnemySkill], v: str | int | None) -> str | int | None:
        if not v:
            return None
        return v


class DamageTypeResistance(APIModel):
    """Represent the damage resistance of an enemy in HSR.

    Attributes:
        element: The element of the resistance.
        value: The value of the resistance.
    """

    element: HSRElement = Field(alias="damage_type")
    value: float


class ChildMonster(APIModel):
    """Represent the specific details of a monster type.

    Attributes:
        id: The ID of this instance of the monster.
        attack_modify_ratio: Multiplier applied to the monster's base attack.
        defence_modify_ratio: Multiplier applied to the monster's base defense.
        hp_modify_ratio: Multiplier applied to the monster's base HP.
        spd_modify_ratio: Multiplier applied to the monster's base speed.
        spd_modify_value: An optional fixed value added to the monster's speed (can override base speed).
        stance_modify_value: Multiplier applied to the monster's base toughness.
        stance_modify_fixed_value: An optional fixed value that overrides the monster's base toughness.
        elite_group: The elite group ID used to scale this variant's stats.
        hard_level_group: The difficulty group ID used to scale this variant's stats.
        stance_weak_list: List of elemental types that this monster is weak to (for toughness damage).
        damage_type_resistances: List of resistances the monster has against specific elements.
        skills: List of skills this monster instance can use in combat.
    """

    id: int
    attack_modify_ratio: float = Field(alias="attack_modify_ratio", default=1)
    defence_modify_ratio: float = Field(alias="defence_modify_ratio", default=1)
    hp_modify_ratio: float = Field(alias="hp_modify_ratio", default=1)
    spd_modify_ratio: float = Field(alias="speed_modify_ratio", default=1)
    spd_modify_value: float | None = Field(alias="speed_modify_value", default=None)
    stance_modify_value: float = Field(alias="stance_modify_ratio", default=1)
    stance_modify_fixed_value: float | None = Field(alias="stance_modify_value", default=None)
    elite_group: int = Field(alias="elite_group", default=1)
    hard_level_group: int = Field(alias="hard_level_group", default=1)

    stance_weak_list: list[HSRElement] = Field(alias="stance_weak_list")
    damage_type_resistances: list[DamageTypeResistance] = Field(alias="damage_type_resistance")
    skills: list[HSREnemySkill] = Field(alias="skill_list")


class MonsterPhase(APIModel):
    """Represent one phase of a multi-phase monster.

    Attributes:
        num: The number of the phase.
        max_hp_ratio: The ratio of the monster's max HP allotted to this phase.
    """

    num: int = Field(alias="phase_num")
    max_hp_ratio: float = Field(alias="phase_max_hp_ratio")


class MonsterDrop(APIModel):
    """Represent the rewards dropped by a monster at a specific world level.

    Attributes:
        monster_template_id: The ID of the monster template this drop belongs to.
        world_level: The world (Equilibrium) level this drop applies to.
        avatar_exp_reward: The amount of character EXP awarded.
        item_ids: The IDs of the items dropped.
    """

    monster_template_id: int
    world_level: int = Field(alias="world_level", default=0)
    avatar_exp_reward: int = Field(alias="avatar_exp_reward", default=0)
    item_ids: list[int] = Field(alias="display_item_list")

    @field_validator("item_ids", mode="before")
    @classmethod
    def __extract_item_ids(cls, value: list[dict[str, int]]) -> list[int]:
        return [item["item_id"] for item in value]


class MonsterDetail(APIModel):
    """Represent an enemy monster with details in HSR.

    Attributes:
        id: Unique identifier for the monster.
        rank: The rating of the monster (e.g. "Minion", "Elite", "BigBoss").
        name: Name of the monster.
        description: The description of the monster.
        attack_base: The base attack stat for this monster.
        defence_base: The base defense stat.
        hp_base: The base HP value.
        spd_base: The base speed stat.
        stance_base: The base toughness value.
        stance_count: The number of toughness bars the monster has.
        status_resistance_base: The base status resistance (used for debuff resist chance).
        critical_damage_base: The base critical damage stat.
        initial_delay_ratio: The action delay ratio applied to the monster's first turn.
        minimum_fatigue_ratio: The minimum damage resistance ratio of the monster.
        camp_id: The ID of the faction (camp) the monster belongs to.
        icon: The monster's icon URL.
        max_phase: The number of phases the monster has.
        phases: The per-phase data of a multi-phase monster.
        drops: The rewards dropped by the monster, per world level.
        monster_types: A list of `ChildMonster` variants derived from this monster.
    """

    id: int
    rank: str
    name: str = Field(default="")
    description: str = Field(alias="desc", default="")
    attack_base: float = Field(alias="attack_base", default=0)
    defence_base: float = Field(alias="defence_base", default=0)
    hp_base: float = Field(alias="hp_base", default=0)
    spd_base: float = Field(alias="speed_base", default=0)
    stance_base: float = Field(alias="stance_base", default=0)
    stance_count: int = Field(alias="stance_count", default=0)
    status_resistance_base: float = Field(alias="status_resistance_base", default=0)
    critical_damage_base: float = Field(alias="critical_damage_base", default=0)
    initial_delay_ratio: float | None = Field(alias="initial_delay_ratio", default=None)
    minimum_fatigue_ratio: float = Field(alias="minimum_fatigue_ratio", default=0)
    camp_id: int | None = Field(alias="monster_camp_id", default=None)
    icon: str = Field(alias="image_path")
    max_phase: int = Field(alias="max_monster_phase", default=1)
    phases: list[MonsterPhase] = Field(alias="phase_list", default_factory=list)
    drops: list[MonsterDrop] = Field(alias="drop", default_factory=list)

    monster_types: list[ChildMonster] = Field(alias="child")

    @field_validator(
        "attack_base",
        "defence_base",
        "hp_base",
        "spd_base",
        "stance_base",
        "stance_count",
        "status_resistance_base",
        "critical_damage_base",
        "minimum_fatigue_ratio",
        mode="before",
    )
    @classmethod
    def default_zero_if_none(cls, value: int | float | None) -> int | float:
        return value if isinstance(value, (int, float)) else 0

    @field_validator("description", mode="before")
    @classmethod
    def default_empty_string(cls, value: str | None) -> str:
        return value or ""

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        filename = value.rsplit("/", 1)[-1]
        filename = filename.replace(".png", ".webp")
        return get_asset_url(Game.HSR, f"monsterfigure/{filename}")

    @property
    def skills(self) -> list[HSREnemySkill]:
        """Get the unique skills across all monster variants, deduplicated by ID."""
        skills: dict[int, HSREnemySkill] = {}
        for monster_type in self.monster_types:
            for skill in monster_type.skills:
                skills.setdefault(skill.id, skill)
        return list(skills.values())


class Monster(APIModel):
    """
    Represent an enemy monster in HSR.

    Attributes:
        id: The ID of the monster.
        icon: The icon URL of the monster.
        children: A list of child monster IDs associated with this monster.
        weaknesses: List of elements that this monster is weak to (used for breaking toughness).
        names: A dictionary of names in different languages.
        description: The English description of the monster.
        name: The English name of the monster.
    """

    id: int  # This field is not present in the API response.
    icon: str
    children: list[int] = Field(alias="child")
    weaknesses: list[HSRElement] = Field(alias="weak")
    names: dict[Literal["en", "zh", "ko", "ja"], str]
    description: str = Field(alias="desc", default="")
    name: str = Field("")  # The value of this field is assigned in post processing.

    @field_validator("description", mode="before")
    @classmethod
    def default_empty_string_listing(cls, value: str | None) -> str:
        return value or ""

    @field_validator("icon", mode="before")
    @classmethod
    def __convert_icon(cls, value: str) -> str:
        filename = value.rsplit("/", 1)[-1]
        filename = filename.replace(".png", ".webp")
        return get_asset_url(Game.HSR, f"monsterfigure/{filename}")

    @model_validator(mode="before")
    @classmethod
    def __transform_names(cls, values: dict[str, Any]) -> dict[str, Any]:
        # This is probably the most questionable API design decision I've ever seen.
        values["names"] = {
            "en": values.pop("en"),
            "zh": values.pop("zh"),
            "ko": values.pop("ko"),
            "ja": values.pop("ja"),
        }
        return values
