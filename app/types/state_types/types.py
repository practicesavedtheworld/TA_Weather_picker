from typing import TypeAlias, Literal

connected: bool | None = None
LogLevel: TypeAlias = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
