"""
Утилиты для работы с путями
"""
from pathlib import Path
from typing import Union

from core.config import BASE_DIR, DATA_DIR, ICONS_DIR


def get_resource_path(relative_path: str) -> Path:
    """
    Получить абсолютный путь к ресурсу

    Args:
        relative_path: Относительный путь от BASE_DIR

    Returns:
        Абсолютный путь
    """
    return BASE_DIR / relative_path


def ensure_dir(directory: Union[str, Path]) -> Path:
    """
    Убедиться что директория существует, создать если нет

    Args:
        directory: Путь к директории

    Returns:
        Path объект директории
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_db_path() -> Path:
    """Получить путь к базе данных"""
    return DATA_DIR / "procurement.db"


def get_icons_dir() -> Path:
    """Получить путь к папке с иконками"""
    return ICONS_DIR