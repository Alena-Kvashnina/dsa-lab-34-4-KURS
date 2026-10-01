"""Объекты-значения предметной области «Прокат самокатов»."""

from dataclasses import dataclass
from uuid import UUID, uuid4

from domain.exceptions import InvalidValueObject


@dataclass(frozen=True)
class ScooterId:
    value: UUID

    @staticmethod
    def new() -> "ScooterId":
        return ScooterId(uuid4())


@dataclass(frozen=True)
class TripId:
    value: UUID

    @staticmethod
    def new() -> "TripId":
        return TripId(uuid4())


@dataclass(frozen=True)
class ChargeLevel:
    """Уровень заряда батареи в процентах, 0..100.

    Валидация диапазона — прямо в конструкторе (объект-значение
    не может существовать в недопустимом состоянии).
    """

    percent: int

    def __post_init__(self) -> None:
        if not (0 <= self.percent <= 100):
            raise InvalidValueObject("Уровень заряда должен быть от 0 до 100")

    def is_below(self, threshold: "ChargeLevel") -> bool:
        return self.percent < threshold.percent
