from typing import Optional

from aiogram import types


def kb_text_or_input(
    state: str,
    backstate: str
) -> types.InlineKeyboardMarkup:
    """
    Формирует InlineKeyboardMarkup с кнопкой "Далее" и условной кнопкой "Назад".

    Args:
        state (str): Текущее состояние пользователя.
        backstate (Optional[str]): Предыдущее состояние (для кнопки "Назад").

    Returns:
        types.InlineKeyboardMarkup: Объект клавиатуры с кнопками.
    """
    keyboard_buttons: list[list[types.InlineKeyboardButton]] = [
        [types.InlineKeyboardButton(
            text="Далее" if backstate != "1" else "Соглашаюсь",
            callback_data=f"userstate_{state}"
        )]
    ]
    print(backstate, state)
    if backstate != "1":
        keyboard_buttons.append(
            [types.InlineKeyboardButton(
                text="Назад",
                callback_data=f"backstate_{backstate}"
            )]
        )

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def kb_input(
    state: str
) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Далее" if state == "1" else "Соглашаюсь",
                callback_data=f"userstate_{state}"
            )
        ]]
    )
