"""
Модуль для асинхронной загрузки файлов локализации и объединения их
в один объект для пользователя или администратора.
"""

import json
from pathlib import Path
from typing import Any, Literal

import aiofiles
from loguru import logger

from app.config import LOCALIZATIONS_DIR
from app.core.bot.services.localization.model import Localization


async def _read_json(
    file_path: Path
) -> dict[str, Any]:
    """Асинхронно читает JSON-файл и возвращает словарь.

    Args:
        file_path (Path): Путь к JSON-файлу.

    Returns:
        dict[str, Any]: Содержимое файла в виде словаря. Пустой словарь
        при ошибке или отсутствии файла.
    """
    if not file_path.exists():
        logger.error(f"File not found: {file_path.resolve()}")
        return {}

    try:
        async with aiofiles.open(
            file_path,
            mode="r",
            encoding="utf8"
        ) as f:
            content: str = await f.read()
            return json.loads(content)
    except Exception as error:
        logger.error(f"Error loading {file_path}: {error}")
        return {}


async def load_localization(
    language: str,
    role: Literal["user", "admin"]
) -> Localization:
    """Загружает локализацию для пользователя или администратора.

    Для пользователя объединяет данные из файла default и файла
    его директории. Для администратора загружает один файл.

    Args:
        language (str): Код языка (например, 'en', 'ru').
        role (Literal['user', 'admin']): Роль для которой загружается
            локализация.

    Returns:
        Localization: Экземпляр объекта локализации с загруженными
        данными.
    """
    dir_path: Path = LOCALIZATIONS_DIR / role

    if role == "user":
        # Для пользователя: объединяем данные из default и его директории
        file_event_steps: Path = LOCALIZATIONS_DIR / \
            "default" / f"{language}.json"
        file_other: Path = dir_path / f"{language}.json"

        data: dict[str, Any] = await _read_json(file_event_steps)
        data.update(await _read_json(file_other))
        return Localization(data)

    # Для администратора: загружаем один файл
    return Localization(await _read_json(dir_path / f"{language}.json"))
