"""
Модуль обработки финального состояния пользователя,
формирования итогового сообщения и клавиатуры.
"""

from typing import Any, Dict, Tuple

from aiogram.types import InlineKeyboardMarkup

from app.core.bot.services.keyboards.user import kb_end
from app.core.bot.services.multi.context import MultiContext
from app.core.bot.services.requests.data.dlist import manage_data_list


async def handle_end(
    ctx: MultiContext,
) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Обрабатывает состояние пользователя и формирует сообщение.

    Формирует текст на основе шаблона локализации и списка данных,
    собранных от пользователя.

    Args:
        ctx (MultiContext): Контекст с параметрами обработки.

    Returns:
        Tuple[str, InlineKeyboardMarkup]: Сообщение и клавиатура.
    """

    # Получаем список всех данных пользователя
    data_list: Dict[str, Any] = await manage_data_list(tg_id=ctx.tg_id)

    # Формируем текст блоков данных
    items_text: str = "\n\n".join(
        f"🔹️ {key}: {value}" for key, value in data_list.items()
    )

    # Получаем шаблон локализации для начала и конца сообщения
    p1: str
    p2: str
    p1, p2 = ctx.loc.template.end

    text_message: str = f"{p1}{items_text}{p2}"

    # Формируем клавиатуру завершения
    keyboard: InlineKeyboardMarkup = kb_end(buttons=ctx.loc.button)

    return text_message, keyboard
