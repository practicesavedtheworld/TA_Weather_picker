import decimal
from typing import TypeAlias

Float: TypeAlias = float | decimal.Decimal
FLOAT_OR_INT: TypeAlias = Float | int
