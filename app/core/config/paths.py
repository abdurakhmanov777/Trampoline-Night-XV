"""
Пути к файлам, шрифтам и изображениям
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# Основные директории
# ------------------------------------------------------------
ASSETS_DIR: Path = Path(os.getenv("ASSETS_DIR", "assets"))
IMAGES_DIR: Path = ASSETS_DIR / "images"
FONTS_DIR: Path = ASSETS_DIR / "fonts"
FILES_DIR: Path = ASSETS_DIR / "files"

# ------------------------------------------------------------
# Основные ресурсы
# ------------------------------------------------------------
IMAGE_PATH: Path = IMAGES_DIR / os.getenv(
    "IMAGE_NAME", "background.png"
)
FONT_PATH: Path = FONTS_DIR / os.getenv(
    "FONT_NAME", "ALS_Sector_Bold.ttf"
)

# ------------------------------------------------------------
# Документы для отправки через бота
# ------------------------------------------------------------
GUEST_PATH: Path = FILES_DIR / os.getenv(
    "GUEST_PATH", "Анкета_гостя.pdf"
)
PARTICIPANT_PATH: Path = FILES_DIR / os.getenv(
    "PARTICIPANT_PATH", "Расписка_участника.pdf"
)
