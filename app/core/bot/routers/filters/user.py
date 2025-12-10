"""Фильтр callback-запросов, содержащих подстроку 'user{SYMB}'.

Модуль определяет фильтр для обработки callback-запросов, в которых
данные содержат подстроку 'user{SYMB}'. Используется в маршрутах Aiogram.
"""

from typing import Any, Union

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from app.config.settings import SYMB


class CallbackNextFilter(BaseFilter):
    """Фильтр для callback-запросов, содержащих подстроку 'user{SYMB}'.

    Если `callback.data` содержит подстроку 'user{SYMB}', фильтр возвращает
    словарь с этой подстрокой без префикса 'user{SYMB}' для передачи в роутер.
    Иначе возвращает False.
    """

    async def __call__(
        self,
        callback: CallbackQuery,
    ) -> Union[dict[str, Any], bool]:
        """Проверить наличие подстроки 'user{SYMB}' в данных запроса.

        Parameters
        ----------
        callback : CallbackQuery
            Объект callback-запроса, полученный от пользователя.

        Returns
        -------
        Union[dict[str, Any], bool]
            Словарь с ключом 'user{SYMB}data',
                содержащим подстроку после 'user{SYMB}',
            если подстрока 'user{SYMB}' найдена, иначе False.
        """
        if not callback.data or f"user{SYMB}" not in callback.data:
            return False

        user_values: list[str] = callback.data.split(SYMB)[1:]

        return {"value": user_values}
