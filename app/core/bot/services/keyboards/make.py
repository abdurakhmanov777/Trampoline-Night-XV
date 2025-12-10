from aiogram import types


def build_keyboard(
    button_rows: list[list[tuple[str, str]]]
) -> types.InlineKeyboardMarkup:
    """Создаёт InlineKeyboardMarkup из списка рядов кнопок."""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text=text,
                callback_data=cb
            ) for text, cb in row]
            for row in button_rows
        ]
    )
