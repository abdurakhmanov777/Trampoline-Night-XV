"""
Управление стеком состояний пользователя.
"""

from typing import List, Optional

from app.core.database.models import User

from .crud import UserCRUD


class UserState(UserCRUD):
    """Менеджер состояний пользователя."""

    async def push_state(self, tg_id: int, new_state: str) -> bool:
        """
        Добавить новое состояние в стек пользователя.
        """
        user: Optional[User] = await self.get(tg_id)
        if not user:
            return False

        stack: List[str] = user.state.split(",") if user.state else []
        stack.append(new_state)
        user.state = ",".join(stack)
        await self.session.commit()
        return True

    async def pop_state(self, tg_id: int) -> Optional[str]:
        """
        Извлечь последнее состояние из стека пользователя.
        """
        user: Optional[User] = await self.get(tg_id)
        if not user:
            return None

        stack: List[str] = user.state.split(",") if user.state else []
        if not stack:
            return None

        last_state: str = stack.pop()
        user.state = ",".join(stack)
        await self.session.commit()
        return last_state

    async def peek_state(self, tg_id: int) -> Optional[str]:
        """
        Посмотреть последнее состояние в стеке без удаления.
        """
        user: Optional[User] = await self.get(tg_id)
        if not user:
            return None

        stack: List[str] = user.state.split(",") if user.state else []
        return stack[-1] if stack else None
