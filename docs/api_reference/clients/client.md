# API Reference

## HakushinAPI

You should use the `HakushinAPI` class to get clients for the different games.

For methods that each client has, refer to the different game sections in the sidebar.

```py
import hakushin

# Genshin Impact client
async with hakushin.HakushinAPI(hakushin.Game.GI) as client:
    ...

# Honkai Star Rail client
async with hakushin.HakushinAPI(hakushin.Game.HSR) as client:
    ...

# Zenless Zone Zero client
async with hakushin.HakushinAPI(hakushin.Game.ZZZ) as client:
    ...
```
