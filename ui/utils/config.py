"""
Конфигурация приложения
"""
from pathlib import Path

from PyQt6.QtGui import QFont

# ========== ПУТИ ==========
# Поднимаемся от ui/utils/config.py на 3 уровня вверх до корня проекта
BASE_DIR = Path(__file__).parent.parent.parent
ICONS_DIR = BASE_DIR / "ui" / "icons"
DATA_DIR = BASE_DIR / "data"
STYLES_DIR = BASE_DIR / "ui" / "styles"

# БД
DB_ECHO = False

# Создаем папку data если её нет
DATA_DIR.mkdir(exist_ok=True)

# ========== НАЗВАНИЕ ПРИЛОЖЕНИЯ ==========
APP_TITLE = "Закупки ЦМИТ ЛЮКС"
APP_LOGO = "cmit_logo_parody.png"

# ========== РАЗМЕРЫ ОКНА ==========
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800

# ========== SIDEBAR ==========
SIDEBAR_WIDTH = 280
LOGO_HEIGHT = 80
MENU_BUTTON_HEIGHT = 50

# ========== ЭЛЕМЕНТЫ МЕНЮ ==========
MENU_ITEMS = [
    ("home.png", "Главная"),
    ("add.png", "Создать заявку"),
    ("search.png", "История заявок"),
    ("product.png", "Справочник товаров"),
    ("light-bulb.png", "О предприятии"),
    ("settings.png", "Настройки"),
]


# ========== ЦВЕТОВАЯ СХЕМА ==========
class Colors:
    """Цветовая палитра приложения (Tailwind CSS style)"""

    # Основные (Primary)
    PRIMARY = "#3B82F6"
    PRIMARY_HOVER = "#2563EB"
    PRIMARY_LIGHT = "#EFF6FF"
    PRIMARY_DARK = "#1D4ED8"

    # Вторичные
    SECONDARY = "#6B7280"
    SECONDARY_HOVER = "#4B5563"
    SUCCESS = "#10B981"
    SUCCESS_LIGHT = "#D1FAE5"
    WARNING = "#F59E0B"
    WARNING_LIGHT = "#FEF3C7"
    DANGER = "#EF4444"
    DANGER_HOVER = "#DC2626"
    DANGER_LIGHT = "#FEE2E2"

    # Фоны
    BACKGROUND = "#F9FAFB"
    SURFACE = "#FFFFFF"
    BORDER = "#E5E7EB"
    BORDER_DARK = "#D1D5DB"

    # Текст
    TEXT_PRIMARY = "#1F2937"
    TEXT_SECONDARY = "#6B7280"
    TEXT_MUTED = "#9CA3AF"
    TEXT_INVERTED = "#FFFFFF"

    # Специальные
    INFO_LIGHT = "#DBEAFE"
    PURPLE_LIGHT = "#F3E8FF"
    YELLOW_LIGHT = "#FEF9C3"


# ========== ШРИФТЫ ==========
class Fonts:
    """Настройки шрифтов"""

    FAMILY = "Segoe UI"

    # Размеры
    SIZE_XSMALL = 9
    SIZE_SMALL = 10
    SIZE_NORMAL = 12
    SIZE_MEDIUM = 13
    SIZE_LARGE = 14
    SIZE_XLARGE = 16
    SIZE_TITLE = 20
    SIZE_HEADING = 24
    SIZE_DISPLAY = 32

    # Веса
    WEIGHT_NORMAL = QFont.Weight.Normal if 'QFont' in dir() else 400
    WEIGHT_MEDIUM = QFont.Weight.Medium if 'QFont' in dir() else 500
    WEIGHT_BOLD = QFont.Weight.Bold if 'QFont' in dir() else 700


# ========== ОТСТУПЫ ==========
class Spacing:
    """Стандартные отступы (в пикселях)"""

    NONE = 0
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 24
    XXL = 32
    XXXL = 48


# ========== РАЗМЕРЫ ЭЛЕМЕНТОВ ==========
class Sizes:
    """Стандартные размеры UI-элементов"""

    # Кнопки
    BUTTON_HEIGHT = 45
    BUTTON_HEIGHT_SMALL = 35
    BUTTON_HEIGHT_LARGE = 55

    # Поля ввода
    INPUT_HEIGHT = 40
    INPUT_HEIGHT_SMALL = 32

    # Иконки
    ICON_XSMALL = 14
    ICON_SMALL = 18
    ICON_MEDIUM = 24
    ICON_LARGE = 32
    ICON_XLARGE = 48
    ICON_XXLARGE = 64

    # Карточки
    CARD_RADIUS = 12
    CARD_RADIUS_LARGE = 16

    # Таблицы
    TABLE_ROW_HEIGHT = 50
    TABLE_HEADER_HEIGHT = 45

    # Пагинация
    ITEMS_PER_PAGE = 10
    PAGINATION_BUTTON_SIZE = 35


# ========== НАСТРОЙКИ ПО УМОЛЧАНИЮ ==========
class Defaults:
    """Значения по умолчанию"""

    DAMAGE_PERCENT = 2.5
    MIN_RATING = "4.0"
    STUDENTS_COUNT = 100
    TIMEOUT = 5
    MAX_ITEMS = 20