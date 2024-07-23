import pytest

import hakushin


@pytest.mark.asyncio
async def test_new() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
        await client.fetch_new()


@pytest.mark.asyncio
async def test_characters() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
        await client.fetch_characters()


@pytest.mark.asyncio
async def test_character_detail() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
        characters = await client.fetch_characters()
        for ch in characters:
            await client.fetch_character_detail(ch.id)
