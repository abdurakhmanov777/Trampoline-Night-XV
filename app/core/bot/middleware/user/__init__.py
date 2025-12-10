"""
Пакет для обработки данных пользователя в базовом middleware Aiogram.
Содержит функции обновления FSM, загрузки локализации и подготовки
данных пользователя до вызова handler.
"""

from .fsm import clear_fsm_user, get_user_fsm
from .process import user_before

__all__: list[str] = [
    "clear_fsm_user",
    "get_user_fsm",
    "user_before",
]
