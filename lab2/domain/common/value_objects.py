"""Объекты-значения, общие для нескольких предметных областей."""

from dataclasses import dataclass
from decimal import Decimal

from domain.exceptions import InvalidValueObject


@dataclass(frozen=True)
class Money:
    """Денежная сумма. Неизменяемый объект-значение.

    Два объекта Money с одинаковой суммой полностью взаимозаменяемы —
    у денег нет собственной идентичности, важно только значение.
    """

    amount: Decimal

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise InvalidValueObject("Сумма не может быть отрицательной")

    def __add__(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)

    def __lt__(self, other: "Money") -> bool:
        return self.amount < other.amount
