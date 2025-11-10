"""
Базовый класс менеджера пользователей.
"""

from sqlalchemy.ext.asyncio import AsyncSession


class UserManagerBase:
    """Базовый класс для работы с таблицей User."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализация менеджера пользователей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
        """
        self.session: AsyncSession = session
