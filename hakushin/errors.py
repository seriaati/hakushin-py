__all__ = ("HakushinError", "NotFoundError")


class HakushinError(Exception):
    """Base class for exceptions in the Hakushin API."""

    def __init__(self, status: int, message: str, url: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message
        self.url = url

    def __str__(self) -> str:
        return f"{self.status}: {self.message} ({self.url})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} status={self.status} message={self.message!r} url={self.url!r}>"


class NotFoundError(HakushinError):
    """Raised when the requested resource is not found."""

    def __init__(self, url: str) -> None:
        super().__init__(404, "The requested resource was not found.", url)
