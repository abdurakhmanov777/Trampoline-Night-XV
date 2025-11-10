"""
Инициализация менеджера пользователей.

Объединяет все функциональные возможности работы с таблицей User:
- CRUD-операции
- Управление стеком состояний
- Обновление полей пользователя
"""

from .crud import UserCRUD
from .state import UserState
from .update import UserUpdate


class UserManager(
    UserUpdate,
    UserState,
    UserCRUD,
):
    """Полнофункциональный менеджер для работы с пользователями Telegram.

    Наследует методы:
        - UserCRUD: CRUD-операции с пользователями
        - UserState: управление стеком состояний
        - UserUpdate: обновление полей пользователя
    """
    # Пустой класс, объединяющий функционал всех менеджеров
    pass
