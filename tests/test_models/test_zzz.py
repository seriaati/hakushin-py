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
