"""
Модуль обработки пользовательских сообщений Telegram-бота для приватных чатов.

Содержит обработчик пользовательских сообщений с динамическими
клавиатурами и локализацией.
"""

from typing import Any

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from app.core.bot.routers.filters import ChatTypeFilter
from app.core.bot.services.logger import log
from app.core.bot.services.multi import multi
from app.core.bot.services.requests.user import manage_user, manage_user_state
from app.core.database.models.user import User

user_message: Router = Router()


@user_message.message(
    ChatTypeFilter(chat_type=["private"])
)
async def msg_user(
    message: types.Message,
    state: FSMContext
) -> None:
    """Обрабатывает входящие сообщения пользователя.

    Получает текст и клавиатуру из локализации по текущему шагу
    пользователя и обновляет сообщение с динамической клавиатурой.

    Args:
        message (types.Message): Входящее сообщение Telegram.
        state (FSMContext): Контекст FSM для хранения данных пользователя.
    """
    if not message.from_user or not message.bot:
        return

    # Получаем локализацию пользователя
    user_data: dict[str, Any] = await state.get_data()
    loc: Any | None = user_data.get("loc_user")
    if not loc:
        return

    tg_id: int = message.from_user.id

    # Получаем состояние и данные пользователя из базы
    db_user: User | bool | None | int = await manage_user(
        tg_id=tg_id,
        action="get"
    )
    user_state: bool | str | list[str] | None = await manage_user_state(
        tg_id,
        "peek"
    )

    if not isinstance(db_user, User) or not isinstance(user_state, str):
        return

    # Проверяем, что шаг пользователя ожидает ввод текста
    state_obj: Any | None = getattr(loc.steps, user_state, None)
    if not state_obj or state_obj.type != "input":
        return

    # Генерация текста сообщения, клавиатуры и параметров предпросмотра
    text_message: str
    keyboard_message: types.InlineKeyboardMarkup
    link_opts: types.LinkPreviewOptions

    text_message, keyboard_message, link_opts = await multi(
        loc=loc,
        value=user_state,
        tg_id=tg_id,
        data=message.text
    )

    # Обновляем предыдущее сообщение с новым текстом и клавиатурой
    try:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=db_user.msg_id,
            text=text_message,
            reply_markup=keyboard_message,
            link_preview_options=link_opts
        )
    except BaseException:
        pass

    await log(message)
