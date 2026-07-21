"""
Утилиты для работы с иконками
"""
from pathlib import Path
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from ui.utils.config import ICONS_DIR

# ========== ИМЕНА ИКОНОК (центральный реестр) ==========
class IconNames:
    """Названия всех иконок в приложении"""
    # Навигация
    HOME = "home.png"
    ADD = "add.png"
    SEARCH = "search.png"
    PRODUCT = "product.png"
    SETTINGS = "settings.png"
    LIGHT_BULB = "light-bulb.png"
    DOOR = "door.png"

    # Действия
    EDIT = "edit.png"
    DELETE = "delete.png"
    SAVE = "save.png"
    CANCEL = "cancel.png"
    CLEAR = "clear.png"
    EXPORT = "export.png"
    IMPORT = "import.png"

    # Элементы интерфейса
    CALENDAR = "calendar.png"
    STAR = "star.png"
    GROUP = "group.png"
    DOCUMENT = "document.png"
    RUBBLE = "ruble.png"
    MAGNIFYING_GLASS = "magnifying-glass.png"
    STATS = "stats.png"
    WARNING = "warning.png"
    ACTIVE_REQUEST = "sticky-note.png"

    # Логотип
    LOGO = "cmit_logo_parody.png"


def create_icon_label(icon_name: str, size: int = 24, parent=None) -> QLabel:
    """
    Создать QLabel с иконкой

    Args:
        icon_name: Название иконки из IconNames или путь
        size: Размер иконки в пикселях
        parent: Родительский виджет

    Returns:
        QLabel с иконкой
    """
    label = QLabel(parent=parent)
    icon_path = ICONS_DIR / icon_name

    if icon_path.exists():
        pixmap = QPixmap(str(icon_path))
        scaled_pixmap = pixmap.scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(scaled_pixmap)
    else:
        # Заглушка если иконка не найдена
        label.setText(f"[{icon_name}]")
        label.setStyleSheet("color: #9CA3AF; font-size: 10px;")

    label.setFixedSize(size, size)
    return label


def get_icon_path(icon_name: str) -> Path:
    """Получить полный путь к иконке"""
    return ICONS_DIR / icon_name


def icon_exists(icon_name: str) -> bool:
    """Проверить существует ли иконка"""
    return (ICONS_DIR / icon_name).exists()