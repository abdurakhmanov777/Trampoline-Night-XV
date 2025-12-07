"""
Управление стеком состояний пользователя.

Работает с user.state как со списком,
а в БД хранится строка (user._state).
"""

from typing import List, Optional

from app.core.database.models import User

from .crud import UserCRUD


class UserState(UserCRUD):
    """Менеджер состояний пользователя."""

    async def push_state(self, tg_id: int, new_state: str) -> bool:
        """
        Добавить новое состояние в стек (в конец списка).
        """
        user: User = await self.get_or_create(tg_id)

        stack = user.state       # <-- уже список
        stack.append(new_state)

        user.state = stack       # setter сам превратит список в строку
        await self.session.commit()
        return True

    async def pop_state(self, tg_id: int) -> Optional[str]:
        """
        Извлечь последнее состояние (pop).
        """
        user: User = await self.get_or_create(tg_id)

        stack = user.state
        if not stack:
            return None

        last_state = stack.pop()

        user.state = stack
        await self.session.commit()
        return last_state

    async def peek_state(self, tg_id: int) -> Optional[str]:
        """
        Посмотреть последнее состояние без удаления.
        """
        user: User = await self.get_or_create(tg_id)
        stack = user.state

        return stack[-1] if stack else None

    async def get_state(self, tg_id: int) -> List[str]:
        """
        Получить весь список состояний.
        """
        user: User = await self.get_or_create(tg_id)
        return user.state

    async def clear_state(self, tg_id: int) -> bool:
        """
        Сбросить состояние до ["1"].
        """
        user: User = await self.get_or_create(tg_id)

        user.state = ["1"]       # setter → "_state='1'"
        await self.session.commit()
        return True
