"""Объекты-значения предметной области «Библиотека»."""

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from domain.exceptions import InvalidValueObject


@dataclass(frozen=True)
class BookId:
    """Идентификатор книги. Сам по себе тоже объект-значение."""

    value: UUID

    @staticmethod
    def new() -> "BookId":
        return BookId(uuid4())


@dataclass(frozen=True)
class ReaderId:
    """Идентификатор читателя."""

    value: UUID

    @staticmethod
    def new() -> "ReaderId":
        return ReaderId(uuid4())


@dataclass(frozen=True)
class LoanId:
    """Идентификатор выдачи."""

    value: UUID

    @staticmethod
    def new() -> "LoanId":
        return LoanId(uuid4())


@dataclass(frozen=True)
class LoanPeriod:
    """Срок выдачи книги: дата выдачи и установленный срок возврата.

    Инвариант объекта-значения (правило 6 из Раздела II):
    срок возврата не может быть раньше даты выдачи.
    Проверяется один раз, в момент создания — после этого объект
    неизменяем, значит, не может оказаться в недопустимом состоянии позже.
    """

    issue_date: date
    due_date: date

    def __post_init__(self) -> None:
        if self.due_date < self.issue_date:
            raise InvalidValueObject(
                "Срок возврата не может быть раньше даты выдачи"
            )

    def is_overdue(self, return_date: date) -> bool:
        return return_date > self.due_date
