"""
Вспомогательные функции для базового middleware Aiogram.
"""

from typing import Any

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


def get_message(
    event: Any
) -> Message:
    if isinstance(event, Message):
        return event
    else:
        return getattr(event, "message")


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
    tg_id: int,
    bot_id: int,
    user: User | None,
    data: dict[str, str] | None,
) -> None:
    """
    Обновляет User и Data в БД при необходимости.

    Parameters
    ----------
    user : User | None
        Экземпляр пользователя.
    data : dict[str, str] | None
        Данные пользователя.
    tg_id : int
        Идентификатор пользователя.
    """
    if user and data is not None:
        async with async_session() as session:
            await UserManager(session).update_user(
                user=user
            )
            await DataManager(session).update_all(
                tg_id=tg_id,
                bot_id=bot_id,
                new_data=data
            )
