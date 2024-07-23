import pytest

import hakushin


@pytest.mark.asyncio
async def test_new() -> None:
    async with hakushin.HakushinAPI() as client:
        await client.fetch_new(hakushin.Game.ZZZ)


@pytest.mark.asyncio
async def test_characters() -> None:
    async with hakushin.HakushinAPI() as client:
        await client.fetch_characters(hakushin.Game.ZZZ)


@pytest.mark.asyncio
async def test_character_detail() -> None:
    async with hakushin.HakushinAPI() as client:
        new = await client.fetch_new(hakushin.Game.ZZZ)
        for chara_id in new.character_ids:
            await client.fetch_character_detail(chara_id, hakushin.Game.ZZZ)
