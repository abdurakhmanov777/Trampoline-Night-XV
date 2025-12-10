"""
Обработка данных пользователя для базового middleware Aiogram.
"""

from typing import Any, Dict, Optional, Tuple

from app.core.database import User

from .fsm import fsm_data_user


async def user_before(
    data: Dict[str, Any],
    event: Any
) -> Tuple[Optional[User], Optional[Dict[str, str]], int]:
    """
    Логика до вызова handler для role=user.

    Parameters
    ----------
    data : Dict[str, Any]
        Словарь данных пользователя.
    event : Any
        Событие пользователя.

    Returns
    -------
    Tuple[Optional[User], Optional[Dict[str, str]], int]
        Кортеж из:
        - экземпляра пользователя или None,
        - словаря данных пользователя или None,
        - идентификатора предыдущего сообщения.
    """
    user: Optional[User]
    db: Optional[Dict[str, str]]
    user, db = await fsm_data_user(data=data, event=event)
    msg_id: int = user.msg_id_other if user else 0
    return user, db, msg_id
