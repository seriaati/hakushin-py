from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hakushin.clients.gi import GIClient


async def test_new(gi_client: GIClient) -> None:
    await gi_client.fetch_new()


async def test_characters(gi_client: GIClient) -> None:
    await gi_client.fetch_characters()


async def test_character(gi_client: GIClient) -> None:
    new = await gi_client.fetch_new()
    for chara_id in new.character_ids:
        await gi_client.fetch_character_detail(str(chara_id))


async def test_weapons(gi_client: GIClient) -> None:
    await gi_client.fetch_weapons()


async def test_weapon(gi_client: GIClient) -> None:
    gi_new = await gi_client.fetch_new()
    for weapon_id in gi_new.weapon_ids:
        await gi_client.fetch_weapon_detail(weapon_id)


async def test_artifact_sets(gi_client: GIClient) -> None:
    await gi_client.fetch_artifact_sets()


async def test_artifact_set(gi_client: GIClient) -> None:
    gi_new = await gi_client.fetch_new()
    for artifact_set_id in gi_new.artifact_set_ids:
        await gi_client.fetch_artifact_set_detail(artifact_set_id)


async def test_stygians(gi_client: GIClient) -> None:
    stygians = await gi_client.fetch_stygians()
    for entry in stygians:
        await gi_client.fetch_stygian_detail(entry.id)


async def test_mw_costumes(gi_client: GIClient) -> None:
    await gi_client.fetch_mw_costumes()


async def test_mw_costume_sets(gi_client: GIClient) -> None:
    await gi_client.fetch_mw_costume_sets()


async def test_mw_items(gi_client: GIClient) -> None:
    await gi_client.fetch_mw_items()
