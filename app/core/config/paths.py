"""
Пути к директориям и ресурсам проекта
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR: Path = Path(__file__).parent.parent.parent.parent

# ------------------------------------------------------------
# Загрузка переменных окружения
# ------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------
# Основные директории проекта
# ------------------------------------------------------------
ASSETS_DIR: Path = BASE_DIR / "app" / "assets"        # Папка с ресурсами
IMAGES_DIR: Path = ASSETS_DIR / "images"             # Картинки
FONTS_DIR: Path = ASSETS_DIR / "fonts"              # Шрифты
FILES_DIR: Path = ASSETS_DIR / "files"              # Документы
LOCALIZATION_DIR: Path = ASSETS_DIR / "localization"  # Локализация

# ------------------------------------------------------------
# Основные ресурсы
# ------------------------------------------------------------
IMAGE_PATH: Path = IMAGES_DIR / os.getenv(
    "IMAGE_NAME", "background.png"
)  # Фоновое изображение
FONT_PATH: Path = FONTS_DIR / os.getenv(
    "FONT_NAME", "ALS_Sector_Bold.ttf"
)  # Шрифт для текста

# ------------------------------------------------------------
# Документы для отправки через бота
# ------------------------------------------------------------
GUEST_PATH: Path = FILES_DIR / os.getenv(
    "GUEST_PATH", "Анкета_гостя.pdf"
)  # Анкета гостя
PARTICIPANT_PATH: Path = FILES_DIR / os.getenv(
    "PARTICIPANT_PATH", "Расписка_участника.pdf"
)  # Расписка участника

# ------------------------------------------------------------
# Файл логирования
# ------------------------------------------------------------
LOG_FILE: Path = BASE_DIR / "logs" / "app.log"  # Лог файл приложения
