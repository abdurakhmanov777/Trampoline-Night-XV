"""
Инициализация всех менеджеров базы данных.

Позволяет импортировать все менеджеры из одного места.
"""

from .admin import AdminManager
from .data import DataManager
from .flag import FlagManager
from .user import UserManager

__all__: list[str] = [
    "AdminManager",
    "DataManager",
    "FlagManager",
    "UserManager",
]
