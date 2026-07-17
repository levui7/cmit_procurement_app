# import sys
# from pathlib import Path
# from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
#                              QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout,
#                              QSizePolicy, QDialog)
# from PyQt6.QtCore import Qt, QSize
# from PyQt6.QtGui import QFont, QPixmap, QIcon
#
# from ui.styles import get_main_page_styles
#
# class MainPage(QWidget):
#     def __init__(self, icons_path, parent=None):
#         super().__init__(parent)
#         self.icons_path = icons_path
#         self.create_widgets()
#         self.apply_styles()
#
#     def create_icon_label(self, filename, size=24):
#         """Создание QLabel с иконкой"""
#         label = QLabel()
#         pixmap = self.load_icon(filename, size)
#         label.setPixmap(pixmap)
#         label.setFixedSize(size, size)
#         return label
#
#     def create_widgets(self):
#         """Создание контента главной страницы (БЕЗ сайдбара)"""
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(50, 40, 50, 40)
#         layout.setSpacing(30)
#
#         # Заголовок страницы
#         title = QLabel("Главная")
#         title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
#         title.setStyleSheet("color: #1F2937;")
#
#         subtitle = QLabel("Добро пожаловать в систему автоматизации закупок ЦМИТ ЛЮКС")
#         subtitle.setFont(QFont("Segoe UI", 13))
#         subtitle.setStyleSheet("color: #6B7280;")
#
#         layout.addWidget(title)
#         layout.addWidget(subtitle)
#         layout.addSpacing(20)
#
#         # Сетка карточек (2x2)
#         cards_widget = QWidget()
#         cards_layout = QGridLayout(cards_widget)
#         cards_layout.setSpacing(25)
#         cards_layout.setContentsMargins(0, 0, 0, 0)
#
#         # Данные карточек (УДАЛИЛИ "Выход из приложения", так как есть общая кнопка)
#         cards_data = [
#             ("add.png", "Создание новой заявки", "Создайте новую заявку на закупку товаров", "#3B82F6", "#EFF6FF"),
#             ("search.png", "История заявок", "Просмотрите ваши предыдущие заявки", "#10B981", "#D1FAE5"),
#             ("product.png", "Справочник товаров", "Просмотрите или редактируйте актуальные товары предприятия",
#              "#8B5CF6", "#FFFACD"),
#         ]
#
#         for i, (icon_file, title_text, description, icon_color, bg_color) in enumerate(cards_data):
#             card = self.create_card(icon_file, title_text, description, bg_color)
#             row = i // 2
#             col = i % 2
#             cards_layout.addWidget(card, row, col)
#
#         layout.addWidget(cards_widget)
#         layout.addStretch()
#
#     def navigate_to(self, page_name):
#         """Переключение страницы через родительское окно (AppWindow)"""
#         parent = self.parent()
#         while parent is not None:
#             if hasattr(parent, 'switch_page'):
#                 parent.switch_page(page_name)
#                 return
#             parent = parent.parent()
#
#     def create_card(self, icon_file, title, description, bg_color):
#         """Создание карточки с PNG иконкой"""
#         card = QFrame()
#         card.setObjectName("card")
#         card.setFixedHeight(200)
#         card.setCursor(Qt.CursorShape.PointingHandCursor)
#         card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
#
#         layout = QHBoxLayout(card)
#         layout.setContentsMargins(35, 30, 35, 30)
#         layout.setSpacing(25)
#
#         # Иконка с фоном
#         icon_container = QFrame()
#         icon_container.setFixedSize(90, 90)
#         icon_container.setStyleSheet(f"background-color: {bg_color}; border-radius: 15px;")
#
#         icon_layout = QVBoxLayout(icon_container)
#         icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#
#         # PNG иконка
#         icon_label = self.create_icon_label(icon_file, size=50)
#         icon_layout.addWidget(icon_label)
#
#         # Текст
#         text_layout = QVBoxLayout()
#         text_layout.setSpacing(12)
#
#         title_label = QLabel(title)
#         title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
#         title_label.setStyleSheet("color: #1F2937;")
#         title_label.setWordWrap(True)
#
#         desc_label = QLabel(description)
#         desc_label.setFont(QFont("Segoe UI", 12))
#         desc_label.setStyleSheet("color: #6B7280;")
#         desc_label.setWordWrap(True)
#
#         text_layout.addWidget(title_label)
#         text_layout.addWidget(desc_label)
#
#         layout.addWidget(icon_container)
#         layout.addLayout(text_layout)
#         layout.addStretch()
#
#         # Стрелка
#         arrow = QLabel("→")
#         arrow.setFont(QFont("Segoe UI", 28))
#         arrow.setStyleSheet("color: #9CA3AF;")
#         layout.addWidget(arrow)
#
#         # Подключение клика
#         card.mousePressEvent = lambda event, t=title: self.on_card_click(t)
#
#         return card
#
#     def on_card_click(self, card_title):
#         """Обработчик клика на карточку"""
#         if card_title == "Создание новой заявки":
#             # Переход на экран создания заявки
#             print("Переход к созданию заявки")
#         elif card_title == "История заявок":
#             print("Переход к истории заявок")
#         elif card_title == "Справочник товаров":
#             print("Переход к справочнику товаров")
#
#     def apply_styles(self):
#         """Применение стилей (CSS)"""
#         self.setStyleSheet(get_main_page_styles())
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     app.setFont(QFont("Segoe UI", 10))
#
#     # Для тестирования создаем временное окно
#     from PyQt6.QtWidgets import QMainWindow
#
#     window = QMainWindow()
#     window.setWindowTitle("Тест: Главная страница")
#     window.setGeometry(100, 100, 1400, 900)
#
#     icons_path = Path(__file__).parent / "icons"
#     page = MainPage(icons_path)
#     window.setCentralWidget(page)
#
#     window.show()
#     sys.exit(app.exec())

"""
Главная страница приложения
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from ui.utils.styles import get_main_page_styles


class MainPage(QWidget):
    def __init__(self, icons_path, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path
        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        """Создание контента главной страницы (БЕЗ сайдбара)"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(30)

        # Заголовок страницы
        title = QLabel("Главная")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")

        subtitle = QLabel("Добро пожаловать в систему автоматизации закупок ЦМИТ ЛЮКС")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #6B7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        # Сетка карточек
        cards_widget = QWidget()
        cards_layout = QGridLayout(cards_widget)
        cards_layout.setSpacing(25)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        # Данные карточек (Выход удален, так как есть глобальная кнопка)
        cards_data = [
            ("add.png", "Создание новой заявки", "Создайте новую заявку на закупку товаров", "#3B82F6", "#EFF6FF"),
            ("search.png", "История заявок", "Просмотрите ваши предыдущие заявки", "#10B981", "#D1FAE5"),
            ("product.png", "Справочник товаров", "Просмотрите или редактируйте актуальные товары предприятия",
             "#8B5CF6", "#FFFACD"),
        ]

        for i, (icon_file, title_text, description, icon_color, bg_color) in enumerate(cards_data):
            card = self.create_card(icon_file, title_text, description, bg_color)
            row = i // 2
            col = i % 2
            cards_layout.addWidget(card, row, col)

        layout.addWidget(cards_widget)
        layout.addStretch()

    def create_card(self, icon_file, title, description, bg_color):
        """Создание карточки"""
        card = QFrame()
        card.setObjectName("card")
        card.setFixedHeight(200)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(25)

        # Иконка с фоном
        icon_container = QFrame()
        icon_container.setFixedSize(90, 90)
        icon_container.setStyleSheet(f"background-color: {bg_color}; border-radius: 15px;")

        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = self.create_icon_label(icon_file, size=50)
        icon_layout.addWidget(icon_label)

        # Текст
        text_layout = QVBoxLayout()
        text_layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1F2937;")
        title_label.setWordWrap(True)

        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 12))
        desc_label.setStyleSheet("color: #6B7280;")
        desc_label.setWordWrap(True)

        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)

        layout.addWidget(icon_container)
        layout.addLayout(text_layout)
        layout.addStretch()

        # Стрелка
        arrow = QLabel("→")
        arrow.setFont(QFont("Segoe UI", 28))
        arrow.setStyleSheet("color: #9CA3AF;")
        layout.addWidget(arrow)

        # Подключение клика
        card.mousePressEvent = lambda event, t=title: self.on_card_click(t)

        return card

    def create_icon_label(self, filename, size=24):
        """Создание QLabel с иконкой"""
        label = QLabel()
        icon_path = self.icons_path / filename

        if icon_path.exists():
            pixmap = QPixmap(str(icon_path))
            scaled_pixmap = pixmap.scaled(size, size,
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            label.setPixmap(scaled_pixmap)
        else:
            print(f"!!! Иконка не найдена: {icon_path}")

        label.setFixedSize(size, size)
        return label

    def navigate_to(self, page_name):
        """Переключение страницы через родительское окно"""
        parent = self.parent()
        while parent is not None:
            if hasattr(parent, 'switch_page'):
                parent.switch_page(page_name)
                return
            parent = parent.parent()

    def on_card_click(self, card_title):
        """Обработчик клика на карточку"""
        if card_title == "Создание новой заявки":
            self.navigate_to("Создать заявку")
        elif card_title == "История заявок":
            self.navigate_to("История заявок")
        elif card_title == "Справочник товаров":
            self.navigate_to("Справочник товаров")

    def apply_styles(self):
        """Применение стилей"""
        self.setStyleSheet(get_main_page_styles())


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     app.setFont(QFont("Segoe UI", 10))
#
#     # Для тестирования создаем временное окно
#     from PyQt6.QtWidgets import QMainWindow
#
#     window = QMainWindow()
#     window.setWindowTitle("Тест: Главная страница")
#     window.setGeometry(100, 100, 1400, 900)
#
#     icons_path = Path(__file__).parent / "icons"
#     page = MainPage(icons_path)
#     window.setCentralWidget(page)
#
#     window.show()
#     sys.exit(app.exec())