from dataclasses import dataclass


@dataclass
class BaseConfigExceptions(BaseException):
    message: str = "Some error occurred"
    exc_details: str = "Details..."

    def __repr__(self):
        return f"{self.message}\n{self.exc_details}"

    def __str__(self):
        return self.__repr__()


@dataclass
class FailedDownloadProjectSettings(BaseConfigExceptions):
    message: str = "Setting isn't download. It's validation error or env file does not exist"
