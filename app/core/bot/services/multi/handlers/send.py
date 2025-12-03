"""
Модуль обработки состояния отправки финального сообщения с изображением.

Содержит логику генерации кода, создания изображения и отправки финального
сообщения пользователю с закреплением в чате.
"""

from datetime import datetime
from io import BytesIO
from typing import Any, Optional, Union

from aiogram import types
from aiogram.enums import ChatAction

from app.core.bot.services.generator import generate_image
from app.core.bot.services.generator.generator_code import generate_code
from app.core.bot.services.keyboards.user import kb_send
from app.core.bot.services.requests.user import manage_user
from app.core.database.models.user import User


async def handle_send(
    loc: Any,
    tg_id: int,
    event: Optional[Union[types.CallbackQuery, types.Message]],
) -> Optional[int]:
    """
    Обрабатывает состояние отправки финального сообщения с изображением.

    Проводит загрузку данных пользователя, генерирует код, создает изображение
    и отправляет финальное сообщение с закреплением.

    Args:
        loc (Any): Локализация с шаблонами сообщений.
        tg_id (int): Telegram ID пользователя.
        event (CallbackQuery | Message | None): Исходное событие,
            содержащее сообщение или callback.

    Returns:
        Optional[int]: Идентификатор отправленного сообщения, если успешно,
            иначе None.
    """
    # Универсальный способ извлечения сообщения
    if isinstance(event, types.CallbackQuery):
        message: Optional[types.MaybeInaccessibleMessageUnion] = (
            event.message
        )
    else:
        message = event

    # Если сообщение недоступно — прекращаем обработку
    if not message or not message.bot:
        return None

    # Получение пользователя из базы
    user: Union[User, bool, None, int] = await manage_user(
        tg_id=tg_id,
        action="get",
    )
    if not isinstance(user, User):
        return None

    # Генерация числового кода
    code: Optional[int] = generate_code(
        user_id=user.id,
        num_digits=3,
    )

    # Отображение анимации загрузки
    await message.bot.send_chat_action(
        chat_id=tg_id,
        action=ChatAction.UPLOAD_PHOTO,
    )

    try:
        # Генерация изображения кода
        buffer: BytesIO = await generate_image(str(code))

        # Формирование подписи к изображению
        part1: str
        part2: str
        part3: str
        part1, part2, part3 = loc.messages.template.send
        dt: datetime = datetime.strptime(
            f"{loc.event.date} {loc.event.time}", "%Y-%m-%d %H:%M:%S"
        )
        date_str: str = (
            f"{dt.day} {getattr(loc.months, str(dt.month - 1))} "
            f"{dt.year}, {dt.hour:02d}:{dt.minute:02d}"
        )

        caption: str = f"{part1}{code}{part2}{date_str}{part3}"

        # Отправка изображения пользователю
        msg: types.Message = await message.answer_photo(
            photo=types.BufferedInputFile(
                buffer.read(),
                filename="code.png",
            ),
            caption=caption,
            parse_mode="HTML",
            reply_markup=kb_send(loc.buttons),
        )

        # Закрепление отправленного сообщения
        await message.bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=msg.message_id,
        )

        return msg.message_id

    except BaseException:
        return None
