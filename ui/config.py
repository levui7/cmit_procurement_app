"""
Конфигурация приложения
"""
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).parent
ICONS_DIR = BASE_DIR / "icons"
STYLES_DIR = BASE_DIR / "styles"

# Название приложения
APP_TITLE = "Закупки ЦМИТ ЛЮКС"
APP_LOGO = "cmit_logo_parody.png"

# Размеры окна
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800

# Размеры sidebar
SIDEBAR_WIDTH = 280
LOGO_HEIGHT = 80
MENU_BUTTON_HEIGHT = 50

# Элементы меню
MENU_ITEMS = [
    ("home.png", "Главная"),
    ("add.png", "Создать заявку"),
    ("search.png", "История заявок"),
    ("product.png", "Справочник товаров"),
    ("light-bulb.png", "О предприятии"),
    ("settings.png", "Настройки"),
]