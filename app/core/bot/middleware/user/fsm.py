"""
Модуль для обновления данных FSM, включая локализацию,
объект пользователя и данные пользователя.
"""

from typing import Any, cast

from aiogram.fsm.context import FSMContext

from app.core.bot.services.localization import Localization, load_localization
from app.core.database import DataManager, User, UserManager, async_session


async def get_user_fsm(
    data: dict[str, Any],
    event: Any = None,
) -> tuple[User | None, dict[str, Any] | None]:
    """
    Обновляет FSM данные: user_db, data_db и локализацию.

    Если их нет в FSM, создаёт/загружает все данные сразу.
    Язык определяется из user_db (или по умолчанию "ru").
    """
    state: FSMContext | None = data.get("state")
    if state is None:
        raise ValueError("FSMContext не найден в data")

    fsm_data: dict[str, Any] = await state.get_data()

    # Ключи для FSM
    loc_key = "loc_user"
    user_key = "user_db"
    data_key = "data_db"

    # Проверяем, есть ли все данные
    user_db: User | None = cast(User | None, fsm_data.get(user_key))
    data_db: dict[str, Any] | None = fsm_data.get(data_key)
    loc: Localization | None = fsm_data.get(loc_key)

    # Если чего-то не хватает, загружаем всё вместе
    if not (user_db and data_db and loc):
        if not event:
            # Без event нельзя создать user_db и data_db
            return user_db, data_db

        bot_id: int = event.bot.id
        tg_id: int = event.from_user.id

        async with async_session() as session:
            user_manager = UserManager(session)
            data_manager = DataManager(session)

            # Загружаем или создаём пользователя
            user_db = await user_manager.get_or_create(tg_id=tg_id, bot_id=bot_id)
            # Загружаем данные пользователя
            data_db = await data_manager.dict_all(tg_id=tg_id, bot_id=bot_id)
            # Загружаем локализацию
            lang: str = user_db.lang if user_db else "ru"
            loc = await load_localization(lang=lang, role="user")

            # Обновляем FSM сразу всеми данными
            await state.update_data(**{
                user_key: user_db,
                data_key: data_db,
                loc_key: loc,
                "lang": lang
            })

    return user_db, data_db


async def clear_fsm_user(
    data: dict[str, Any]
) -> None:
    """
    Очищает данные FSM для пользователя.
    """

    state: FSMContext | None = data.get("state")
    if state is None:
        raise ValueError("FSMContext не найден в data")

    # Очищаем данные FSM
    await state.clear()
