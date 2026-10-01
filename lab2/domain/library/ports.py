"""Репозитории домена «Библиотека», описанные как Protocol (порт).

Домен описывает только то, что ему нужно от внешнего мира — уметь
сохранить агрегат и получить его обратно по id — но не знает и не
должен знать, реализовано это настоящей базой данных или словарём
в памяти.
"""

from typing import Protocol

from domain.library.book import Book
from domain.library.loan import Loan
from domain.library.value_objects import BookId, LoanId


class BookRepository(Protocol):
    def get(self, book_id: BookId) -> Book: ...
    def save(self, book: Book) -> None: ...


class LoanRepository(Protocol):
    def get(self, loan_id: LoanId) -> Loan: ...
    def save(self, loan: Loan) -> None: ...
