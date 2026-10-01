"""Агрегат «поездка». Trip — сам себе корень, вложенных сущностей нет.

Хранит scooter_id, а не объект Scooter — связь между агрегатами
только по идентификатору.
"""

from datetime import datetime
from decimal import Decimal

from domain.common.value_objects import Money
from domain.exceptions import DomainInvariantViolation
from domain.scooters.value_objects import ScooterId, TripId


class Trip:
    """Корень агрегата «поездка».

    Инкапсулированные инварианты (из Раздела II):
    - правило 4: время окончания не может быть раньше времени начала;
    - правило 7: одну и ту же поездку нельзя завершить дважды;
    - правило 5/6: при завершении стоимость рассчитывается по тарифу
      и не может быть отрицательной (обеспечивается через Money).
    """

    def __init__(self, trip_id: TripId, scooter_id: ScooterId, started_at: datetime) -> None:
        self.id = trip_id
        self.scooter_id = scooter_id
        self.started_at = started_at
        self.finished_at: datetime | None = None
        self.cost: Money | None = None

    @property
    def is_finished(self) -> bool:
        return self.finished_at is not None

    def finish(
        self,
        finished_at: datetime,
        price_per_minute: Decimal,
        minimum_cost: Decimal,
    ) -> Money:
        """Завершить поездку и зафиксировать стоимость по тарифу."""
        if self.is_finished:
            raise DomainInvariantViolation("Поездку нельзя завершить дважды")
        if finished_at < self.started_at:
            raise DomainInvariantViolation(
                "Время окончания не может быть раньше времени начала"
            )

        minutes = Decimal(str((finished_at - self.started_at).total_seconds() / 60))
        raw_cost = minutes * price_per_minute
        self.cost = Money(max(raw_cost, minimum_cost))
        self.finished_at = finished_at
        return self.cost
