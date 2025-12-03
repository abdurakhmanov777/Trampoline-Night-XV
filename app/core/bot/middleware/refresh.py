"""
Модуль для обновления данных FSM пользователя или администратора.

Обеспечивает асинхронную загрузку локализации и обновление данных
в состоянии хэндлера.
"""

from typing import Any, Dict, Literal, Optional

from app.core.bot.services.localization import Localization, load_localization
from app.core.database import async_session
from app.core.database.managers import UserManager
from app.core.database.models import User


async def refresh_fsm_data(
    data: Dict[str, Any],
    event: Optional[Any] = None,
    role: Literal["user", "admin"] = "user",
) -> None:
    """
    Обновляет данные FSM, включая локализацию для пользователя или
    администратора.

    Локализация загружается только если её ещё нет в состоянии FSM.
    Для пользователей язык определяется из базы данных, для админов
    используется язык по умолчанию.

    Args:
        data (Dict[str, Any]): Словарь данных хэндлера FSM.
        event (Optional[Any]): Событие от Telegram.
        role (Literal["user", "admin"]): Роль пользователя для загрузки
            локализации.
    """
    state: Any = data.get("state")
    if not state:
        return

    key: str = f"loc_{role}"

    # Проверяем наличие локализации в состоянии, чтобы избежать повторной
    # загрузки
    user_data: Dict[str, Any] = await state.get_data()
    if key in user_data:
        return

    async def _get_language() -> str:
        """
        Определяет язык пользователя или возвращает язык по умолчанию.

        Returns:
            str: Язык пользователя.
        """
        if role == "admin":
            return "ru"

        lang: str = "ru"
        if event:
            tg_id: Optional[int] = getattr(event.from_user, "id", None)
            if tg_id:
                async with async_session() as session:
                    user_manager: UserManager = UserManager(session)
                    user: Optional[User] = await user_manager.get(tg_id)
                    if user:
                        lang = user.lang
        return lang

    # Определяем язык и загружаем локализацию
    lang: str = await _get_language()
    loc: Localization = await load_localization(
        language=lang,
        role=role
    )

    # Обновляем данные FSM новым объектом локализации и языком
    await state.update_data(**{
        key: loc,
        "lang": lang
    })
