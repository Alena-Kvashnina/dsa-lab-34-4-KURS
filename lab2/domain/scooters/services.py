"""Доменные сервисы предметной области «Прокат самокатов»."""

from datetime import datetime

from domain.scooters.scooter import Scooter
from domain.scooters.trip import Trip
from domain.scooters.value_objects import TripId


class StartTripService:
    """Операция «начать поездку».

    Доменный сервис, а не метод одного агрегата: нужно проверить
    и изменить состояние Scooter (свободен ли, достаточно ли заряда)
    и создать новую запись в Trip. Ни один агрегат не может
    выполнить это в одиночку.
    """

    def start_trip(self, scooter: Scooter, started_at: datetime) -> Trip:
        scooter.start_trip()  # бросит DomainInvariantViolation при нарушении правил 1-2
        return Trip(TripId.new(), scooter.id, started_at)
