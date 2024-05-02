import pytest

import hakushin


@pytest.mark.asyncio
async def test_errors() -> None:
    async with hakushin.HakushinAPI() as client:
        with pytest.raises(hakushin.errors.NotFoundError):
            await client.fetch_character_detail(0, hakushin.Game.GI)
            await client.fetch_character_detail(0, hakushin.Game.HSR)
