from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import hakushin
from hakushin.client import HakushinAPI

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from hakushin.clients.gi import GIClient
    from hakushin.clients.hsr import HSRClient
    from hakushin.clients.zzz import ZZZClient


@pytest.fixture
async def gi_client() -> AsyncGenerator[GIClient]:
    async with HakushinAPI(hakushin.Game.GI) as client:
        yield client


@pytest.fixture
async def hsr_client() -> AsyncGenerator[HSRClient]:
    async with HakushinAPI(hakushin.Game.HSR) as client:
        yield client


@pytest.fixture
async def zzz_client() -> AsyncGenerator[ZZZClient]:
    async with HakushinAPI(hakushin.Game.ZZZ) as client:
        yield client
