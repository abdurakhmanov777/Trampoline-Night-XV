"""
Модуль обработки финального состояния пользователя.

Предоставляет функцию `handler_submit`, которая формирует итоговое сообщение
пользователю на основе сохранённых данных, шаблонов локализации и
клавиатуры завершения.
"""

from typing import Any, Dict, List, Tuple

from aiogram.types import InlineKeyboardMarkup, LinkPreviewOptions

from app.core.bot.services.keyboards.user import kb_payment
from app.core.bot.services.multi.context import MultiContext
from app.core.bot.services.requests.data import manage_data_list
from app.core.bot.services.requests.user import manage_user_state


async def handler_payment(
    ctx: MultiContext,
) -> Tuple[str, InlineKeyboardMarkup, LinkPreviewOptions]:
    """
    Формирует итоговое сообщение пользователя по завершении сценария.

    Получает список состояний пользователя, отбирает те, которые содержат
    данные, загружает соответствующие значения и формирует финальный блок
    текста с учётом шаблонов локализации.

    Args:
        ctx (MultiContext): Контекст шага многошагового сценария, включающий
            локализацию, ID пользователя и связанные данные.

    Returns:
        Tuple[str, InlineKeyboardMarkup, LinkPreviewOptions]:
            Итоговое сообщение, финальная клавиатура и настройки предпросмотра.
    """
    states: bool | str | List[str] | None = await manage_user_state(
        tg_id=ctx.tg_id,
        action="get_state",
    )

    if not isinstance(states, list):
        raise ValueError(
            f"Некорректный формат состояний пользователя: {states!r}"
        )

    loc: Any = ctx.loc

    text_message: str = loc.messages.payment

    # Создаём финальную клавиатуру
    keyboard: InlineKeyboardMarkup = kb_payment(
        buttons=loc.buttons
    )

    opts: LinkPreviewOptions = LinkPreviewOptions(is_disabled=True)

    return text_message, keyboard, opts
