# Лабораторная работа №2 — Раздел III

Доменные модели двух предметных областей: Библиотека и Прокат самокатов.

## Структура
- domain/exceptions.py — иерархия доменных исключений
- domain/common/ — общие объекты-значения (Money)
- domain/library/ — агрегаты Book и Loan, доменный сервис CheckoutService
- domain/scooters/ — агрегаты Scooter и Trip, доменный сервис StartTripService
- adapters/memory.py — in-memory реализации репозиториев (Protocol из domain/*/ports.py)
- tests/ — pytest-тесты, подтверждающие работу инвариантов

## Запуск тестов
```
pip install pytest --break-system-packages
PYTHONPATH=. python -m pytest tests/ -v
```
