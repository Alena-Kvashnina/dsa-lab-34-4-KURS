"""Агрегат «выдача». Loan — сам себе корень, вложенных сущностей нет.

Хранит book_id, а не объект Book — связь между агрегатами
только по идентификатору (Book и Loan — разные агрегаты, см. Раздел II).
"""

from datetime import date
from decimal import Decimal

from domain.common.value_objects import Money
from domain.exceptions import DomainInvariantViolation
from domain.library.value_objects import BookId, LoanId, LoanPeriod, ReaderId


class Loan:
    """Корень агрегата «выдача».

    Инкапсулированные инварианты (из Раздела II):
    - правило 7: одну и ту же выдачу нельзя закрыть возвратом дважды;
    - правило 3: дата возврата не может быть раньше даты выдачи;
    - правило 4: если возврат произошёл после срока, штраф
      рассчитывается и фиксируется.
    """

    def __init__(
        self,
        loan_id: LoanId,
        book_id: BookId,
        reader_id: ReaderId,
        period: LoanPeriod,
    ) -> None:
        self.id = loan_id
        self.book_id = book_id
        self.reader_id = reader_id
        self.period = period
        self._closed = False
        self.fine: Money | None = None

    @property
    def is_closed(self) -> bool:
        return self._closed

    def return_book(self, return_date: date, fine_per_day: Decimal) -> Money:
        """Закрыть выдачу возвратом книги и, если нужно, зафиксировать штраф."""
        if self._closed:
            raise DomainInvariantViolation("Выдача уже закрыта возвратом")
        if return_date < self.period.issue_date:
            raise DomainInvariantViolation(
                "Дата возврата не может быть раньше даты выдачи"
            )

        if self.period.is_overdue(return_date):
            days_late = (return_date - self.period.due_date).days
            self.fine = Money(fine_per_day * days_late)
        else:
            self.fine = Money(Decimal(0))

        self._closed = True
        return self.fine
