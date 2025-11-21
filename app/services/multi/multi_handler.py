"""
Модуль для формирования текстового сообщения и клавиатуры на основе
локализации пользователя и типа состояния.
"""

import re
from typing import Any, Tuple

from aiogram.types import InlineKeyboardMarkup

from app.services.keyboards.user import kb_input, kb_select, kb_text
from app.services.requests.data.crud import manage_data
from app.utils.morphology.casing import lower_words
from app.utils.morphology.inflection import inflect_text


async def multi(
    loc: Any,
    value: str,
    tg_id: int,
    data: str | None = None
) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Формирует текст сообщения и соответствующую клавиатуру для пользователя.

    Args:
        loc (Any): Объект локализации с состояниями пользователя.
        value (str): Ключ состояния пользователя.

    Returns:
        Tuple[str, InlineKeyboardMarkup]: Текст сообщения и объект клавиатуры.
    """
    loc_state: Any = getattr(loc, f"userstate_{value}")
    type_message: str = loc_state.type
    base_text: str = loc_state.text
    keyboard: Any = loc_state.keyboard

    if type_message == "text":
        text_message: str = base_text
        keyboard_message: InlineKeyboardMarkup = await kb_text(
            state=keyboard,
            backstate=value
        )

    elif type_message == "input":
        format_: str = loc_state.format
        pattern: Any = loc_state.pattern
        template: Any = loc.template.input
        error = False
        if data is not None:
            regex: re.Pattern[Any] = re.compile(pattern)
            if regex.fullmatch(data):
                data = await manage_data(
                    tg_id=tg_id,
                    action="create_or_update",
                    key=base_text,
                    value=data
                )
            else:
                error = True
        else:
            data = await manage_data(
                tg_id=tg_id,
                action="get",
                key=base_text
            )

        flag = False
        if error:
            error_parts: Tuple[str, str] = template.error
            text_message = f"{error_parts[0]}{format_}{error_parts[1]}"

        elif not data:
            start_parts: Tuple[str, str, str] = template.start
            edit_base_text: str = await inflect_text(
                text=await lower_words(
                    text=base_text,
                    capitalize_first=False
                ),
                case='винительный'
            )
            text_message = (
                f"{start_parts[0]}{edit_base_text}{start_parts[1]}"
                f"{format_}{start_parts[2]}"
            )

        else:
            flag = True
            saved_parts: Tuple[str, str, str] = template.saved
            text_message = (
                f"{saved_parts[0]}{base_text}{saved_parts[1]}"
                f"{data}{saved_parts[2]}"
            )

        keyboard_message: InlineKeyboardMarkup = await kb_input(
            state=keyboard,
            backstate=value,
            show_next=flag
        )

    else:
        select_parts: Tuple[str, str] = loc.template.select
        text_message: str = f"{select_parts[0]}{base_text}{select_parts[1]}"
        keyboard_message: InlineKeyboardMarkup = await kb_select(
            data=keyboard
        )

    return text_message, keyboard_message
