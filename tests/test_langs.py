from __future__ import annotations

import pytest

import hakushin


@pytest.mark.asyncio
async def test_langs() -> None:
    for lang in hakushin.Language:
        async with hakushin.HakushinAPI(hakushin.Game.GI, lang) as client:
            await client.fetch_character_detail("10000098")
        async with hakushin.HakushinAPI(hakushin.Game.HSR, lang) as client:
            await client.fetch_character_detail(1309)
        async with hakushin.HakushinAPI(hakushin.Game.ZZZ, lang) as client:
            await client.fetch_character_detail(1011)
