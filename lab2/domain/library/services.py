"""Доменные сервисы предметной области «Библиотека»."""

from domain.library.book import Book
from domain.library.loan import Loan
from domain.library.value_objects import LoanId, LoanPeriod, ReaderId


class CheckoutService:
    """Операция «выдать книгу читателю».

    Это доменный сервис, а не метод одного агрегата, потому что
    операция одновременно затрагивает два агрегата: нужно проверить
    и изменить доступность экземпляров у Book и создать новую запись
    в Loan. Ни Book, ни Loan не могут выполнить это в одиночку —
    у каждого есть доступ только к собственным данным.
    """

    def checkout(self, book: Book, reader_id: ReaderId, period: LoanPeriod) -> Loan:
        book.checkout()  # бросит DomainInvariantViolation, если нет свободных экземпляров
        return Loan(LoanId.new(), book.id, reader_id, period)
