from typing import Any, Literal, Optional

from app.core.database.engine import async_session
from app.core.database.managers import UserManager


async def manage_user_state(
    tg_id: int,
    action: Literal[
        "push",
        "pop",
        "peek",
        "peekpush",
        "popeek",
        "clear",
        "get_state",
    ] = "peek",
    new_state: Optional[str] = None,
) -> Optional[Any]:
    """
    Универсальная обёртка для работы со стеком состояний пользователя.
    """
    async with async_session() as session:
        manager = UserManager(session)
        if action in ("push", "peekpush") and new_state is None:
            raise ValueError(
                f"Для действия '{action}' необходимо указать new_state.")

        if action == "push":
            assert new_state is not None  # явно гарантируем тип
            return await manager.push_state(tg_id, new_state)

        elif action == "peekpush":
            assert new_state is not None  # явно гарантируем тип
            current: str | None = await manager.peek_state(tg_id)
            await manager.push_state(tg_id, new_state)
            return current

        elif action == "pop":
            return await manager.pop_state(tg_id)

        elif action == "peek":
            return await manager.peek_state(tg_id)

        elif action == "popeek":
            last = await manager.pop_state(tg_id)
            return await manager.peek_state(tg_id) or last

        elif action == "clear":
            await manager.clear_state(tg_id)  # если есть метод clear_state
            return True

        elif action == "get_state":
            states = await manager.get_state(tg_id)
            return states or ["1"]

        raise ValueError(f"Неизвестное действие: {action!r}")
