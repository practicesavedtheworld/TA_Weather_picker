from dataclasses import dataclass


@dataclass
class BaseCitiesExceptions(BaseException):
    message: str = "Cities Error"
    exc_details: str | None = None

    def __repr__(self):
        return f"{self.message}\n{self.exc_details}"

    def __str__(self):
        return self.__repr__()


@dataclass
class NoCitiesSelected(BaseCitiesExceptions):
    message = "At least one city must be selected. Now city quantity is <= 0"
