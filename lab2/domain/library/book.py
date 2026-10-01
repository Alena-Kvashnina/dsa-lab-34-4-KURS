"""Агрегат «книга». Book — сам себе корень, вложенных сущностей нет."""

from domain.exceptions import DomainInvariantViolation
from domain.library.value_objects import BookId


class Book:
    """Корень агрегата. Хранит количество экземпляров книги.

    Инвариант (правило 1 из Раздела II): нельзя выдать книгу,
    если нет свободных экземпляров. Проверяется внутри метода
    checkout() — снаружи поле available_copies изменить напрямую
    нельзя, только через методы корня.
    """

    def __init__(self, book_id: BookId, total_copies: int) -> None:
        if total_copies < 0:
            raise DomainInvariantViolation(
                "Общее количество экземпляров не может быть отрицательным"
            )
        self.id = book_id
        self._total_copies = total_copies
        self._available_copies = total_copies

    @property
    def available_copies(self) -> int:
        return self._available_copies

    @property
    def total_copies(self) -> int:
        return self._total_copies

    def checkout(self) -> None:
        """Выдать один экземпляр книги."""
        if self._available_copies <= 0:
            raise DomainInvariantViolation("Нет свободных экземпляров книги")
        self._available_copies -= 1

    def return_copy(self) -> None:
        """Вернуть один экземпляр книги."""
        if self._available_copies >= self._total_copies:
            raise DomainInvariantViolation(
                "Нельзя вернуть больше экземпляров, чем всего есть у книги"
            )
        self._available_copies += 1
