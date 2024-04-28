# hakushin-py

 An async API wrapper for [Hakushin](https://hakush.in/) written in Python. Hakushin is a website that display Genshin Impact and Honkai: Star Rail game data, including the beta ones.  
 > Note: I am not the developer of Hakushin.  

## Quick Links

Developing something for Hoyoverse games? Check out my other API wrappers:

- [enka.py](https://github.com/seriaati/enka-py) is an Enka Network API wrapper for fetching in-game showcase.
- [yatta](https://github.com/seriaati/yatta) is a Project Yatta API wrapper for fetching Honkai Star Rail game data.
- [ambr](https://github.com/seriaati/yatta) is a Project Ambr API wrapper for fetching Genshin Impact game data.

## Features

- Fully typed.
- Provides direct icon URLs.
- Fully asynchronous by using `aiosqlite`, `aiohttp`, and `asyncio`.
- Supports persistent caching using SQLite.
- Supports [Pydantic V2](https://github.com/pydantic/pydantic).
- Supports both Genshin Impact and Honkai: Star Rail.
- 100% test coverage.

> [!IMPORTANT]  
> This wrapper is mainly focused on fetching beta game data, this mean that it **does not** cover all the endpoints of the Hakushin API and models do not cover all the fields from the API's response.

## Installing

```bash
# poetry
poetry add git+https://github.com/seriaati/hakushin-py

# pip
pip install git+https://github.com/seriaati/hakushin-py
```

## Quick Example

```py
import hakushin
import asyncio

async def main() -> None:
    async with hakushin.HakushinAPI() as client:
        await client.fetch_character(10000095, hakushin.Game.GI)
        await client.fetch_character(1309, hakushin.Game.HSR)

asyncio.run(main())
```

# Usage

## Starting and closing the client properly

To use the client properly, you can either:  
Manually call `start()` and `close()`  

```py
import hakushin
import asyncio

async def main() -> None:
    api = hakushin.HakushinAPI()
    await api.start()
    await api.fetch_new(hakushin.Game.GI)
    await api.close()

asyncio.run(main())
```

Or use the `async with` syntax:  

```py
import hakushin
import asyncio

async def main() -> None:
    async with hakushin.HakushinAPI() as api:
        await api.fetch_new(hakushin.Game.GI)

asyncio.run(main())
```

> [!IMPORTANT]  
> You ***need*** to call `start()` or the api client will not function properly; the `close()` method closes the request session and database properly.

## Finding models' attributes

If you're using an IDE like VSCode or Pycharm, then you can see all the attributes and methods the model has in the autocomplete.
> [!TIP]
> If you're using VSCode, `alt` + `left click` on the attribute, then the IDE will bring you to the source code of this wrapper for you to see all the fields defined, most classes and methods have docstrings for you to reference to.

## Catching exceptions

If data is not found (API returns 404), then `hakushin.errors.NotFoundError` will be raised.

# Questions, issues, contributions

For questions, you can contact me on [Discord](https://discord.com/users/410036441129943050) or open an [issue](https://github.com/seriaati/hakushin/issues).  
To report issues with this wrapper, open an [issue](https://github.com/seriaati/hakushin/issues).  
To contribute, fork this repo and submit a [pull request](https://github.com/seriaati/hakushin/pulls).
