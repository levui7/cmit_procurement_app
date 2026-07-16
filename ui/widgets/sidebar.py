"""
Общий sidebar для всех страниц
"""
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from pathlib import Path
from functools import partial


class Sidebar(QFrame):
    """Общий sidebar с навигацией"""

    def __init__(self, icons_path, on_page_change=None, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path
        self.on_page_change = on_page_change  # Функция обратного вызова
        self.current_page = "Главная"
        self.menu_buttons = {}

        self.setObjectName("sidebar")
        self.setFixedWidth(280)

        self._create_ui()

    def _create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Логотип
        logo_frame = QFrame()
        logo_frame.setObjectName("logoFrame")
        logo_frame.setFixedHeight(80)
        logo_layout = QHBoxLayout(logo_frame)
        logo_layout.setContentsMargins(25, 20, 20, 20)
        logo_layout.setSpacing(15)

        logo_icon = self._create_icon_label("cmit_logo_parody.png", size=40)
        logo_text = QLabel("ЦМИТ ЛЮКС")
        logo_text.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        logo_text.setStyleSheet("color: #1F2937;")

        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        layout.addWidget(logo_frame)

        # Меню
        menu_frame = QFrame()
        menu_frame.setObjectName("menuFrame")
        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setContentsMargins(10, 20, 10, 20)
        menu_layout.setSpacing(5)

        menu_items = [
            ("home.png", "Главная"),
            ("add.png", "Создать заявку"),
            ("search.png", "История заявок"),
            ("product.png", "Справочник товаров"),
            ("light-bulb.png", "О предприятии"),
            ("settings.png", "Настройки"),
        ]

        for icon_file, text in menu_items:
            btn = self._create_menu_button(icon_file, text)
            self.menu_buttons[text] = btn
            menu_layout.addWidget(btn)

        menu_layout.addStretch()
        layout.addWidget(menu_frame)

        # Установить активную страницу
        self.set_active_page("Главная")

    def _create_menu_button(self, icon_file, text):
        btn = QPushButton()
        btn.setObjectName("menuButton")
        btn.setFixedHeight(50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont("Segoe UI", 13))
        btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Layout для кнопки
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(20, 10, 20, 10)
        btn_layout.setSpacing(15)

        icon_label = self._create_icon_label(icon_file, size=24)
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(text_label)
        btn_layout.addStretch()

        # Подключение клика
        btn.clicked.connect(lambda: self._on_button_click(text))

        return btn

    def _on_button_click(self, page_name):
        """Обработчик клика по кнопке"""
        if self.on_page_change:
            self.on_page_change(page_name)

    def set_active_page(self, page_name):
        """Установить активную страницу"""
        self.current_page = page_name

        for name, btn in self.menu_buttons.items():
            if name == page_name:
                btn.setObjectName("activeMenu")
            else:
                btn.setObjectName("menuButton")

        # Обновить стили
        self.style().unpolish(self)
        self.style().polish(self)

    def _create_icon_label(self, filename, size=24):
        label = QLabel()
        icon_path = self.icons_path / filename

        if icon_path.exists():
            pixmap = QPixmap(str(icon_path))
            scaled_pixmap = pixmap.scaled(size, size,
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            label.setPixmap(scaled_pixmap)

        label.setFixedSize(size, size)
        return label