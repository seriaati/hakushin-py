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


@pytest.mark.asyncio
async def test_weapons() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
        await client.fetch_weapons()


@pytest.mark.asyncio
async def test_weapon_detail() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
        weapons = await client.fetch_weapons()
        for weapon in weapons:
            await client.fetch_weapon_detail(weapon.id)


@pytest.mark.asyncio
async def test_bangbooss() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
        await client.fetch_bangboos()


@pytest.mark.asyncio
async def test_bangboo_detail() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
        bangboos = await client.fetch_bangboos()
        for bangboo in bangboos:
            await client.fetch_bangboo_detail(bangboo.id)


@pytest.mark.asyncio
async def test_drive_discs() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
        await client.fetch_drive_discs()


@pytest.mark.asyncio
async def test_drive_disc_detail() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
        drive_discs = await client.fetch_drive_discs()
        for drive_disc in drive_discs:
            await client.fetch_drive_disc_detail(drive_disc.id)


@pytest.mark.asyncio
async def test_items() -> None:
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
        await client.fetch_items()
