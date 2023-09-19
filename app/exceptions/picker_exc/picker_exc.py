from dataclasses import dataclass


@dataclass
class PickerExceptions(BaseException):
    message: str = "Some error occurred"
    exc_details: str = "Details..."

    def __repr__(self):
        return f"{self.message}\n{self.exc_details}"

    def __str__(self):
        return self.__repr__()


@dataclass
class PickerConnectionError(PickerExceptions):
    message: str = "Connection refused"


@dataclass
class PickerClientError(PickerExceptions):
    message: str = "Session is broken"

