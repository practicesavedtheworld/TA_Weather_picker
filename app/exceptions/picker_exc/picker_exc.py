from dataclasses import dataclass


@dataclass
class BasePickerExceptions(BaseException):
    message: str = "Some error occurred"
    exc_details: str = "Details..."

    def __repr__(self):
        return f"{self.message}\n{self.exc_details}"

    def __str__(self):
        return self.__repr__()


@dataclass
class PickerConnectionError(BasePickerExceptions):
    message: str = "Connection refused"


@dataclass
class PickerClientError(BasePickerExceptions):
    message: str = "Session is broken"

