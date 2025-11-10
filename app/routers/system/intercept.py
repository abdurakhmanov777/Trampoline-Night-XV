from typing import Any, Callable

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.filters import AdminFilter, ChatTypeFilter

router: Router = Router()


def intercept(
    *filters: Any
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Универсальный декоратор для обработки событий администратора
    в приватных чатах.

    Регистрирует одну и ту же функцию как обработчик сообщений и
    callback-запросов, добавляя фильтры администратора и типа чата.

    Args:
        *filters (Any): Дополнительные фильтры для регистрации
            обработчиков.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]:
        Декоратор, регистрирующий обработчик событий.
    """

    def decorator(
        func: Callable[..., Any]
    ) -> Callable[..., Any]:
        # Для callback-запросов
        router.callback_query(
            ChatTypeFilter(chat_type=["private"]),
            AdminFilter(),
            *filters,
        )(func)

        # Для текстовых сообщений
        router.message(
            ChatTypeFilter(chat_type=["private"]),
            AdminFilter(),
            *filters,
        )(func)

        return func

    return decorator


@intercept()
async def open_settings(event: CallbackQuery | Message):
    await event.answer("Настройки администратора")
