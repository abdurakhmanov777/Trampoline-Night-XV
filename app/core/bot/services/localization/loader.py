"""
Модуль для асинхронной загрузки файлов локализации и объединения их
в единый объект локализации для пользователя или администратора.
"""

import asyncio
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
    """Асинхронно читает JSON-файл и возвращает его содержимое.

    Args:
        file_path (Path): Путь к JSON-файлу для чтения.

    Returns:
        dict[str, Any]: Содержимое JSON-файла в виде словаря.
        При ошибке или отсутствии файла возвращается пустой словарь.
    """
    if not file_path.exists():
        logger.error(f"File not found: {file_path.resolve()}")
        return {}

    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            return json.loads(await f.read())
    except Exception as exc:
        logger.error(f"Error loading {file_path}: {exc}")
        return {}


async def load_localization(
    lang: str,
    role: Literal["user", "admin"],
) -> Localization:
    """Загружает локализацию для указанной роли и языка.

    Для пользователей объединяет основной файл и файл локализации
    по умолчанию. Для администраторов загружает только основной файл.

    Args:
        lang (str): Код языка локализации (например, "ru", "en").
        role (Literal["user", "admin"]): Роль пользователя или администратора.

    Returns:
        Localization: Объект локализации с объединёнными данными.
    """
    role_dir: Path = LOCALIZATIONS_DIR / role
    primary_file: Path = role_dir / f"{lang}.json"

    if role == "user":
        default_file: Path = LOCALIZATIONS_DIR / "default" / f"{lang}.json"
        default_data: dict[str, Any]
        primary_data, default_data = await asyncio.gather(
            _read_json(primary_file),
            _read_json(default_file),
        )
        # Объединяем данные дефолтной локализации с основной
        primary_data.update(default_data)
    else:
        primary_data: dict[str, Any] = await _read_json(primary_file)

    return Localization(primary_data)
