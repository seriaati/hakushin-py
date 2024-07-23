import pytest

import hakushin


@pytest.mark.asyncio
async def test_not_found_error() -> None:
    with pytest.raises(hakushin.errors.NotFoundError):
        async with hakushin.HakushinAPI(hakushin.Game.GI) as client:
            await client.fetch_character_detail("0")
        async with hakushin.HakushinAPI(hakushin.Game.HSR) as client:
            await client.fetch_character_detail(0)
        async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
            await client.fetch_character_detail(0)
