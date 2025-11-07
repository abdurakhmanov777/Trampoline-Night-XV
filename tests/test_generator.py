import os
from io import BytesIO

import pytest
from PIL import Image
from PIL.ImageFile import ImageFile

from app.services.generator.main import create_text_image

# Определяем тестовые данные
TEST_TEXT = "Тест"
FONT_PATH: str = os.path.join(
    os.path.dirname(__file__),
    "../app/services/generator/ALS_Sector_Bold.ttf"
)
INPUT_IMAGE_PATH: str = os.path.join(
    os.path.dirname(__file__),
    "../app/services/generator/images/input.png"
)


@pytest.mark.asyncio
async def test_create_text_image_returns_bytesio():
    """Функция должна возвращать объект BytesIO."""
    result: BytesIO = await create_text_image(TEST_TEXT)
    assert isinstance(result, BytesIO)


@pytest.mark.asyncio
async def test_create_text_image_is_valid_png():
    """Буфер должен содержать корректное PNG-изображение."""
    buffer: BytesIO = await create_text_image(TEST_TEXT)
    buffer.seek(0)
    image: ImageFile = Image.open(buffer)
    assert image.format == "PNG"


@pytest.mark.asyncio
async def test_create_text_image_size_matches_background():
    """Размер изображения должен совпадать с исходным фоном."""
    background: ImageFile = Image.open(INPUT_IMAGE_PATH)
    buffer: BytesIO = await create_text_image(TEST_TEXT)
    buffer.seek(0)
    image: ImageFile = Image.open(buffer)
    assert image.size == background.size
