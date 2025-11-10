"""
Базовый класс менеджера данных.
"""

from sqlalchemy.ext.asyncio import AsyncSession


class DataManagerBase:
    """Базовый менеджер для работы с таблицей Data."""

    def __init__(
        self,
        session: AsyncSession
    ) -> None:
        """
        Инициализация менеджера.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
        """
        self.session: AsyncSession = session
