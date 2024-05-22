# hakushin-py

## Quick links

Developing something for Hoyoverse games? Here's a collection of Python async API wrappers for Hoyoverse games made by me:

- [enka.py](https://github.com/seriaati/enka-py) is an Enka Network API wrapper for fetching in-game showcase.
- [yatta.py](https://github.com/seriaati/yatta) is a Project Yatta API wrapper for fetching Honkai Star Rail game data.
- [ambr.py](https://github.com/seriaati/ambr) is a Project Ambr API wrapper for fetching Genshin Impact game data.
- [hakushin.py](https://github.com/seriaati/hakushin-py) is a Hakushin API wrapper for fetching Genshin Impact and Honkai Star Rail beta game data.

## Introduction

hakushin-py is an async API wrapper for [hakush.in](https://hakush.in/) written in Python.  
Hakush.in is a website that displays beta game data for Genshin Impact and Honkai Star Rail.

> Note: I am not the developer of hakush.in

### Features

- Fully typed.
- Fully asynchronous by using `aiofiles`, `aiohttp`, and `asyncio`, suitable for Discord bots.
- Provides direct icon URLs.
- Supports Python 3.11+.
- Supports all game languages.
- Supports both Genshin Impact and Honkai Star Rail.
- Supports persistent caching using SQLite.
- Supports [Pydantic V2](https://github.com/pydantic/pydantic), this also means full autocomplete support.

## Installation

```bash
# poetry
poetry add hakushin-py

# pip
pip install hakushin-py
```

## Quick Example

```py
import hakushin
import asyncio

async def main() -> None:
    async with hakushin.HakushinAPI(hakushin.Language.EN) as client:
        await client.fetch_new(hakushin.Game.GI)

asyncio.run(main())
```

## Getting Started

Read the [wiki](https://github.com/seriaati/hakushin-py/wiki) to learn more about on how to use this wrapper.

## Questions, Issues, Contributions

For questions, you can contact me on [Discord](https://discord.com/users/410036441129943050) or open an [issue](https://github.com/seriaati/hakushin-py/issues).  
To report issues with this wrapper, open an [issue](https://github.com/seriaati/hakushin-py/issues).  
To contribute, fork this repo and submit a [pull request](https://github.com/seriaati/hakushin-py/pulls).
