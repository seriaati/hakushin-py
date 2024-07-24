import pytest

import hakushin


@pytest.mark.asyncio
async def test_new() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.HSR) as client:
        await client.fetch_new()


@pytest.mark.asyncio
async def test_characters() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.HSR) as client:
        await client.fetch_characters()


@pytest.mark.asyncio
async def test_character() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.HSR) as client:
        new = await client.fetch_new()
        for chara_id in new.character_ids:
            await client.fetch_character_detail(chara_id)


@pytest.mark.asyncio
async def test_light_cones() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.HSR) as client:
        await client.fetch_light_cones()


@pytest.mark.asyncio
async def test_light_cone() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.HSR) as client:
        hsr_new = await client.fetch_new()
        for light_cone_id in hsr_new.light_cone_ids:
            await client.fetch_light_cone_detail(light_cone_id)


@pytest.mark.asyncio
async def test_relic_set() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.HSR) as client:
        hsr_new = await client.fetch_new()
        for relic_set_id in hsr_new.relic_set_ids:
            await client.fetch_relic_set_detail(relic_set_id)
