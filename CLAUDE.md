# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing

- Run all tests: `pytest`
- Run specific test file: `pytest tests/test_errors.py`
- Run tests with async support: Tests use `pytest-asyncio` with auto mode configured

### Linting and Formatting

- Run linter: `ruff check`
- Auto-fix linting issues: `ruff check --fix`
- Format code: `ruff format`
- Type checking: `pyright` (configured in pyproject.toml)

### Documentation

- Build docs: `mkdocs build`
- Serve docs locally: `mkdocs serve`
- Docs are hosted at <https://gh.seria.moe/hakushin-py>

### Writing Docstrings

1. For class methods that use "cls" as their first argument, decorate them with the @classmethod decorator. Put the decorator right under the pydantic field_validator or model_validator decorator.
2. If a class/method/function already contains docstrings but is not in Google style, fix it to Google style.
3. If a class/method/function already contains docstrings but contains type annotation, remove it. For example, "description (str)" should be changed to "description" because typings are already written in the code as type annotations.
4. If any public class/method/function does not have docstrings, add Google style docstring for it. Do not add docstrings for private methods and magic methods.
5. For python files in the "/models" folder, if a class is not exported to "all", add it to "all".
6. Convert the names of all Pydantic validator methods to dunder methods. For exampe, "convert_icon" or "_convert_icon" should become "__convert_icon".
7. For docstrings of every object, if they are not in imperative tone, convert them to imperative tone.

### Package Management

- Install dependencies: `uv sync`
- Add new dependency: `uv add <package>`
- Build package: `uv build`

## Architecture Overview

### Core Design

hakushin-py is an async API wrapper for the hakush.in API that fetches game data for Genshin Impact, Honkai Star Rail, and Zenless Zone Zero. The library is built around a factory pattern with game-specific clients.

### Key Components

#### Client Factory (`hakushin/client.py`)

- `HakushinAPI` class serves as the main entry point
- Uses overloaded `__new__` method to return game-specific clients based on `Game` enum
- Supports GI, HSR, and ZZZ games with proper type hints

#### Base Client (`hakushin/clients/base.py`)

- `BaseClient` provides shared functionality for all game clients
- Handles HTTP requests with caching via `aiohttp-client-cache` and SQLite backend
- Implements context manager protocol for session management
- Base URL: `https://api.hakush.in`

#### Game-Specific Clients

- `GIClient` (Genshin Impact): `hakushin/clients/gi.py`
- `HSRClient` (Honkai Star Rail): `hakushin/clients/hsr.py`
- `ZZZClient` (Zenless Zone Zero): `hakushin/clients/zzz.py`

#### Models Architecture

- All models inherit from `APIModel` in `hakushin/models/base.py`
- `APIModel` extends Pydantic's `BaseModel` with automatic text cleanup
- Game-specific models organized in subdirectories: `gi/`, `hsr/`, `zzz/`
- Models handle text formatting (cleanup, ruby tag removal, device param replacement)

### Language Support

- `Language` enum supports multiple languages
- HSR uses special language mapping via `HSR_API_LANG_MAP`
- Other games use direct language values

### Caching Strategy

- SQLite-based HTTP response caching with configurable TTL (default: 1 hour)
- Cache stored at `./.cache/hakushin/aiohttp-cache.db` by default
- Can be disabled per request when needed

### Error Handling

- Custom exceptions in `hakushin/errors.py`
- `NotFoundError` for 404 responses
- `HakushinError` for other HTTP errors

## Testing Structure

- Game-specific test files: `tests/test_models/test_{game}.py`
- Shared fixtures in `tests/conftest.py` provide pre-configured clients
- Tests use async fixtures with proper context management
