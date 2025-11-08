from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware

from app.database.models.user import User
from app.filters import AdminFilter
from app.services.localization import load_localization_main
from app.services.requests.requests import get_user_by_tg_id
from app.utils.logger import log_error

# Временный список администраторов для демонстрации
TEMP_ADMINS: list[int] = [111111111, 1645736584]


async def update_language_data(
    data: dict,
    event: Optional[Any] = None,
) -> None:
    """
    Обновление языковых данных пользователя.

    Проверяет наличие данных о языке в состоянии пользователя,
    при отсутствии берет язык из БД или устанавливает 'ru' по умолчанию.

    Args:
        data (dict): Словарь данных хэндлера.
        event (Optional[Any]): Событие от Telegram.
    """
    state: Any = data.get("state")
    if not state:
        return

    user_data: dict = await state.get_data()

    # Если языковые данные уже есть, ничего не делаем
    if "loc" in user_data:
        return

    lang: str = "ru"
    if event:
        tg_id: Optional[int] = getattr(event.from_user, "id", None)
        user: Optional[User] = (
            await get_user_by_tg_id(tg_id) if tg_id else None
        )
        if user and user.lang:
            lang = user.lang

    await state.update_data(
        lang=lang,
        loc=await load_localization_main(lang),
    )


class MwBase(BaseMiddleware):
    """
    Базовый middleware для Aiogram.

    Поддерживает:
    - подсчет вызовов хэндлера,
    - удаление события после обработки,
    - передачу дополнительных параметров в data,
    - автоматическую проверку роли администратора.
    """

    def __init__(
        self,
        delete_event: bool = False,
        **extra_data: Any,
    ) -> None:
        """
        Инициализация middleware.

        Args:
            delete_event (bool): Удалять ли событие после обработки.
            **extra_data: Любые дополнительные параметры для data.
        """
        self.counter: int = 0
        self.delete_event: bool = delete_event
        self.extra_data: Dict[str, Any] = extra_data

    async def __call__(
        self,
        handler: Callable[[Any, dict], Awaitable[Any]],
        event: Optional[Any] = None,
        data: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Основной метод middleware.

        Args:
            handler (Callable): Хэндлер события.
            event (Optional[Any]): Событие от Telegram.
            data (Optional[dict]): Словарь данных хэндлера.

        Returns:
            Любой результат работы хэндлера.
        """
        data = data or {}
        self.counter += 1
        data["counter"] = self.counter

        # Добавляем дополнительные параметры в data
        data.update(self.extra_data)

        # Обновляем языковые данные пользователя
        await update_language_data(data, event)

        # Проверяем роль администратора и добавляем в data
        if event:
            role: Dict[str, Any] | bool = await AdminFilter()(event)
            data["admin_role"] = role

        try:
            result: Any = await handler(event, data)
            # Удаляем событие, если нужно
            if self.delete_event and event is not None and hasattr(
                event, "delete"
            ):
                try:
                    await event.delete()
                except Exception:
                    pass
            return result
        except Exception as e:
            await log_error(event, error=e)


# ---------------- Алиасы middleware ----------------

def MwCommand(**extra_data: Any) -> MwBase:
    """
    Middleware для команд.

    Удаляет событие после обработки.
    """
    return MwBase(delete_event=True, **extra_data)


def MwMessage(**extra_data: Any) -> MwBase:
    """
    Middleware для сообщений.

    Удаляет событие после обработки.
    """
    return MwBase(delete_event=True, **extra_data)


def MwCallback(**extra_data: Any) -> MwBase:
    """
    Middleware для callback query.

    Не удаляет событие после обработки.
    """
    return MwBase(delete_event=False, **extra_data)
