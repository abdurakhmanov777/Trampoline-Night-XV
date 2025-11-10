"""
Фильтры для проверки системных состояний Telegram-бота.

Содержит фильтр SystemBlockFilter, который срабатывает, если бот
находится в режиме технического обслуживания или регистрация закрыта.
"""

from __future__ import annotations

from typing import Union

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

# Глобальные флаги состояния бота
MAINTENANCE_MODE: bool = False
REGISTRATION_CLOSED: bool = True


class SystemBlockFilter(Filter):
    """
    Фильтр для проверки активных блокировок бота.

    Срабатывает, если активен один из флагов:
    - MAINTENANCE_MODE: бот на техобслуживании.
    - REGISTRATION_CLOSED: регистрация закрыта.
    """

    async def __call__(
        self,
        event: Union[Message, CallbackQuery],
    ) -> bool:
        """
        Проверяет наличие активной блокировки.

        Args:
            event (Message | CallbackQuery): Событие от пользователя.

        Returns:
            bool: True, если бот заблокирован.
        """
        return MAINTENANCE_MODE or REGISTRATION_CLOSED
