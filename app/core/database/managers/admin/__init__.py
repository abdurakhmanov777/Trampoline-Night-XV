"""
Инициализация менеджера администраторов.
"""

from .crud import AdminCRUD
from .state import AdminState
from .text import AdminText


class AdminManager(AdminText, AdminState, AdminCRUD):
    """
    Полнофункциональный менеджер для работы с администраторами:
    - CRUD-операции
    - Управление стеком состояний
    - Обновление текста
    """
    pass
