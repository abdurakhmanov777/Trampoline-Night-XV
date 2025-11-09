"""
Базовый класс для всех ORM-моделей.
"""

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс ORM с поддержкой асинхронных атрибутов."""
    pass
