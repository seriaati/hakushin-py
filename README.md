# hakushin-py

## Introduction

hakushin-py is an async API wrapper for [hakush.in](https://hakush.in/) written in Python.  
hakush.in is a website that displays Genshin Impact, Honkai Star Rail, Zenless Zone Zero, and Wuthering Waves game data.  
Developing something for Hoyoverse games? You might be interested in [other API wrappers](https://github.com/seriaati#api-wrappers) written by me.

> Note: I am not the developer of hakush.in

## Important Note

This wrapper does not support all endpoints from hakush.in, it is mainly focused on fetching the beta game data.  
This means I selectively chose the endpoints and API fields that I personally think are useful for theorycrafting.  
If you want a more complete wrapper for game data, use [ambry.py](https://github.com/seriaati/ambr) and [yatta.py](https://github.com/seriaati/yatta) instead.  
However, **there is an exception for ZZZ**, since Project Ambr and Yatta has no equivalent for ZZZ, this wrapper supports all endpoints for the ZZZ Hakushin API.  
Regarding Wuthering Waves support for this wrapper, it is currently not planned.

### Features

- Fully typed.
- Fully asynchronous by using `aiohttp`, and `asyncio`, suitable for Discord bots.
- Provides direct icon URLs.
- Supports Python 3.11+.
- Supports all game languages.
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
    async with hakushin.HakushinAPI(hakushin.Game.GI, hakushin.Language.EN) as client:
        await client.fetch_characters()
    async with hakushin.HakushinAPI(hakushin.Game.HSR, hakushin.Language.JA) as client:
        await client.fetch_light_cones()
    async with hakushin.HakushinAPI(hakushin.Game.ZZZ, hakushin.Language.KO) as client:
        await client.fetch_weapons()

asyncio.run(main())
```

## Getting Started

Read the [wiki](https://github.com/seriaati/hakushin-py/wiki) to learn more about on how to use this wrapper.

## Questions, Issues, Feedback, Contributions

Whether you want to make any bug reports, feature requests, or contribute to the wrapper, simply open an issue or pull request in this repository.  
If GitHub is not your type, you can find me on [Discord](https://discord.com/invite/b22kMKuwbS), my username is @seria_ati.
