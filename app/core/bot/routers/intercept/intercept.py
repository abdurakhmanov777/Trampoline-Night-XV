from typing import Dict, Union

from aiogram import Router
from aiogram.types import CallbackQuery, Message

from app.core.bot.routers.filters import InterceptFilter

intercept_handler: Router = Router()


@intercept_handler.callback_query(
    InterceptFilter()
)
async def open_settings(
    event: Union[CallbackQuery, Message],
    block_info: Dict[str, bool],
) -> None:
    """
    Обработчик открытия настроек администратора.

    Args:
        event: Событие от пользователя (CallbackQuery или Message).
        block_info: Словарь активных флагов системного блока.
    """
    # Словарь флагов и соответствующих сообщений
    flag_messages: Dict[str, str] = {
        "flag_bot": (
            "Технические шоколадки\n\nПопробуйте зайти через 10 минут"
        ),
        "flag_reg": (
            "К сожалению, регистрация закрыта"
        ),
    }

    # Получаем первое сообщение для активного флага
    text: str | None = next(
        (
            message
            for flag, message in flag_messages.items()
            if block_info.get(flag)
        ),
        None,  # Если ни один флаг не сработал, text будет None
    )

    # Если есть сообщение, показываем его пользователю
    if text is not None:
        await event.answer(
            text=text,
            show_alert=True,
        )
