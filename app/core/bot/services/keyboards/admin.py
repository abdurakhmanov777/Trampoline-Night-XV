"""
Модуль для формирования инлайн-клавиатур Telegram-бота.

Содержит функции для генерации клавиатур с кнопками "Далее", "Назад"
и выбора из списка опций различной длины.
"""


from aiogram import types

from .make import make_button, make_keyboard


def kb_delete(
) -> types.InlineKeyboardMarkup:
    """Создаёт клавиатуру с кнопкой 'Закрыть окно'.

    Args:
        buttons (Any): Объект локализации с текстами кнопок.

    Returns:
        types.InlineKeyboardMarkup: Сформированная клавиатура.
    """
    return make_keyboard([[make_button("Удалить", "delete")]])
