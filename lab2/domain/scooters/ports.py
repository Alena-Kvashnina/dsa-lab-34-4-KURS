"""Репозитории домена «Прокат самокатов», описанные как Protocol (порт)."""

from typing import Protocol

from domain.scooters.scooter import Scooter
from domain.scooters.trip import Trip
from domain.scooters.value_objects import ScooterId, TripId


class ScooterRepository(Protocol):
    def get(self, scooter_id: ScooterId) -> Scooter: ...
    def save(self, scooter: Scooter) -> None: ...


class TripRepository(Protocol):
    def get(self, trip_id: TripId) -> Trip: ...
    def save(self, trip: Trip) -> None: ...
