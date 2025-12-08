"""
Модуль для асинхронной загрузки файлов локализации.

Позволяет загружать JSON-файлы локализации для пользователей
и администраторов без блокировки event loop.
"""

import json
from pathlib import Path
from typing import Any, Literal

import aiofiles
from loguru import logger

from app.config import LOCALIZATIONS_DIR
from app.core.bot.services.localization.model import Localization


async def load_localization(
    language: str,
    role: Literal[
        "user",
        "admin",
    ],
) -> Localization:
    """
    Асинхронно загружает файл локализации по указанному языку и роли.

    Args:
        language (str): Код языка, например "ru".
        role (Literal["user", "admin"]):
            "user" для пользовательской локализации,
            "admin" для админской.

    Returns:
        Localization: Экземпляр Localization с данными из JSON-файла.
        Если файл не найден или произошла ошибка, возвращается пустая
        локализация.
    """
    # Определяем директорию в зависимости от роли
    dir_path: Path = LOCALIZATIONS_DIR / role

    # Формируем путь к файлу
    file_path: Path = dir_path / f"{language}.json"

    if not file_path.exists():
        logger.error(f"Localization file not found: {file_path.resolve()}")
        return Localization({})

    try:
        async with aiofiles.open(file_path, mode="r", encoding="utf8") as f:
            content: str = await f.read()
            localization_dict: Any = json.loads(content)
            return Localization(localization_dict)
    except Exception as error:
        logger.error(f"Error loading localization file: {error}")
        return Localization({})
