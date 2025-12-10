"""
Обработка данных пользователя для базового middleware Aiogram.
"""

from typing import Any

from app.core.database import User

from .fsm import get_user_fsm


async def user_before(
    data: dict[str, Any],
    event: Any
) -> tuple[User | None, dict[str, str] | None, int]:
    """
    Логика до вызова handler для role=user.

    Parameters
    ----------
    data : dict[str, Any]
        Словарь данных пользователя.
    event : Any
        Событие пользователя.

    Returns
    -------
    tuple[User | None, dict[str, str]  | None, int]
        Кортеж из:
        - экземпляра пользователя или None,
        - словаря данных пользователя или None,
        - идентификатора предыдущего сообщения.
    """
    user: User | None
    db: dict[str, str] | None
    user, db = await get_user_fsm(data=data, event=event)
    msg_id: int = user.msg_id_other if user else 0
    return user, db, msg_id
