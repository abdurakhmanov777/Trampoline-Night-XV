import codecs
import os
from pathlib import Path
from typing import Set

from dotenv import load_dotenv

# ------------------------------------------------------------
# Загрузка переменных окружения
# ------------------------------------------------------------
from_path: Path = Path(__file__).parent.parent / ".env"
load_dotenv(from_path)
# ------------------------------------------------------------
# Основные настройки приложения
# ------------------------------------------------------------
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
DB_URL: str = os.getenv("DB_URL", "")
LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")

# ------------------------------------------------------------
# Пути к ресурсам
# ------------------------------------------------------------
ASSETS_DIR = Path(os.getenv("ASSETS_DIR", "assets"))
IMAGES_DIR: Path = ASSETS_DIR / "images"
FONTS_DIR: Path = ASSETS_DIR / "fonts"

IMAGE_PATH: Path = IMAGES_DIR / os.getenv("IMAGE_NAME", "background.png")
FONT_PATH: Path = FONTS_DIR / os.getenv("FONT_NAME", "ALS_Sector_Bold.ttf")

# ------------------------------------------------------------
# Дополнительные параметры
# ------------------------------------------------------------
TIME_ZONE: int = int(os.getenv("TIME_ZONE", "0"))
MAIN_ADMINS: list[int] = [
    int(x) for x in os.getenv("MAIN_ADMINS", "").split(",") if x
]

SYMB: str = codecs.decode(os.getenv("SYMB", "").encode(), "unicode_escape")

# ------------------------------------------------------------
# Google Sheets
# ------------------------------------------------------------
GSHEET_NAME: str = os.getenv("NAME_GOOGLESHEETS", "DefaultSheetName")
GSHEET_TAB: str = os.getenv("GOOGLE_SHEET_WORKSHEET", "Участники")
GSHEET_CREDS: Path = Path("credentials/creds.json")

# ------------------------------------------------------------
# Команды и callback-префиксы
# ------------------------------------------------------------
COMMAND_MAIN: Set[str] = {"start", "help", "test"}
CALLBACK_MAIN: Set[str] = {"start", "settings", "info", "miniapp"}
CALLBACK_SELECT: Set[str] = {"lang"}
