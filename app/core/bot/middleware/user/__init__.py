"""
Пакет для обработки данных пользователя в базовом middleware Aiogram.
Содержит функции обновления FSM, загрузки локализации и подготовки
данных пользователя до вызова handler.
"""

from .fsm import fsm_data_user
from .process import user_before

__all__: list[str] = [
    "fsm_data_user",
    "user_before",
]
