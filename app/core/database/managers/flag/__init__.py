"""
Инициализация менеджера флагов.
"""

from .crud import FlagCRUD
from .list import FlagList


class FlagManager(FlagCRUD, FlagList):
    """
    Полнофункциональный менеджер для работы с таблицей флагов.

    Включает:
    - CRUD-операции (создание, получение, обновление, удаление)
    - Получение списка всех флагов
    """
    pass
