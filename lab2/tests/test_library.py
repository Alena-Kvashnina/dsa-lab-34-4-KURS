from datetime import date, timedelta
from decimal import Decimal

import pytest

from domain.exceptions import DomainInvariantViolation, InvalidValueObject
from domain.library.book import Book
from domain.library.services import CheckoutService
from domain.library.value_objects import BookId, LoanPeriod, ReaderId


def make_book(total_copies: int = 1) -> Book:
    return Book(BookId.new(), total_copies)


def make_period(days: int = 14) -> LoanPeriod:
    issue = date(2026, 9, 1)
    return LoanPeriod(issue_date=issue, due_date=issue + timedelta(days=days))


def test_checkout_fails_when_no_copies_available():
    book = make_book(total_copies=0)
    service = CheckoutService()
    with pytest.raises(DomainInvariantViolation):
        service.checkout(book, ReaderId.new(), make_period())


def test_checkout_decreases_available_copies():
    book = make_book(total_copies=1)
    service = CheckoutService()
    service.checkout(book, ReaderId.new(), make_period())
    assert book.available_copies == 0


def test_loan_period_rejects_due_date_before_issue_date():
    with pytest.raises(InvalidValueObject):
        LoanPeriod(issue_date=date(2026, 9, 10), due_date=date(2026, 9, 1))


def test_return_book_twice_is_forbidden():
    book = make_book(total_copies=1)
    loan = CheckoutService().checkout(book, ReaderId.new(), make_period())
    loan.return_book(date(2026, 9, 5), fine_per_day=Decimal("10"))
    with pytest.raises(DomainInvariantViolation):
        loan.return_book(date(2026, 9, 6), fine_per_day=Decimal("10"))


def test_fine_is_calculated_when_returned_late():
    book = make_book(total_copies=1)
    loan = CheckoutService().checkout(book, ReaderId.new(), make_period(days=14))
    return_date = date(2026, 9, 1) + timedelta(days=17)  # 3 дня просрочки
    fine = loan.return_book(return_date, fine_per_day=Decimal("10"))
    assert fine.amount == Decimal("30")


def test_no_fine_when_returned_on_time():
    book = make_book(total_copies=1)
    loan = CheckoutService().checkout(book, ReaderId.new(), make_period(days=14))
    fine = loan.return_book(date(2026, 9, 10), fine_per_day=Decimal("10"))
    assert fine.amount == Decimal("0")
