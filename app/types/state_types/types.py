from typing import Literal, TypeAlias

connected: bool | None = None
LogLevel: TypeAlias = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
