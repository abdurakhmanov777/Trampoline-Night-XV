"""
Базовый middleware для обработки событий Aiogram.
"""

from datetime import datetime
from typing import Any, Awaitable, Callable, Literal

from aiogram import BaseMiddleware

from app.core.bot.middleware.user.fsm import clear_fsm_user
from app.core.bot.services.logger import log_error
from app.core.database import User

from . import utils
from .user.process import user_before


class MwBase(BaseMiddleware):
    """Базовый middleware для обработки событий Aiogram."""

    def __init__(
        self,
        delete_event: bool = False,
        role: Literal["user", "admin"] = "user",
        allowed_types: set[str] | None = None,
        **extra_data: Any,
    ) -> None:
        """
        Инициализация middleware.

        Parameters
        ----------
        delete_event : bool
            Флаг удаления исходного сообщения после обработки.
        role : Literal["user", "admin"]
            Роль для обработки (user или admin).
        allowed_types : set[str] | None
            Разрешённые типы сообщений.
        **extra_data : Any
            Дополнительные данные для передачи в handler.
        """
        self.delete_event: bool = delete_event
        self.role: Literal["user", "admin"] = role
        self.extra_data: dict[str, Any] = extra_data

        self.allowed: set[str] = {"text"}
        if allowed_types:
            self.allowed.update(allowed_types)

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """
        Обрабатывает событие и вызывает handler.

        Parameters
        ----------
        handler : Callable[[Any, dict[str, Any]], Awaitable[Any]]
            Асинхронная функция-обработчик события.
        event : Any | None
            Событие пользователя.
        data : dict[str, Any] | None
            Словарь данных для передачи в handler.

        Returns
        -------
        Any
            Результат работы handler или None.
        """
        if event is None or not getattr(event, "from_user", None):
            return None

        if not await utils.check_type(event, self.allowed):
            return None

        data = data or {}
        data.update(self.extra_data)

        user: User | None = None
        db: dict[str, str] | None = None
        msg_id: int = 0

        if self.role == "user":
            time1: datetime = datetime.now()
            user, db, msg_id = await user_before(data, event)
            time2: datetime = datetime.now()
            print(f"user_before time: {(time2 - time1).total_seconds()} sec")
        else:
            # Логика для админов будет добавлена позже
            pass

        try:
            result: Any = await handler(event, data)
            await utils.remove_event(event, self.delete_event)

        except Exception as error:
            await log_error(event, error=error)
            return None

        if self.role == "user":
            chat_id: Any = utils.get_message(event).chat.id
            if chat_id is not None:
                await utils.remove_old_msg(event, chat_id, msg_id)

            await utils.update_db(
                tg_id=event.from_user.id,
                bot_id=event.bot.id,
                user=user,
                data=db,
            )
            if user and int(user.state[-1]) >= 100:
                await clear_fsm_user(data)
        else:
            # Логика для админов будет добавлена позже
            pass

        return result
