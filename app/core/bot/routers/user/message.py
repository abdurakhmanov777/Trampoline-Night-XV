"""
Модуль регистрации сообщений Telegram-бота для приватных чатов.

Содержит обработчики сообщений с динамическими клавиатурами
и локализацией.
"""

from functools import wraps
from typing import Any, Callable

from aiogram import Bot, Router
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.types import User as TgUser

from app.core.bot.routers.filters import ChatTypeFilter
from app.core.bot.services.logger import log
from app.core.bot.services.multi import multi
from app.core.bot.services.requests.user import manage_user, manage_user_state
from app.core.bot.utils.guards.guards import ensure
from app.core.database.models.user import User

router: Router = Router()


def user_message(
    *filters: BaseFilter
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор для регистрации сообщений пользователя в приватных чатах.

    Проверяет наличие сообщения, бота и локализации и передает их
    в хэндлер через именованные аргументы tg_user, bot, loc, message.

    Args:
        *filters (BaseFilter): Дополнительные фильтры для сообщений.

    Returns:
        Callable: Обертка для функции-обработчика сообщения.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(
            message: Message,
            state: FSMContext,
            *args: Any,
            **kwargs: Any
        ) -> None:
            tg_user: TgUser | None = message.from_user
            bot: Bot | None = message.bot
            state_data: dict[str, Any] = await state.get_data()
            loc: Any | None = state_data.get("loc_user")

            if tg_user is None or bot is None or loc is None:
                return

            kwargs.update(
                {"tg_user": tg_user, "bot": bot, "loc": loc, "message": message}
            )
            return await func(message, state, *args, **kwargs)

        return router.message(ChatTypeFilter(["private"]), *filters)(wrapper)

    return decorator


@user_message()
async def msg_user(
    message: Message,
    state: FSMContext,
    *,
    tg_user: TgUser,
    bot: Bot,
    loc: Any
) -> None:
    """Обрабатывает текстовое сообщение пользователя и вызывает
    динамическую логику состояния с типом 'input'.

    Args:
        message (Message): Входящее сообщение Telegram.
        state (FSMContext): Контекст FSM для хранения данных пользователя.
        tg_user (TgUser): Пользователь Telegram.
        bot (Bot): Экземпляр бота.
        loc (Any): Локализация пользователя.
    """
    tg_id: int = tg_user.id

    # Получаем данные пользователя и текущее состояние
    db_user: User | None = ensure(await manage_user(tg_id=tg_id, action="get"), User)
    value: str | None = ensure(await manage_user_state(tg_id, "peek"), str)

    if not db_user or not value:
        return

    # Проверяем, что состояние соответствует "input"
    state_obj: Any | None = getattr(loc, f"userstate_{value}", None)
    if not state_obj or getattr(state_obj, "type", None) != "input":
        return

    # Генерация текста и клавиатуры для сообщения
    text: str
    keyboard: InlineKeyboardMarkup
    text, keyboard = await multi(loc=loc, value=value, tg_id=tg_id, data=message.text)

    # Пробуем обновить последнее сообщение пользователя
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=db_user.msg_id,
            text=text,
            reply_markup=keyboard
        )
    except Exception:
        pass

    await log(message)
