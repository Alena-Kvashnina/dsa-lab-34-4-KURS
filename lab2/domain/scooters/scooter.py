"""Агрегат «самокат». Scooter — сам себе корень, вложенных сущностей нет."""

from enum import Enum, auto

from domain.exceptions import DomainInvariantViolation
from domain.scooters.value_objects import ChargeLevel, ScooterId

MIN_CHARGE_TO_RENT = ChargeLevel(20)


class ScooterStatus(Enum):
    FREE = auto()
    RENTED = auto()
    MAINTENANCE = auto()


class Scooter:
    """Корень агрегата.

    Инкапсулированные инварианты (из Раздела II):
    - правило 1: нельзя начать поездку, если самокат не свободен;
    - правило 2: нельзя начать поездку, если заряд ниже порога.
    """

    def __init__(
        self,
        scooter_id: ScooterId,
        charge: ChargeLevel,
        status: ScooterStatus = ScooterStatus.FREE,
    ) -> None:
        self.id = scooter_id
        self._charge = charge
        self._status = status

    @property
    def status(self) -> ScooterStatus:
        return self._status

    @property
    def charge(self) -> ChargeLevel:
        return self._charge

    def start_trip(self) -> None:
        if self._status is not ScooterStatus.FREE:
            raise DomainInvariantViolation("Самокат не свободен")
        if self._charge.is_below(MIN_CHARGE_TO_RENT):
            raise DomainInvariantViolation(
                "Уровень заряда ниже минимального порога"
            )
        self._status = ScooterStatus.RENTED

    def finish_trip(self) -> None:
        if self._status is not ScooterStatus.RENTED:
            raise DomainInvariantViolation(
                "Самокат не находится в аренде, завершать нечего"
            )
        self._status = ScooterStatus.FREE

    def send_to_maintenance(self) -> None:
        if self._status is ScooterStatus.RENTED:
            raise DomainInvariantViolation(
                "Нельзя отправить на обслуживание арендованный самокат"
            )
        self._status = ScooterStatus.MAINTENANCE
