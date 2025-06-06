# Getting Started

## Installation

```bash
pip install hakushin-py
```

## Usage

Every API call goes through the `HakushinAPI` class. You can see more details in the [API Reference](./api_reference/clients/client.md).

```py
import hakushin

async with hakushin.HakushinAPI(hakushin.Game.GI) as api: 
    characters = await api.fetch_characters()
    print(characters)
```

Overall, it's pretty straightforward. You can find all the available methods in the [API Reference](./api_reference/clients/client.md).

## Tips

### Starting and Closing the Client Properly

Remember to call `start()` and `close()` or use `async with` to ensure proper connection management.

```py
import hakushin

async with hakushin.HakushinAPI() as api:
    ...

# OR
api = hakushin.HakushinAPI()
await api.start()
...
await api.close()
```

### Finding Model Attributes

Refer to the [Models](./api_reference/models/models.md) section for a list of all available models and their attributes.

### Catching Errors

Refer to the [Errors](./api_reference/errors.md) section for a list of all available exceptions, catch them with `try/except` blocks.

```py
import hakushin

async with hakushin.HakushinAPI(hakushin.Game.GI) as api:
    try:
        await api.fetch_character(0)
    except hakushin.errors.NotFoundError:
        print("Character does not exist.")
```
