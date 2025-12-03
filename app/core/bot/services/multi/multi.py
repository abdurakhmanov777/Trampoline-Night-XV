"""
Модуль маршрутизации генерации сообщений и клавиатур для пользователя
на основе локализации и текущего состояния.

Предоставляет функцию `multi`, которая определяет обработчик шага,
создаёт контекст выполнения и возвращает параметры сообщения для Telegram.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from aiogram import types

from app.core.bot.services.requests.data import manage_data

from .context import MultiContext
from .handlers.end import handle_end
from .handlers.input import handle_input
from .handlers.select import handle_select
from .handlers.start import handle_start
from .handlers.text import handle_text

#: Таблица стандартных обработчиков по типу состояния.
HANDLERS: Dict[str, Callable[[MultiContext], Any]] = {
    "input": handle_input,
    "select": handle_select,
    "text": handle_text,
}

#: Таблица обработчиков для специальных состояний.
SPECIAL_HANDLERS: Dict[str, Callable[[MultiContext], Any]] = {
    "1": handle_start,
    "99": handle_end,
}


async def multi(
    loc: Any,
    value: str,
    tg_id: int,
    data: Optional[str] = None,
    data_select: Optional[List[str]] = None,
    event: Optional[
        Union[types.CallbackQuery, types.Message]
    ] = None,
) -> Tuple[
    str,
    types.InlineKeyboardMarkup,
    types.LinkPreviewOptions,
]:
    """
    Формирует параметры ответа Telegram на основе состояния пользователя.

    Функция определяет, какой обработчик шага вызвать, подготавливает
    контекст и возвращает сообщение, клавиатуру и параметры предпросмотра.

    Args:
        loc (Any):
            Объект локализации, содержащий состояние пользователя.
        value (str):
            Текущее значение состояния пользователя.
        tg_id (int):
            Telegram ID пользователя.
        data (Optional[str]):
            Дополнительные данные, переданные пользователем.
        data_select (Optional[List[str]]):
            Пара ключ–значение для сохранения в хранилище данных.
        event (Optional[Union[CallbackQuery, Message]]):
            Telegram событие (сообщение или callback).

    Returns:
        Tuple[str, InlineKeyboardMarkup, LinkPreviewOptions]:
            Текст сообщения, клавиатура и параметры предпросмотра ссылок.
    """

    # Пытаемся получить обработчик для специальных состояний.
    handler: Optional[Callable[[MultiContext], Any]] = (
        SPECIAL_HANDLERS.get(value)
    )
    loc_state: Optional[Any] = None

    if handler is None:
        # Получаем состояние локализации и определяем обработчик.
        loc_state = getattr(loc, f"userstate_{value}")
        assert loc_state is not None
        handler = HANDLERS.get(
            loc_state.type,
            handle_start,
        )

    context: MultiContext = MultiContext(
        loc=loc,
        loc_state=loc_state,
        value=value,
        tg_id=tg_id,
        data=data,
        event=event,
    )

    # Сохраняем выбранные данные, если они переданы.
    if data_select:
        key: str = data_select[0]
        value_to_store: str = data_select[1]

        await manage_data(
            tg_id=tg_id,
            action="create_or_update",
            key=key,
            value=value_to_store,
        )

    return await handler(context)
