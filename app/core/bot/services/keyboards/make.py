"""
Модуль для формирования inline-клавиатур Telegram-бота.

Содержит функции для создания отдельных кнопок и клавиатур
с возможностью размещения кнопок в нескольких рядах.
Клавиатуры могут использоваться для навигации ("Далее", "Назад")
или выбора опций различной длины.

Функции:
    - make_button(text, callback_data):
        Создаёт отдельную кнопку.
    - make_keyboard(button_rows):
        Формирует InlineKeyboardMarkup из списка строк кнопок.
"""

from typing import List

from aiogram import types


def make_button(
    text: str,
    callback_data: str
) -> types.InlineKeyboardButton:
    """Создаёт кнопку с заданным текстом и callback_data.

    Args:
        text (str): Текст кнопки.
        callback_data (str): Callback data кнопки.

    Returns:
        types.InlineKeyboardButton: Объект кнопки для InlineKeyboardMarkup.
    """
    return types.InlineKeyboardButton(text=text, callback_data=callback_data)


def make_keyboard(
    button_rows: List[List[types.InlineKeyboardButton]]
) -> types.InlineKeyboardMarkup:
    """Создаёт InlineKeyboardMarkup из списка строк кнопок.

    Args:
        button_rows (List[List[types.InlineKeyboardButton]]): Строки кнопок.

    Returns:
        types.InlineKeyboardMarkup: Сформированная клавиатура.
    """
    return types.InlineKeyboardMarkup(inline_keyboard=button_rows)
