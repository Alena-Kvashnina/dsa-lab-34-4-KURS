"""Реализации репозиториев поверх in-memory структур (словарей).

Это адаптеры: они реализуют Protocol-порты, описанные в domain/*/ports.py,
но сам домен ничего не знает про их существование и про то, что
«базой данных» здесь служит обычный словарь Python.
"""

from domain.exceptions import NotFoundError
from domain.library.book import Book
from domain.library.loan import Loan
from domain.library.value_objects import BookId, LoanId
from domain.scooters.scooter import Scooter
from domain.scooters.trip import Trip
from domain.scooters.value_objects import ScooterId, TripId


class InMemoryBookRepository:
    def __init__(self) -> None:
        self._items: dict[BookId, Book] = {}

    def get(self, book_id: BookId) -> Book:
        if book_id not in self._items:
            raise NotFoundError(f"Книга {book_id} не найдена")
        return self._items[book_id]

    def save(self, book: Book) -> None:
        self._items[book.id] = book


class InMemoryLoanRepository:
    def __init__(self) -> None:
        self._items: dict[LoanId, Loan] = {}

    def get(self, loan_id: LoanId) -> Loan:
        if loan_id not in self._items:
            raise NotFoundError(f"Выдача {loan_id} не найдена")
        return self._items[loan_id]

    def save(self, loan: Loan) -> None:
        self._items[loan.id] = loan


class InMemoryScooterRepository:
    def __init__(self) -> None:
        self._items: dict[ScooterId, Scooter] = {}

    def get(self, scooter_id: ScooterId) -> Scooter:
        if scooter_id not in self._items:
            raise NotFoundError(f"Самокат {scooter_id} не найден")
        return self._items[scooter_id]

    def save(self, scooter: Scooter) -> None:
        self._items[scooter.id] = scooter


class InMemoryTripRepository:
    def __init__(self) -> None:
        self._items: dict[TripId, Trip] = {}

    def get(self, trip_id: TripId) -> Trip:
        if trip_id not in self._items:
            raise NotFoundError(f"Поездка {trip_id} не найдена")
        return self._items[trip_id]

    def save(self, trip: Trip) -> None:
        self._items[trip.id] = trip
