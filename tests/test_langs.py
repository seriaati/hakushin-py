from __future__ import annotations

import pytest

import hakushin


@pytest.mark.parametrize("lang", list(hakushin.Language))
async def test_langs(lang: hakushin.Language) -> None:
    async with hakushin.HakushinAPI(hakushin.Game.GI, lang) as client:
        await client.fetch_character_detail("10000098")

    async with hakushin.HakushinAPI(hakushin.Game.HSR, lang) as client:
        await client.fetch_character_detail(1309)

    async with hakushin.HakushinAPI(hakushin.Game.ZZZ, lang) as client:
        await client.fetch_character_detail(1011)
