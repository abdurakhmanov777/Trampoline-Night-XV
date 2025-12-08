"""
Модуль содержит базовый middleware для обработки событий Aiogram.

Middleware выполняет фильтрацию типов сообщений, подсчёт вызовов,
удаление событий, проверку роли пользователя, обновление данных FSM и БД,
а также удаление сообщений неподдерживаемых типов.
"""

from typing import Any, Awaitable, Callable, Dict, Literal, Optional, Set

from aiogram import BaseMiddleware
from aiogram.types import ContentType, Message

from app.core.bot.services.logger import log_error
from app.core.database import DataManager, User, UserManager, async_session

from .refresh import refresh_data_user


class MwBase(BaseMiddleware):
    """
    Базовый middleware для обработки событий Aiogram.
    """

    def __init__(
        self,
        delete_event: bool = False,
        role: Literal["user", "admin"] = "user",
        allowed_types: Optional[Set[str]] = None,
        **extra_data: Any,
    ) -> None:
        self.delete_event: bool = delete_event
        self.role: Literal["user", "admin"] = role
        self.extra_data: Dict[str, Any] = extra_data

        self.allowed_types: Set[str] = {ContentType.TEXT}
        if allowed_types:
            self.allowed_types.update(allowed_types)

    # ------------------------------
    # ВЫНЕСЕННЫЕ ЧАСТИ ЛОГИКИ
    # ------------------------------

    async def _filter_types(
        self,
        event: Any
    ) -> bool:
        """Возвращает True, если событие разрешено, иначе удаляет и возвращает False."""
        if isinstance(
            event,
            Message
        ) and event.content_type not in self.allowed_types:
            try:
                await event.delete()
            except Exception:
                pass
            return False
        return True

    def _prepare_data(
        self,
        data: Dict[str, Any]
    ) -> None:
        """Добавляет extra_data в data."""
        data.update(self.extra_data)

    async def _process_user_before(
        self,
        data: Dict[str, Any],
        event: Any
    ) -> tuple[Optional[User], Optional[Dict[str, str]], int]:
        """Логика, выполняемая ДО вызова handler для role=user."""
        user_db: User | None
        data_db: Dict[str, str] | None
        user_db, data_db = await refresh_data_user(
            data=data,
            event=event,
            role=self.role,
        )
        msg_id: int = user_db.msg_id_other if user_db else 0
        return user_db, data_db, msg_id

    async def _delete_event(
        self,
        event: Any
    ) -> None:
        """Удаление сообщения, если delete_event=True."""
        if not self.delete_event:
            return
        try:
            await event.delete()
        except Exception:
            pass

    def _extract_chat_id(
        self,
        event: Any
    ) -> Optional[int]:
        """Извлекает chat_id для user post-processing."""
        if isinstance(event, Message):
            return event.chat.id

        msg: Any | None = getattr(event, "message", None)
        if isinstance(msg, Message):
            return msg.chat.id

        return None

    async def _cleanup_old_message(
        self,
        event: Any,
        chat_id: int,
        msg_id: int
    ) -> None:
        """Удаляет старое сообщение msg_id."""
        if msg_id and event.bot:
            try:
                await event.bot.delete_message(chat_id, msg_id)
            except Exception:
                pass

    async def _update_db_if_needed(
        self,
        user_db: Optional[User],
        data_db: Optional[Dict[str, str]],
        user_id: int,
    ) -> None:
        """Обновляет User и Data в БД."""
        if user_db and data_db is not None:
            async with async_session() as session:
                await UserManager(session).update_user(user_db)
                await DataManager(session).update_all(user_id, data_db)

    # ------------------------------
    # ОСНОВНОЙ МЕТОД
    # ------------------------------

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Optional[Any] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:

        if event is None or not event.from_user:
            return

        # Фильтрация типов сообщений
        if not await self._filter_types(event):
            return None

        data = data or {}
        self._prepare_data(data)

        user_db: User | None = None
        data_db: Dict[str, str] | None = None
        msg_id: int = 0

        # ------------------------------
        # ЛОГИКА ДЛЯ ПОЛЬЗОВАТЕЛЯ (до handler)
        # ------------------------------
        if self.role == "user":
            user_db, data_db, msg_id = await self._process_user_before(
                data, event
            )

        # ------------------------------
        # ВЫЗОВ handler
        # ------------------------------
        try:
            result: Any = await handler(event, data)
            await self._delete_event(event)

        except Exception as error:
            await log_error(event, error=error)
            return None

        # ------------------------------
        # ЛОГИКА ДЛЯ ПОЛЬЗОВАТЕЛЯ (после handler)
        # ------------------------------
        if self.role == "user":
            chat_id: int | None = self._extract_chat_id(event)

            if chat_id is not None:
                await self._cleanup_old_message(event, chat_id, msg_id)

            await self._update_db_if_needed(
                user_db=user_db,
                data_db=data_db,
                user_id=event.from_user.id,
            )

        return result
