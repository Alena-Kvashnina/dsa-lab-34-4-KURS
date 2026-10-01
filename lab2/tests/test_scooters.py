from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from domain.exceptions import DomainInvariantViolation, InvalidValueObject
from domain.scooters.scooter import Scooter, ScooterStatus
from domain.scooters.services import StartTripService
from domain.scooters.value_objects import ChargeLevel, ScooterId


def make_scooter(charge_percent: int = 80, status: ScooterStatus = ScooterStatus.FREE) -> Scooter:
    return Scooter(ScooterId.new(), ChargeLevel(charge_percent), status)


def test_start_trip_fails_when_scooter_not_free():
    scooter = make_scooter(status=ScooterStatus.RENTED)
    with pytest.raises(DomainInvariantViolation):
        StartTripService().start_trip(scooter, datetime(2026, 9, 1, 10, 0))


def test_start_trip_fails_when_charge_too_low():
    scooter = make_scooter(charge_percent=5)
    with pytest.raises(DomainInvariantViolation):
        StartTripService().start_trip(scooter, datetime(2026, 9, 1, 10, 0))


def test_start_trip_marks_scooter_as_rented():
    scooter = make_scooter(charge_percent=80)
    StartTripService().start_trip(scooter, datetime(2026, 9, 1, 10, 0))
    assert scooter.status is ScooterStatus.RENTED


def test_charge_level_rejects_out_of_range_value():
    with pytest.raises(InvalidValueObject):
        ChargeLevel(150)


def test_finish_trip_twice_is_forbidden():
    scooter = make_scooter()
    trip = StartTripService().start_trip(scooter, datetime(2026, 9, 1, 10, 0))
    trip.finish(datetime(2026, 9, 1, 10, 20), Decimal("5"), Decimal("50"))
    with pytest.raises(DomainInvariantViolation):
        trip.finish(datetime(2026, 9, 1, 10, 30), Decimal("5"), Decimal("50"))


def test_finish_before_start_is_forbidden():
    scooter = make_scooter()
    trip = StartTripService().start_trip(scooter, datetime(2026, 9, 1, 10, 0))
    with pytest.raises(DomainInvariantViolation):
        trip.finish(datetime(2026, 9, 1, 9, 0), Decimal("5"), Decimal("50"))


def test_cost_never_below_minimum():
    scooter = make_scooter()
    trip = StartTripService().start_trip(scooter, datetime(2026, 9, 1, 10, 0))
    # поездка всего 1 минуту -> дешевле минимальной стоимости
    cost = trip.finish(
        datetime(2026, 9, 1, 10, 1), price_per_minute=Decimal("5"), minimum_cost=Decimal("50")
    )
    assert cost.amount == Decimal("50")
