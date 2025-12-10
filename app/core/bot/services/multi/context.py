"""
Модуль, содержащий класс контекста
для обработки состояния пользователя в боте.
"""

from dataclasses import dataclass
from typing import Any

from aiogram import types
from aiogram.fsm.context import FSMContext


@dataclass(slots=True)
class MultiContext:
    """Контекст, содержащий параметры для обработки состояния пользователя.

    Атрибуты:
        state (Any): Данные из временного хранилища FSMContext.
        loc (Any): Объект локализации, содержащий состояния пользователя.
        loc_state (Any): Текущие состояния локализации.
        value (str): Идентификатор текущего состояния.
        tg_id (int): Telegram ID пользователя.
        data (str | None): Дополнительные данные, переданные пользователем.
        event (types.CallbackQuery | types.Message | None):
            Событие Telegram, которое вызвало этот контекст.
    """
    state: FSMContext
    loc: Any
    loc_state: Any
    value: str = ""
    tg_id: int = 0
    data: str | None = None
    event: types.CallbackQuery | types.Message | None = None
