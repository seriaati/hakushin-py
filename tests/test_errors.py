from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import hakushin

if TYPE_CHECKING:
    from hakushin.clients.gi import GIClient
    from hakushin.clients.hsr import HSRClient
    from hakushin.clients.zzz import ZZZClient


async def test_gi_not_found(gi_client: GIClient) -> None:
    with pytest.raises(hakushin.errors.NotFoundError):
        await gi_client.fetch_character_detail("0")


async def test_hsr_not_found(hsr_client: HSRClient) -> None:
    with pytest.raises(hakushin.errors.NotFoundError):
        await hsr_client.fetch_character_detail(0)


async def test_zzz_not_found(zzz_client: ZZZClient) -> None:
    with pytest.raises(hakushin.errors.NotFoundError):
        await zzz_client.fetch_character_detail(0)
