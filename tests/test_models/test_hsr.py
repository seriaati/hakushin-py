from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hakushin.clients.hsr import HSRClient


async def test_characters(hsr_client: HSRClient) -> None:
    await hsr_client.fetch_characters()


async def test_character(hsr_client: HSRClient) -> None:
    characters = await hsr_client.fetch_characters()
    for chara_id in [char.id for char in characters]:
        await hsr_client.fetch_character_detail(chara_id)


async def test_light_cones(hsr_client: HSRClient) -> None:
    await hsr_client.fetch_light_cones()


async def test_light_cone(hsr_client: HSRClient) -> None:
    light_cones = await hsr_client.fetch_light_cones()
    for light_cone_id in [light_cone.id for light_cone in light_cones]:
        await hsr_client.fetch_light_cone_detail(light_cone_id)


async def test_relic_set(hsr_client: HSRClient) -> None:
    relic_sets = await hsr_client.fetch_relic_sets()
    for relic_set_id in [relic_set.id for relic_set in relic_sets]:
        await hsr_client.fetch_relic_set_detail(relic_set_id)


async def test_monsters(hsr_client: HSRClient) -> None:
    monsters = await hsr_client.fetch_monsters()
    for monster_id in [monster.id for monster in monsters]:
        await hsr_client.fetch_monsters_detail(monster_id)


async def test_moc(hsr_client: HSRClient) -> None:
    mocs = await hsr_client.fetch_moc()
    for moc in mocs:
        await hsr_client.fetch_moc_detail(moc.id)


async def test_moc_extra_node(hsr_client: HSRClient) -> None:
    summary = next(moc for moc in await hsr_client.fetch_moc() if moc.id == 1036)
    assert summary.begin == "2026-08-24 04:00:00"

    moc = await hsr_client.fetch_moc_detail(1036, full=True)
    assert moc.memory_turbulence.startswith(
        "When an ally target uses their Ultimate, they gain 5 Punchlines.\n"
    )
    assert len(moc.stages) == 13

    node = moc.stages[-1]
    assert node.pre_id == 5512
    assert node.cycle_limit == 45
    assert node.second_half is None
    assert node.challenges[2].name == "No more than 0 downed character(s)"
    assert node.special_challenge is not None
    assert node.special_challenge.name == "Gain 3 stars and win with 33 or more Cycles remaining"

    corrosion = node.first_half.corrosion
    assert corrosion is not None
    assert corrosion.level == 3
    assert [m.id for m in corrosion.monsters] == [4064010, 4062010, 4063010]

    boss = node.first_half.waves[1].enemies[0]
    assert boss.id == 4064010
    assert (boss.base_hp, boss.max_phase) == (7258991, 2)


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
