"""
Вспомогательные функции для базового middleware Aiogram.
"""

from typing import Any, Dict, Optional

from aiogram.types import Message

from app.core.database import DataManager, User, UserManager, async_session


async def check_type(
    event: Any,
    allowed: set[str]
) -> bool:
    """
    Проверяет тип события и удаляет неподдерживаемые сообщения.

    Parameters
    ----------
    event : Any
        Событие для проверки.
    allowed : set[str]
        Разрешённые типы сообщений.

    Returns
    -------
    bool
        True, если событие разрешено, иначе False.
    """
    if isinstance(event, Message) and event.content_type not in allowed:
        try:
            await event.delete()
        except Exception:
            pass
        return False
    return True


def get_chat_id(
    event: Any
) -> Optional[int]:
    """
    Извлекает chat_id для последующей обработки.

    Parameters
    ----------
    event : Any
        Событие пользователя.

    Returns
    -------
    Optional[int]
        Идентификатор чата или None.
    """
    if isinstance(event, Message):
        return event.chat.id
    msg: Any = getattr(event, "message", None)
    if isinstance(msg, Message):
        return msg.chat.id
    return None


async def remove_old_msg(
    event: Any,
    chat_id: int,
    msg_id: int
) -> None:
    """
    Удаляет старое сообщение по msg_id.

    Parameters
    ----------
    event : Any
        Событие пользователя.
    chat_id : int
        Идентификатор чата.
    msg_id : int
        Идентификатор старого сообщения.
    """
    if msg_id and event.bot:
        try:
            await event.bot.delete_message(chat_id, msg_id)
        except Exception:
            pass


async def remove_event(
    event: Any,
    flag: bool
) -> None:
    """
    Удаляет сообщение, если flag=True.

    Parameters
    ----------
    event : Any
        Событие для удаления.
    flag : bool
        Флаг необходимости удаления.
    """
    if not flag:
        return
    try:
        await event.delete()
    except Exception:
        pass


async def update_db(
    user_id: int,
    user: Optional[User],
    data: Optional[Dict[str, str]],
) -> None:
    """
    Обновляет User и Data в БД при необходимости.

    Parameters
    ----------
    user : Optional[User]
        Экземпляр пользователя.
    data : Optional[Dict[str, str]]
        Данные пользователя.
    user_id : int
        Идентификатор пользователя.
    """
    if user and data is not None:
        async with async_session() as session:
            await UserManager(session).update_user(user)
            await DataManager(session).update_all(user_id, data)
