"""
Боковая панель навигации (Sidebar)
"""
from pathlib import Path
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QWidget, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ui.utils.icons import create_icon_label, IconNames
from ui.utils.config import SIDEBAR_WIDTH, LOGO_HEIGHT, MENU_BUTTON_HEIGHT, MENU_ITEMS


class Sidebar(QFrame):
    """
    Боковая панель навигации

    Сигналы:
        page_changed(str): Вызывается при переключении страницы
    """

    page_changed = pyqtSignal(str)  # Сигнал с именем страницы

    def __init__(self, icons_path: Path = None, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path
        self.current_page = "Главная"
        self.menu_buttons = {}  # name -> QPushButton

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Создание интерфейса sidebar"""
        self.setObjectName("sidebar")
        self.setFixedWidth(SIDEBAR_WIDTH)

        # Главный layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Логотип
        logo_frame = self._create_logo_section()
        layout.addWidget(logo_frame)

        # 2. Меню навигации
        menu_frame = self._create_menu_section()
        layout.addWidget(menu_frame)

        # 3. Растягиватель (чтобы меню было сверху)
        layout.addStretch()

    def _create_logo_section(self) -> QFrame:
        """Создать секцию с логотипом"""
        logo_frame = QFrame()
        logo_frame.setObjectName("logoFrame")
        logo_frame.setFixedHeight(LOGO_HEIGHT)

        layout = QHBoxLayout(logo_frame)
        layout.setContentsMargins(25, 20, 20, 20)
        layout.setSpacing(15)

        # Иконка логотипа
        logo_icon = create_icon_label(IconNames.LOGO, size=40)
        layout.addWidget(logo_icon)

        # Текст логотипа
        logo_text = QLabel("ЦМИТ ЛЮКС")
        logo_text.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        logo_text.setStyleSheet("color: #1F2937;")
        layout.addWidget(logo_text)

        layout.addStretch()

        return logo_frame

    def _create_menu_section(self) -> QFrame:
        """Создать секцию с меню навигации"""
        menu_frame = QFrame()
        menu_frame.setObjectName("menuFrame")

        layout = QVBoxLayout(menu_frame)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)

        # Создание кнопок меню
        for icon_name, page_name in MENU_ITEMS:
            btn = self._create_menu_button(icon_name, page_name)
            self.menu_buttons[page_name] = btn
            layout.addWidget(btn)

        return menu_frame

    def _create_menu_button(self, icon_name: str, page_name: str) -> QPushButton:
        """
        Создать кнопку меню

        Args:
            icon_name: Название иконки
            page_name: Имя страницы

        Returns:
            QPushButton с иконкой и текстом
        """
        btn = QPushButton()
        btn.setObjectName("menuButton")
        btn.setFixedHeight(MENU_BUTTON_HEIGHT)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont("Segoe UI", 13))
        btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        btn.setToolTip(page_name)

        # Layout для кнопки
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(20, 10, 20, 10)
        btn_layout.setSpacing(15)

        # Иконка
        icon_label = create_icon_label(icon_name, size=24)
        btn_layout.addWidget(icon_label)

        # Текст
        text_label = QLabel(page_name)
        text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text_label.setFont(QFont("Segoe UI", 13))
        btn_layout.addWidget(text_label)

        btn_layout.addStretch()

        # Подключение клика
        btn.clicked.connect(lambda checked, name=page_name: self._on_button_click(name))

        return btn

    def _on_button_click(self, page_name: str):
        """
        Обработчик клика по кнопке меню

        Args:
            page_name: Имя страницы для перехода
        """
        if page_name != self.current_page:
            self.current_page = page_name
            self._update_active_button()
            self.page_changed.emit(page_name)

    def _update_active_button(self):
        """Обновить активную кнопку меню"""
        for name, btn in self.menu_buttons.items():
            if name == self.current_page:
                btn.setObjectName("activeMenu")
            else:
                btn.setObjectName("menuButton")

            # Принудительно обновить стили
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def _apply_styles(self):
        """Применение стилей"""
        # Стили применяются через главный файл styles.py
        # Здесь можно добавить специфичные стили если нужно
        pass

    def set_active_page(self, page_name: str):
        """
        Установить активную страницу (вызывается из главного окна)

        Args:
            page_name: Имя активной страницы
        """
        if page_name != self.current_page:
            self.current_page = page_name
            self._update_active_button()

    def get_current_page(self) -> str:
        """Получить имя текущей страницы"""
        return self.current_page


class SidebarButton(QPushButton):
    """
    Кастомная кнопка для sidebar (опционально, для большей гибкости)
    """

    def __init__(self, icon_name: str, text: str, parent=None):
        super().__init__(parent)
        self.icon_name = icon_name
        self.text = text
        self._setup_ui()

    def _setup_ui(self):
        """Настройка кнопки"""
        self.setObjectName("menuButton")
        self.setFixedHeight(MENU_BUTTON_HEIGHT)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 13))
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)

        icon = create_icon_label(self.icon_name, size=24)
        layout.addWidget(icon)

        label = QLabel(self.text)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(label)
        layout.addStretch()

# """
# Общий sidebar для всех страниц
# """
# from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont, QPixmap
# from pathlib import Path
# from functools import partial
#
#
# class Sidebar(QFrame):
#     """Общий sidebar с навигацией"""
#
#     def __init__(self, icons_path, on_page_change=None, parent=None):
#         super().__init__(parent)
#         self.icons_path = icons_path
#         self.on_page_change = on_page_change  # Функция обратного вызова
#         self.current_page = "Главная"
#         self.menu_buttons = {}
#
#         self.setObjectName("sidebar")
#         self.setFixedWidth(280)
#
#         self._create_ui()
#
#     def _create_ui(self):
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)
#
#         # Логотип
#         logo_frame = QFrame()
#         logo_frame.setObjectName("logoFrame")
#         logo_frame.setFixedHeight(80)
#         logo_layout = QHBoxLayout(logo_frame)
#         logo_layout.setContentsMargins(25, 20, 20, 20)
#         logo_layout.setSpacing(15)
#
#         logo_icon = self._create_icon_label("cmit_logo_parody.png", size=40)
#         logo_text = QLabel("ЦМИТ ЛЮКС")
#         logo_text.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
#         logo_text.setStyleSheet("color: #1F2937;")
#
#         logo_layout.addWidget(logo_icon)
#         logo_layout.addWidget(logo_text)
#         logo_layout.addStretch()
#         layout.addWidget(logo_frame)
#
#         # Меню
#         menu_frame = QFrame()
#         menu_frame.setObjectName("menuFrame")
#         menu_layout = QVBoxLayout(menu_frame)
#         menu_layout.setContentsMargins(10, 20, 10, 20)
#         menu_layout.setSpacing(5)
#
#         menu_items = [
#             ("home.png", "Главная"),
#             ("add.png", "Создать заявку"),
#             ("search.png", "История заявок"),
#             ("product.png", "Справочник товаров"),
#             ("light-bulb.png", "О предприятии"),
#             ("settings.png", "Настройки"),
#         ]
#
#         for icon_file, text in menu_items:
#             btn = self._create_menu_button(icon_file, text)
#             self.menu_buttons[text] = btn
#             menu_layout.addWidget(btn)
#
#         menu_layout.addStretch()
#         layout.addWidget(menu_frame)
#
#         # Установить активную страницу
#         self.set_active_page("Главная")
#
#     def _create_menu_button(self, icon_file, text):
#         btn = QPushButton()
#         btn.setObjectName("menuButton")
#         btn.setFixedHeight(50)
#         btn.setCursor(Qt.CursorShape.PointingHandCursor)
#         btn.setFont(QFont("Segoe UI", 13))
#         btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
#
#         # Layout для кнопки
#         btn_layout = QHBoxLayout(btn)
#         btn_layout.setContentsMargins(20, 10, 20, 10)
#         btn_layout.setSpacing(15)
#
#         icon_label = self._create_icon_label(icon_file, size=24)
#         text_label = QLabel(text)
#         text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
#
#         btn_layout.addWidget(icon_label)
#         btn_layout.addWidget(text_label)
#         btn_layout.addStretch()
#
#         # Подключение клика
#         btn.clicked.connect(lambda: self._on_button_click(text))
#
#         return btn
#
#     def _on_button_click(self, page_name):
#         """Обработчик клика по кнопке"""
#         if self.on_page_change:
#             self.on_page_change(page_name)
#
#     # def set_active_page(self, page_name):
#     #     """Установить активную страницу"""
#     #     self.current_page = page_name
#     #
#     #     for name, btn in self.menu_buttons.items():
#     #         if name == page_name:
#     #             btn.setObjectName("activeMenu")
#     #         else:
#     #             btn.setObjectName("menuButton")
#     #
#     #     # Обновить стили
#     #     self.style().unpolish(self)
#     #     self.style().polish(self)
#
#     def set_active_page(self, page_name):
#         """Установить активную страницу"""
#         self.current_page = page_name
#
#         for name, btn in self.menu_buttons.items():
#             if name == page_name:
#                 btn.setObjectName("activeMenu")
#             else:
#                 btn.setObjectName("menuButton")
#
#             # Применяем unpolish/polish к каждой кнопке, а не к sidebar
#             btn.style().unpolish(btn)
#             btn.style().polish(btn)
#             btn.update()
#
#     def _create_icon_label(self, filename, size=24):
#         label = QLabel()
#         icon_path = self.icons_path / filename
#
#         if icon_path.exists():
#             pixmap = QPixmap(str(icon_path))
#             scaled_pixmap = pixmap.scaled(size, size,
#                                           Qt.AspectRatioMode.KeepAspectRatio,
#                                           Qt.TransformationMode.SmoothTransformation)
#             label.setPixmap(scaled_pixmap)
#
#         label.setFixedSize(size, size)
#         return label