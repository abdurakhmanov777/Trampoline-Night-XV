"""
Фильтр для проверки прав администратора с произвольными ролями.
"""

from typing import Any, Callable, Dict, List, Optional, Union

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from app.core.config import MAIN_ADMINS

# Временный список администраторов для демонстрации
TEMP_ADMINS: list[int] = [111111111, 1645736584]


class AdminFilter(BaseFilter):
    """
    Проверяет, является ли пользователь администратором.

    Возвращает словарь с ролью, если пользователь найден,
    иначе False (требование BaseFilter в Aiogram 3.x).
    """

    def __init__(
        self,
        roles: Optional[Dict[str, list[int]]] = None,
    ) -> None:
        """
        Инициализация фильтра.

        Args:
            roles (Optional[Dict[str, list[int]]]): Словарь ролей
                с их пользователями.
        """
        default_roles: Dict[str, List[int]] = {
            "main": MAIN_ADMINS,
            "moderator": TEMP_ADMINS,
        }
        self.roles: Dict[str, list[int]] = roles or default_roles

    async def __call__(
        self,
        event: Message | CallbackQuery,
    ) -> Union[Dict[str, Any], bool]:
        """
        Проверяет роли пользователя.

        Args:
            event (Message | CallbackQuery): Событие от Telegram.

        Returns:
            dict[str, Any] | bool: Словарь с ролью, если пользователь
                найден, иначе False.
        """
        from_user: Any | None = getattr(event, "from_user", None)
        if not from_user:
            return False

        user_id: Any = from_user.id
        chat_id: Optional[int] = None
        bot: Any | None = getattr(event, "bot", None)

        # Определяем chat_id в зависимости от типа события
        if isinstance(event, Message):
            chat_id = event.chat.id
        elif isinstance(event, CallbackQuery):
            if not event.message:
                return False
            chat_id = event.message.chat.id
        else:
            return False

        # Проверяем локальные роли
        for role, ids in self.roles.items():
            if user_id in ids:
                return {"role": role}

        # Проверка через Telegram API
        if bot:
            try:
                member: Any = await bot.get_chat_member(chat_id, user_id)
                if member.status in {"administrator", "creator"}:
                    return {"role": "moderator"}
            except Exception:
                pass

        return False
