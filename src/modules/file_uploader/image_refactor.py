import asyncio
import random

from PIL import Image
from loguru import logger


async def add_random_pixel(file_path: str):
    async with asyncio.Lock():
        try:
            image = Image.open(file_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            width, height = image.size
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            image.putpixel((x, y), random_color)

            image.save(file_path, quality=95)
            return image
        except (IOError, PermissionError) as e:
            logger.error(f"Failed to process image {file_path}: {e}")
