"""
Инициализация менеджера пользователей.
"""

from .crud import UserCRUD
from .state import UserState
from .update import UserUpdate


class UserManager(UserUpdate, UserState, UserCRUD):
    """
    Полнофункциональный менеджер для работы с пользователями Telegram:
    - CRUD-операции
    - Управление стеком состояний
    - Обновление полей
    """
    pass
