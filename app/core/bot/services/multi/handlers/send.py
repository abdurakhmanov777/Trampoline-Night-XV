"""
Модуль обработки состояния отправки финального сообщения с изображением.
"""

from io import BytesIO
from typing import Any, Optional, Union

from aiogram import types
from aiogram.enums import ChatAction

from app.core.bot.services.generator import generate_text_image
from app.core.bot.services.multi.context import MultiContext


async def handle_send(
    ctx: MultiContext,
) -> Optional[int]:
    """
    Обрабатывает состояние отправки финального сообщения с изображением.

    Args:
        ctx (MultiContext): Контекст с параметрами обработки.

    Returns:
        Optional[int]: ID отправленного сообщения (для закрепления),
            либо None, если отправка невозможна.
    """

    event: Any = ctx.event
    loc: Any = ctx.loc
    tg_id: int = ctx.tg_id

    # Универсальный способ получить message
    message: Optional[types.MaybeInaccessibleMessageUnion]
    if isinstance(event, types.CallbackQuery):
        message = event.message
    else:
        message = event

    if not message or not message.bot:
        return None

    # Генерация кода (временно)
    code: int = 1

    # Анимация загрузки
    await message.bot.send_chat_action(
        chat_id=tg_id,
        action=ChatAction.UPLOAD_PHOTO
    )

    try:
        # Генерация изображения
        buffer: BytesIO = await generate_text_image(str(code))

        p1: str
        p2: str
        p1, p2 = loc.template.send
        caption: str = f"{p1}{code}{p2}"

        # Отправка фото
        msg: types.Message = await message.answer_photo(
            photo=types.BufferedInputFile(buffer.read(), filename="code.png"),
            caption=caption,
            parse_mode="HTML"
        )

        # Закрепление сообщения
        await message.bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=msg.message_id
        )

        return msg.message_id

    except BaseException:
        return None
