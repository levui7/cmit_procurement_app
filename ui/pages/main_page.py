# # import sys
# # from pathlib import Path
# # from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
# #                              QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout,
# #                              QSizePolicy, QDialog)
# # from PyQt6.QtCore import Qt, QSize
# # from PyQt6.QtGui import QFont, QPixmap, QIcon
# #
# # from ui.styles import get_main_page_styles
# #
# # class MainPage(QWidget):
# #     def __init__(self, icons_path, parent=None):
# #         super().__init__(parent)
# #         self.icons_path = icons_path
# #         self.create_widgets()
# #         self.apply_styles()
# #
# #     def create_icon_label(self, filename, size=24):
# #         """Создание QLabel с иконкой"""
# #         label = QLabel()
# #         pixmap = self.load_icon(filename, size)
# #         label.setPixmap(pixmap)
# #         label.setFixedSize(size, size)
# #         return label
# #
# #     def create_widgets(self):
# #         """Создание контента главной страницы (БЕЗ сайдбара)"""
# #         layout = QVBoxLayout(self)
# #         layout.setContentsMargins(50, 40, 50, 40)
# #         layout.setSpacing(30)
# #
# #         # Заголовок страницы
# #         title = QLabel("Главная")
# #         title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
# #         title.setStyleSheet("color: #1F2937;")
# #
# #         subtitle = QLabel("Добро пожаловать в систему автоматизации закупок ЦМИТ ЛЮКС")
# #         subtitle.setFont(QFont("Segoe UI", 13))
# #         subtitle.setStyleSheet("color: #6B7280;")
# #
# #         layout.addWidget(title)
# #         layout.addWidget(subtitle)
# #         layout.addSpacing(20)
# #
# #         # Сетка карточек (2x2)
# #         cards_widget = QWidget()
# #         cards_layout = QGridLayout(cards_widget)
# #         cards_layout.setSpacing(25)
# #         cards_layout.setContentsMargins(0, 0, 0, 0)
# #
# #         # Данные карточек (УДАЛИЛИ "Выход из приложения", так как есть общая кнопка)
# #         cards_data = [
# #             ("add.png", "Создание новой заявки", "Создайте новую заявку на закупку товаров", "#3B82F6", "#EFF6FF"),
# #             ("search.png", "История заявок", "Просмотрите ваши предыдущие заявки", "#10B981", "#D1FAE5"),
# #             ("product.png", "Справочник товаров", "Просмотрите или редактируйте актуальные товары предприятия",
# #              "#8B5CF6", "#FFFACD"),
# #         ]
# #
# #         for i, (icon_file, title_text, description, icon_color, bg_color) in enumerate(cards_data):
# #             card = self.create_card(icon_file, title_text, description, bg_color)
# #             row = i // 2
# #             col = i % 2
# #             cards_layout.addWidget(card, row, col)
# #
# #         layout.addWidget(cards_widget)
# #         layout.addStretch()
# #
# #     def navigate_to(self, page_name):
# #         """Переключение страницы через родительское окно (AppWindow)"""
# #         parent = self.parent()
# #         while parent is not None:
# #             if hasattr(parent, 'switch_page'):
# #                 parent.switch_page(page_name)
# #                 return
# #             parent = parent.parent()
# #
# #     def create_card(self, icon_file, title, description, bg_color):
# #         """Создание карточки с PNG иконкой"""
# #         card = QFrame()
# #         card.setObjectName("card")
# #         card.setFixedHeight(200)
# #         card.setCursor(Qt.CursorShape.PointingHandCursor)
# #         card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
# #
# #         layout = QHBoxLayout(card)
# #         layout.setContentsMargins(35, 30, 35, 30)
# #         layout.setSpacing(25)
# #
# #         # Иконка с фоном
# #         icon_container = QFrame()
# #         icon_container.setFixedSize(90, 90)
# #         icon_container.setStyleSheet(f"background-color: {bg_color}; border-radius: 15px;")
# #
# #         icon_layout = QVBoxLayout(icon_container)
# #         icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
# #
# #         # PNG иконка
# #         icon_label = self.create_icon_label(icon_file, size=50)
# #         icon_layout.addWidget(icon_label)
# #
# #         # Текст
# #         text_layout = QVBoxLayout()
# #         text_layout.setSpacing(12)
# #
# #         title_label = QLabel(title)
# #         title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
# #         title_label.setStyleSheet("color: #1F2937;")
# #         title_label.setWordWrap(True)
# #
# #         desc_label = QLabel(description)
# #         desc_label.setFont(QFont("Segoe UI", 12))
# #         desc_label.setStyleSheet("color: #6B7280;")
# #         desc_label.setWordWrap(True)
# #
# #         text_layout.addWidget(title_label)
# #         text_layout.addWidget(desc_label)
# #
# #         layout.addWidget(icon_container)
# #         layout.addLayout(text_layout)
# #         layout.addStretch()
# #
# #         # Стрелка
# #         arrow = QLabel("→")
# #         arrow.setFont(QFont("Segoe UI", 28))
# #         arrow.setStyleSheet("color: #9CA3AF;")
# #         layout.addWidget(arrow)
# #
# #         # Подключение клика
# #         card.mousePressEvent = lambda event, t=title: self.on_card_click(t)
# #
# #         return card
# #
# #     def on_card_click(self, card_title):
# #         """Обработчик клика на карточку"""
# #         if card_title == "Создание новой заявки":
# #             # Переход на экран создания заявки
# #             print("Переход к созданию заявки")
# #         elif card_title == "История заявок":
# #             print("Переход к истории заявок")
# #         elif card_title == "Справочник товаров":
# #             print("Переход к справочнику товаров")
# #
# #     def apply_styles(self):
# #         """Применение стилей (CSS)"""
# #         self.setStyleSheet(get_main_page_styles())
# #
# #
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     app.setStyle("Fusion")
# #     app.setFont(QFont("Segoe UI", 10))
# #
# #     # Для тестирования создаем временное окно
# #     from PyQt6.QtWidgets import QMainWindow
# #
# #     window = QMainWindow()
# #     window.setWindowTitle("Тест: Главная страница")
# #     window.setGeometry(100, 100, 1400, 900)
# #
# #     icons_path = Path(__file__).parent / "icons"
# #     page = MainPage(icons_path)
# #     window.setCentralWidget(page)
# #
# #     window.show()
# #     sys.exit(app.exec())


"""
Главная страница приложения
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.utils.config import Colors, Fonts, Spacing, Sizes
from ui.utils.icons import create_icon_label, IconNames
from ui.utils.styles import get_main_page_styles


class MainPage(QWidget):
    def __init__(self, icons_path=None, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path  # Оставлен для обратной совместимости, но не используется напрямую
        self.create_widgets()
        self.apply_styles()

    # def create_widgets(self):
    #     """Создание контента главной страницы"""
    #     layout = QVBoxLayout(self)
    #     layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
    #     layout.setSpacing(Spacing.XL)
    #
    #     # Заголовок страницы
    #     title = QLabel("Главная")
    #     title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_DISPLAY, QFont.Weight.Bold))
    #     title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
    #
    #     subtitle = QLabel("Добро пожаловать в систему автоматизации закупок ЦМИТ ЛЮКС")
    #     subtitle.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
    #     subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
    #
    #     layout.addWidget(title)
    #     layout.addWidget(subtitle)
    #     layout.addSpacing(Spacing.LG)
    #
    #     # Сетка карточек
    #     cards_widget = QWidget()
    #     cards_layout = QGridLayout(cards_widget)
    #     cards_layout.setSpacing(Spacing.LG)
    #     cards_layout.setContentsMargins(0, 0, 0, 0)
    #
    #     # Данные карточек (используем константы из config и icons)
    #     # Формат: (IconName, Заголовок, Описание, Цвет_иконки, Цвет_фона)
    #     cards_data = [
    #         (IconNames.ADD, "Создание новой заявки", "Создайте новую заявку на закупку товаров", Colors.PRIMARY, Colors.PRIMARY_LIGHT),
    #         (IconNames.SEARCH, "История заявок", "Просмотрите ваши предыдущие заявки", Colors.SUCCESS, Colors.SUCCESS_LIGHT),
    #         (IconNames.PRODUCT, "Справочник товаров", "Просмотрите или редактируйте актуальные товары предприятия", "#8B5CF6", Colors.PURPLE_LIGHT),
    #     ]
    #
    #     for i, (icon_name, title_text, description, icon_color, bg_color) in enumerate(cards_data):
    #         card = self.create_card(icon_name, title_text, description, bg_color)
    #         row = i // 2
    #         col = i % 2
    #         cards_layout.addWidget(card, row, col)
    #
    #     layout.addWidget(cards_widget)
    #     layout.addStretch()

    def create_widgets(self):
        """Создание контента главной страницы (БЕЗ сайдбара)"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
        layout.setSpacing(Spacing.XL)

        # Заголовок страницы
        title = QLabel("Главная")
        title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_DISPLAY, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")

        subtitle = QLabel("Добро пожаловать в систему автоматизации закупок ЦМИТ ЛЮКС")
        subtitle.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(Spacing.LG)

        # === УРОВЕНЬ 1: Создание заявки + Активная заявка ===
        top_cards_widget = QWidget()
        top_cards_layout = QGridLayout(top_cards_widget)
        top_cards_layout.setSpacing(Spacing.LG)
        top_cards_layout.setContentsMargins(0, 0, 0, 0)

        # Данные карточек первого уровня
        top_cards_data = [
            (IconNames.ADD, "Создание новой заявки", "Создайте новую заявку на закупку товаров", Colors.PURPLE_LIGHT),
            (IconNames.ACTIVE_REQUEST, "Активная заявка", "Просмотрите результаты обработки последней заявки", Colors.WARNING_LIGHT),
        ]

        for i, (icon_name, title_text, description, bg_color) in enumerate(top_cards_data):
            card = self.create_card(icon_name, title_text, description, bg_color)
            top_cards_layout.addWidget(card, 0, i)  # Все карточки в первой строке

        layout.addWidget(top_cards_widget)

        # === УРОВЕНЬ 2: История заявок + Справочник товаров ===
        bottom_cards_widget = QWidget()
        bottom_cards_layout = QGridLayout(bottom_cards_widget)
        bottom_cards_layout.setSpacing(Spacing.LG)
        bottom_cards_layout.setContentsMargins(0, 0, 0, 0)

        # Данные карточек второго уровня
        bottom_cards_data = [
            (IconNames.SEARCH, "История заявок", "Просмотрите ваши предыдущие заявки", Colors.SUCCESS_LIGHT),
            # ← Перемещена сюда
            (IconNames.PRODUCT, "Справочник товаров", "Просмотрите или редактируйте актуальные товары предприятия",
             Colors.ORANGE_LIGHT),
        ]

        for i, (icon_name, title_text, description, bg_color) in enumerate(bottom_cards_data):
            card = self.create_card(icon_name, title_text, description, bg_color)
            bottom_cards_layout.addWidget(card, 0, i)

        layout.addWidget(bottom_cards_widget)
        layout.addStretch()

    def create_card(self, icon_name, title, description, bg_color):
        """Создание интерактивной карточки"""
        card = QFrame()
        card.setObjectName("card")
        card.setFixedHeight(200)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(Spacing.XL, Spacing.LG, Spacing.XL, Spacing.LG)
        layout.setSpacing(Spacing.LG)

        # Иконка с цветным фоном
        icon_container = QFrame()
        icon_container.setFixedSize(90, 90)
        # Используем константу радиуса из config
        icon_container.setStyleSheet(f"background-color: {bg_color}; border-radius: {Sizes.CARD_RADIUS}px;")

        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        # Используем глобальную функцию создания иконки (размер 64px идеально вписывается в 90x90)
        icon_label = create_icon_label(icon_name, size=64)
        icon_layout.addWidget(icon_label)

        # Текстовый блок
        text_layout = QVBoxLayout()
        text_layout.setSpacing(Spacing.SM)

        title_label = QLabel(title)
        title_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        title_label.setWordWrap(True)

        desc_label = QLabel(description)
        desc_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        desc_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        desc_label.setWordWrap(True)

        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)

        layout.addWidget(icon_container)
        layout.addLayout(text_layout)
        layout.addStretch()

        # Стрелка-указатель
        arrow = QLabel("→")
        arrow.setFont(QFont(Fonts.FAMILY, Sizes.ICON_XLARGE))  # 48px
        arrow.setStyleSheet(f"color: {Colors.TEXT_MUTED};")
        layout.addWidget(arrow)

        # Подключение клика (передаем заголовок для навигации)
        card.mousePressEvent = lambda event, t=title: self.on_card_click(t)

        return card

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

        elif card_title == "Активная заявка":
            # ✅ Получаем ID активной заявки через реальную сессию
            from backend.crud.crud_settings import get_app_setting
            from backend.database import get_session

            db = get_session()
            try:
                active_request_id_str = get_app_setting(db, "active_request_id")
            finally:
                db.close()

            if active_request_id_str:
                try:
                    active_request_id = int(active_request_id_str)
                except (ValueError, TypeError):
                    active_request_id = None

                if active_request_id:
                    parent = self.parent()
                    while parent is not None:
                        if hasattr(parent, 'switch_page'):
                            parent.current_request_id = active_request_id
                            parent.switch_page("Активная заявка")
                            return
                        parent = parent.parent()
                else:
                    QMessageBox.information(self, "Информация", "Нет активной заявки")
            else:
                QMessageBox.information(self, "Информация", "Нет активной заявки")

        elif card_title == "История заявок":
            self.navigate_to("История заявок")
        elif card_title == "Справочник товаров":
            self.navigate_to("Справочник товаров")

    def apply_styles(self):
        """Применение стилей"""
        self.setStyleSheet(get_main_page_styles())

#
# """
# Главная страница приложения
# """
# from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#                              QFrame, QGridLayout, QSizePolicy)
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont, QPixmap
# from ui.utils.styles import get_main_page_styles
#
#
# class MainPage(QWidget):
#     def __init__(self, icons_path, parent=None):
#         super().__init__(parent)
#         self.icons_path = icons_path
#         self.create_widgets()
#         self.apply_styles()
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
#         # Сетка карточек
#         cards_widget = QWidget()
#         cards_layout = QGridLayout(cards_widget)
#         cards_layout.setSpacing(25)
#         cards_layout.setContentsMargins(0, 0, 0, 0)
#
#         # Данные карточек (Выход удален, так как есть глобальная кнопка)
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
#     def create_card(self, icon_file, title, description, bg_color):
#         """Создание карточки"""
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
#     def create_icon_label(self, filename, size=24):
#         """Создание QLabel с иконкой"""
#         label = QLabel()
#         icon_path = self.icons_path / filename
#
#         if icon_path.exists():
#             pixmap = QPixmap(str(icon_path))
#             scaled_pixmap = pixmap.scaled(size, size,
#                                           Qt.AspectRatioMode.KeepAspectRatio,
#                                           Qt.TransformationMode.SmoothTransformation)
#             label.setPixmap(scaled_pixmap)
#         else:
#             print(f"!!! Иконка не найдена: {icon_path}")
#
#         label.setFixedSize(size, size)
#         return label
#
#     def navigate_to(self, page_name):
#         """Переключение страницы через родительское окно"""
#         parent = self.parent()
#         while parent is not None:
#             if hasattr(parent, 'switch_page'):
#                 parent.switch_page(page_name)
#                 return
#             parent = parent.parent()
#
#     def on_card_click(self, card_title):
#         """Обработчик клика на карточку"""
#         if card_title == "Создание новой заявки":
#             self.navigate_to("Создать заявку")
#         elif card_title == "История заявок":
#             self.navigate_to("История заявок")
#         elif card_title == "Справочник товаров":
#             self.navigate_to("Справочник товаров")
#
#     def apply_styles(self):
#         """Применение стилей"""
#         self.setStyleSheet(get_main_page_styles())
#
#
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     app.setStyle("Fusion")
# #     app.setFont(QFont("Segoe UI", 10))
# #
# #     # Для тестирования создаем временное окно
# #     from PyQt6.QtWidgets import QMainWindow
# #
# #     window = QMainWindow()
# #     window.setWindowTitle("Тест: Главная страница")
# #     window.setGeometry(100, 100, 1400, 900)
# #
# #     icons_path = Path(__file__).parent / "icons"
# #     page = MainPage(icons_path)
# #     window.setCentralWidget(page)
# #
# #     window.show()
# #     sys.exit(app.exec())