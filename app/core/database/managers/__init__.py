"""
Инициализация всех менеджеров базы данных.

Позволяет импортировать все менеджеры из одного места.
Менеджеры предоставляют CRUD и вспомогательные операции
для работы с таблицами: Admin, Data, Flag и User.
"""

from .admin import AdminManager
from .data import DataManager
from .flag import FlagManager
from .user import UserManager

# Список доступных для импорта менеджеров
__all__: list[str] = [
    "AdminManager",
    "DataManager",
    "FlagManager",
    "UserManager",
]
