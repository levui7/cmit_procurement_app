# """
# Главное окно приложения с общим sidebar и exit card
# """
# import sys
# from pathlib import Path
# from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
# from PyQt6.QtGui import QFont, QIcon
#
# from ui.utils.config import APP_TITLE, APP_LOGO, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
# from ui.utils.styles import get_main_window_styles
# from ui.widgets.sidebar import Sidebar
# from ui.widgets.exit_card import ExitCard
#
# from ui.pages.main_page import MainPage
# from ui.pages.create_request import CreateRequestPage
# from ui.pages.history_request import HistoryRequestPage
# from ui.pages.product_catalog import ProductCatalogPage
# from ui.pages.about_company import AboutCompanyPage
# from ui.pages.settings import SettingsPage
#
#
# class AppWindow(QMainWindow):
#     """Главное окно приложения"""
#
#     def __init__(self):
#         super().__init__()
#
#         self.icons_path = Path(__file__).parent / "icons"
#         self._switching_page = False
#
#         self._setup_window()
#         self._create_widgets()
#         self._apply_styles()
#
#     def _setup_window(self):
#         """Настройка окна"""
#         self.setWindowTitle(APP_TITLE)
#         self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
#         self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
#
#         icon_path = self.icons_path / APP_LOGO
#         if icon_path.exists():
#             self.setWindowIcon(QIcon(str(icon_path)))
#
#     def _create_widgets(self):
#         """Создание интерфейса"""
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#
#         # Главный layout
#         main_layout = QHBoxLayout(central_widget)
#         main_layout.setContentsMargins(0, 0, 0, 0)
#         main_layout.setSpacing(0)
#
#         # 1. Sidebar
#         # self.sidebar = Sidebar(
#         #     icons_path=self.icons_path,
#         #     parent=self
#         # )
#         self.sidebar = Sidebar(parent=self)
#
#         self.sidebar.page_changed.connect(self.switch_page)
#
#         main_layout.addWidget(self.sidebar)
#
#         # 2. Правая часть
#         right_widget = QWidget()
#         right_layout = QVBoxLayout(right_widget)
#         right_layout.setContentsMargins(0, 0, 0, 0)
#         right_layout.setSpacing(0)
#
#         # QStackedWidget для страниц
#         self.stack = QStackedWidget()
#         self.stack.setObjectName("pageStack")
#
#         # Создаем страницы (icons_path больше не передаётся)
#         self.pages = {
#             "Главная": MainPage(parent=self),
#             "Создать заявку": CreateRequestPage(parent=self),
#             "История заявок": HistoryRequestPage(parent=self),
#             "Справочник товаров": ProductCatalogPage(parent=self),
#             "О предприятии": AboutCompanyPage(parent=self),
#             "Настройки": SettingsPage(parent=self),
#         }
#
#         for page in self.pages.values():
#             self.stack.addWidget(page)
#
#         right_layout.addWidget(self.stack)
#
#         # 3. Exit card внизу
#         exit_container = QWidget()
#         exit_layout = QHBoxLayout(exit_container)
#         exit_layout.setContentsMargins(0, 0, 50, 40)
#         exit_layout.addStretch()
#
#         self.exit_card = ExitCard(self.icons_path, parent=self)
#         exit_layout.addWidget(self.exit_card)
#
#         right_layout.addWidget(exit_container)
#         main_layout.addWidget(right_widget)
#
#         # Показываем главную страницу
#         self.switch_page("Главная")
#
#     def switch_page(self, page_name):
#         """Переключение страницы"""
#         if self._switching_page:
#             return
#         self._switching_page = True
#
#         try:
#             if page_name in self.pages:
#                 index = list(self.pages.keys()).index(page_name)
#                 self.stack.setCurrentIndex(index)
#
#                 # Делегируем управление подсветкой сайдбару
#                 self.sidebar.set_active_page(page_name)
#
#         finally:
#             self._switching_page = False
#
#     def _apply_styles(self):
#         """Применение стилей"""
#         self.setStyleSheet(get_main_window_styles())
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     app.setFont(QFont("Segoe UI", 10))
#
#     window = AppWindow()
#     window.show()
#
#     sys.exit(app.exec())

"""
Главное окно приложения с общим sidebar и exit card
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PyQt6.QtGui import QFont, QIcon

from ui.utils.config import APP_TITLE, APP_LOGO, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from ui.utils.styles import get_main_window_styles  # ✅ ИСПРАВЛЕНО: ui.styles вместо ui.utils.styles
from ui.widgets.sidebar import Sidebar
from ui.widgets.exit_card import ExitCard

from ui.pages.main_page import MainPage
from ui.pages.create_request import CreateRequestPage
from ui.pages.history_request import HistoryRequestPage
from ui.pages.product_catalog import ProductCatalogPage
from ui.pages.about_company import AboutCompanyPage
from ui.pages.settings import SettingsPage


class AppWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()

        # ✅ ИСПРАВЛЕНО: правильный путь к иконкам (ui/utils -> ui -> icons)
        self.icons_path = Path(__file__).parent.parent / "icons"
        self._switching_page = False

        self._setup_window()
        self._create_widgets()
        self._apply_styles()

    def _setup_window(self):
        """Настройка окна"""
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        icon_path = self.icons_path / APP_LOGO
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

    def _create_widgets(self):
        """Создание интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Sidebar
        self.sidebar = Sidebar(parent=self)
        self.sidebar.page_changed.connect(self.switch_page)
        main_layout.addWidget(self.sidebar)

        # 2. Правая часть
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # QStackedWidget для страниц
        self.stack = QStackedWidget()
        self.stack.setObjectName("pageStack")

        # Создаем страницы
        self.pages = {
            "Главная": MainPage(parent=self),
            "Создать заявку": CreateRequestPage(parent=self),
            "История заявок": HistoryRequestPage(parent=self),
            "Справочник товаров": ProductCatalogPage(parent=self),
            "О предприятии": AboutCompanyPage(parent=self),
            "Настройки": SettingsPage(parent=self),
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        right_layout.addWidget(self.stack)

        # 3. Exit card внизу
        exit_container = QWidget()
        exit_layout = QHBoxLayout(exit_container)
        exit_layout.setContentsMargins(0, 0, 50, 40)
        exit_layout.addStretch()

        # ✅ ИСПРАВЛЕНО: убран icons_path
        self.exit_card = ExitCard(parent=self)
        exit_layout.addWidget(self.exit_card)

        right_layout.addWidget(exit_container)
        main_layout.addWidget(right_widget)

        # Показываем главную страницу
        self.switch_page("Главная")

    def switch_page(self, page_name):
        """Переключение страницы"""
        if self._switching_page:
            return
        self._switching_page = True

        try:
            if page_name in self.pages:
                index = list(self.pages.keys()).index(page_name)
                self.stack.setCurrentIndex(index)
                self.sidebar.set_active_page(page_name)
        finally:
            self._switching_page = False

    def _apply_styles(self):
        """Применение стилей"""
        self.setStyleSheet(get_main_window_styles())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    window = AppWindow()
    window.show()

    sys.exit(app.exec())