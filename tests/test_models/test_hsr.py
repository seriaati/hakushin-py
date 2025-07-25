from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hakushin.clients.hsr import HSRClient


async def test_new(hsr_client: HSRClient) -> None:
    await hsr_client.fetch_new()


async def test_characters(hsr_client: HSRClient) -> None:
    await hsr_client.fetch_characters()


async def test_character(hsr_client: HSRClient) -> None:
    new = await hsr_client.fetch_new()
    for chara_id in new.character_ids:
        await hsr_client.fetch_character_detail(chara_id)


async def test_light_cones(hsr_client: HSRClient) -> None:
    await hsr_client.fetch_light_cones()


async def test_light_cone(hsr_client: HSRClient) -> None:
    hsr_new = await hsr_client.fetch_new()
    for light_cone_id in hsr_new.light_cone_ids:
        await hsr_client.fetch_light_cone_detail(light_cone_id)


async def test_relic_set(hsr_client: HSRClient) -> None:
    hsr_new = await hsr_client.fetch_new()
    for relic_set_id in hsr_new.relic_set_ids:
        await hsr_client.fetch_relic_set_detail(relic_set_id)


async def test_monsters(hsr_client: HSRClient) -> None:
    hsr_new = await hsr_client.fetch_new()
    for monster_id in hsr_new.monster_ids:
        await hsr_client.fetch_monsters_detail(monster_id)


async def test_moc(hsr_client: HSRClient) -> None:
    mocs = await hsr_client.fetch_moc()
    for moc in mocs:
        await hsr_client.fetch_moc_detail(moc.id)


async def test_pf(hsr_client: HSRClient) -> None:
    pfs = await hsr_client.fetch_pf()
    for pf in pfs:
        await hsr_client.fetch_pf_detail(pf.id)


async def test_apoc(hsr_client: HSRClient) -> None:
    apocs = await hsr_client.fetch_apoc()
    for apoc in apocs:
        await hsr_client.fetch_apoc_detail(apoc.id)


async def test_enemy_stat_calculations(hsr_client: HSRClient) -> None:
    mocs = await hsr_client.fetch_moc()
    for moc in mocs:
        await hsr_client.fetch_moc_detail(moc.id, full=True)

    pfs = await hsr_client.fetch_pf()
    for pf in pfs:
        await hsr_client.fetch_pf_detail(pf.id, full=True)

    apocs = await hsr_client.fetch_apoc()
    for apoc in apocs:
        await hsr_client.fetch_apoc_detail(apoc.id, full=True)
