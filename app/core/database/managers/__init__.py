"""
Пакет менеджеров базы данных.

Импортирует все менеджеры для работы с моделями
"""

from .admin import AdminManager
from .flag import FlagManager

# from .user import User

# Список публичных объектов модуля
__all__: list[str] = [
    "AdminManager",
    # "Base",
    # "Data",
    # "User",
    "FlagManager",
]
