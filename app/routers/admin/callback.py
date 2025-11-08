from typing import Any, Callable

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.services.keyboards as kb
from app.filters import AdminFilter, ChatTypeFilter
from app.utils.logger import log

router = Router()


def admin_callback(
    *filters: Any
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для обработки коллбеков в приватных чатах.
    Добавляет фильтр ChatTypeFilter(chat_type=["private"]) и
    фильтр администратора.

    Args:
        *filters (Any): Дополнительные фильтры для callback_query.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]:
        Декоратор для обработчика коллбека.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        return router.callback_query(
            ChatTypeFilter(chat_type=["private"]),
            AdminFilter(),
            *filters
        )(func)

    return decorator


# --- Пример существующего callback ---
@admin_callback(F.data == 'delete_panel')
async def delete_panel(
    callback: CallbackQuery
) -> None:
    """
    Удаляет сообщение в чате и логирует вызов.

    Args:
        callback (CallbackQuery): объект коллбека
    """
    if isinstance(callback.message, Message):
        await callback.message.delete()

    await log(callback)


# Обработчик основного меню админа
@admin_callback()
async def main(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """
    Основной обработчик коллбеков админ-панели.
    Берёт текст и клавиатуру из локализации и редактирует
    сообщение.

    Args:
        callback (CallbackQuery): объект коллбека
        state (FSMContext): контекст FSM для хранения данных
    """
    if not isinstance(callback.message, Message):
        return

    data: dict = await state.get_data()
    loc: Any | None = data.get("loc_admin")
    if not loc:
        return

    key_path: str = callback.data or ''
    if not key_path.startswith("admin"):
        key_path = f"admin.{key_path}"

    # Двигаемся по вложенной структуре локализации
    keys: list[str] = key_path.split('.')
    current: Any = loc.default

    try:
        for k in keys:
            current = getattr(current, k)
    except AttributeError:
        # Если ключа нет — выходим
        return

    # Получаем текст и клавиатуру
    text: str = current.text
    keyboard_data: list = getattr(current, 'keyboard', [])
    keyboard: kb.InlineKeyboardMarkup = await kb.keyboard_dynamic(
        keyboard_data
    )

    # Редактируем сообщение с текстом и клавиатурой
    await callback.message.edit_text(
        text,
        parse_mode='HTML',
        reply_markup=keyboard
    )

    await log(callback)


# @admin_callback(lambda c: c.data in CALLBACK_SELECT)
# async def select(
#     callback: CallbackQuery,
#     state: FSMContext
# ) -> None:
#     if not isinstance(callback.message, Message):
#         return

#     user_data: Dict[str, Any] = await state.get_data()
#     loc: Any | None = user_data.get("loc_admin")
#     if not loc:
#         return

#     key: str = callback.data or ''
#     current_value: Any | None = user_data.get(key)

#     text: Any = getattr(loc.default, key).text
#     keyboard_data: Any = getattr(loc.default, key).keyboard

#     keyboard: kb.InlineKeyboardMarkup = await kb.toggle(
#         keyboard_data,
#         f'select_{key}_{current_value}' if current_value else ''
#     )

#     await callback.message.edit_text(
#         text=text,
#         parse_mode='HTML',
#         reply_markup=keyboard
#     )
#     await log(callback)


# @admin_callback(lambda c: c.data and c.data.startswith('select_')
#                 and len(c.data.split('_')) == 3)
# async def option(
#     callback: CallbackQuery,
#     state: FSMContext
# ) -> None:
#     await callback.answer()
#     if not callback.data or not isinstance(callback.message, Message):
#         return

#     await callback.message.delete()

#     _, key, value = callback.data.split('_')
#     user_data: Dict[str, Any] = await state.get_data()
#     loc: Optional[Localization] = user_data.get('loc')

#     if key and value:
#         loc = await load_localization(value)
#         await state.update_data(lang=value, loc=loc)

#     if not loc:
#         return

#     text: Any = getattr(loc.default, key).text
#     keyboard_data: Any = getattr(loc.default, key).keyboard

#     keyboard: kb.InlineKeyboardMarkup = await kb.toggle(
#         keyboard_data,
#         callback.data
#     )

#     try:
#         await callback.message.edit_text(
#             text=text,
#             parse_mode='HTML',
#             reply_markup=keyboard
#         )
#         update_dict: Dict[str, Any] = {key: value}
#         await state.update_data(**update_dict)
#         # await user_action_wrapper(
#         #     tg_id=callback.from_user.id,
#         #     action='update',
#         #     field=key,
#         #     value=value
#         # )
#     except Exception:
#         pass

#     await log(callback)
