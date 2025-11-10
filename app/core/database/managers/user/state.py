"""
Управление стеком состояний пользователя.

Содержит методы для добавления, удаления и просмотра
состояний пользователя в виде стека.
"""

from typing import List, Optional

from app.core.database.models import User

from .crud import UserCRUD


class UserState(UserCRUD):
    """Менеджер состояний пользователя."""

    async def push_state(
        self,
        tg_id: int,
        new_state: str,
    ) -> bool:
        """
        Добавить новое состояние в стек пользователя.

        Args:
            tg_id (int): Telegram ID пользователя.
            new_state (str): Новое состояние для добавления.

        Returns:
            bool: True, если состояние добавлено, иначе False.
        """
        user: Optional[User] = await self.get(tg_id)
        if not user:
            # Пользователь не найден
            return False

        stack: List[str] = user.state.split(",") if user.state else []
        stack.append(new_state)
        user.state = ",".join(stack)

        # Сохраняем изменения в базе данных
        await self.session.commit()
        return True

    async def pop_state(
        self,
        tg_id: int,
    ) -> Optional[str]:
        """
        Извлечь последнее состояние из стека пользователя.

        Args:
            tg_id (int): Telegram ID пользователя.

        Returns:
            Optional[str]: Последнее состояние или None, если
                стек пустой или пользователь не найден.
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

    async def peek_state(
        self,
        tg_id: int,
    ) -> Optional[str]:
        """
        Посмотреть последнее состояние в стеке без удаления.

        Args:
            tg_id (int): Telegram ID пользователя.

        Returns:
            Optional[str]: Последнее состояние или None, если
                стек пустой или пользователь не найден.
        """
        user: Optional[User] = await self.get(tg_id)
        if not user:
            return None

        stack: List[str] = user.state.split(",") if user.state else []
        return stack[-1] if stack else None
