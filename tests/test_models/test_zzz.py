from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hakushin.clients.zzz import ZZZClient


async def test_new(zzz_client: ZZZClient) -> None:
    await zzz_client.fetch_new()


async def test_characters(zzz_client: ZZZClient) -> None:
    await zzz_client.fetch_characters()


async def test_character_detail(zzz_client: ZZZClient) -> None:
    characters = await zzz_client.fetch_characters()
    for ch in characters:
        await zzz_client.fetch_character_detail(ch.id)


async def test_weapons(zzz_client: ZZZClient) -> None:
    await zzz_client.fetch_weapons()


async def test_weapon_detail(zzz_client: ZZZClient) -> None:
    weapons = await zzz_client.fetch_weapons()
    for weapon in weapons:
        await zzz_client.fetch_weapon_detail(weapon.id)


async def test_bangbooss(zzz_client: ZZZClient) -> None:
    await zzz_client.fetch_bangboos()


async def test_bangboo_detail(zzz_client: ZZZClient) -> None:
    bangboos = await zzz_client.fetch_bangboos()
    for bangboo in bangboos:
        await zzz_client.fetch_bangboo_detail(bangboo.id)


async def test_drive_discs(zzz_client: ZZZClient) -> None:
    await zzz_client.fetch_drive_discs()


async def test_drive_disc_detail(zzz_client: ZZZClient) -> None:
    drive_discs = await zzz_client.fetch_drive_discs()
    for drive_disc in drive_discs:
        await zzz_client.fetch_drive_disc_detail(drive_disc.id)


async def test_items(zzz_client: ZZZClient) -> None:
    await zzz_client.fetch_items()
