"""
Инициализация менеджера данных.
"""

from .crud import DataCRUD
from .list import DataList


class DataManager(DataCRUD, DataList):
    """
    Полнофункциональный менеджер для работы с таблицей Data.

    Включает:
    - CRUD-операции
    - Получение списка всех записей пользователя
    """
    pass
