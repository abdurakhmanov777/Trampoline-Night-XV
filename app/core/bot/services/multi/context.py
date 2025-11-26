"""
Модуль маршрутизации формирования сообщений и клавиатур
для пользователя на основе локализации и состояния.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from aiogram import types


@dataclass
class MultiContext:
    """
    Контекст, содержащий параметры для обработки состояния пользователя.
    """

    loc: Any
    loc_state: Any
    value: str
    tg_id: int
    data: str | None = None
    event: Optional[types.MaybeInaccessibleMessageUnion] = None
    extra: Dict[str, Any] | None = None
