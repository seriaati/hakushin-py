import pytest

import hakushin


@pytest.mark.asyncio
async def test_langs() -> None:
    for lang in hakushin.Language:
        async with hakushin.HakushinAPI(lang) as client:
            await client.fetch_character_detail(10000098, hakushin.Game.GI)
            await client.fetch_character_detail(1309, hakushin.Game.HSR)
