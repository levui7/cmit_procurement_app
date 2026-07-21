"""
Страница истории закупок
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.utils.config import Colors, Fonts, Spacing, Sizes
from ui.utils.icons import create_icon_label, IconNames
from ui.utils.styles import get_history_styles
from backend.crud.crud_procurement import get_all_requests

from backend.crud.crud_procurement import get_all_requests  # Импортируем CRUD-операцию
from backend.database import get_session

class HistoryRequestPage(QWidget):
    def __init__(self, icons_path=None, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path
        self.create_widgets()
        self.apply_styles()
        self.load_history()

    def create_widgets(self):
        """Создание интерфейса страницы"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
        layout.setSpacing(Spacing.XL)

        # Заголовок страницы
        title = QLabel("История закупок")
        title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_DISPLAY, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")

        subtitle = QLabel("Просматривайте информацию о прошлых закупках")
        subtitle.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(Spacing.SM)

        # Скроллируемая область для карточек
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(Spacing.SM)

        scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(scroll_area)

        # Нижняя панель: кнопка "Назад" + пагинация
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(Spacing.LG)

        # Кнопка "Назад"
        back_btn = QPushButton("← Назад")
        back_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        back_btn.setFixedSize(130, Sizes.INPUT_HEIGHT)
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.go_back)

        bottom_layout.addWidget(back_btn)
        bottom_layout.addStretch()

        # Информация о пагинации
        self.pagination_info = QLabel("0 закупок")
        self.pagination_info.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        self.pagination_info.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        bottom_layout.addWidget(self.pagination_info)

        # Кнопки пагинации
        self.pagination = self.create_pagination()
        bottom_layout.addWidget(self.pagination)

        layout.addLayout(bottom_layout)

    def load_history(self):
        """Загрузка истории закупок из БД"""
        # Получаем все заявки из БД
        db = get_session()
        requests = get_all_requests(db)

        # Очищаем текущий список
        self._clear_history_cards()

        # Создаем карточки для каждой заявки
        for request in requests:
            # Формируем данные для карточки
            data = {
                'id': request.id,
                'number': request.number,
                'date': request.created_at.strftime("%d.%m.%Y") if request.created_at else "N/A",
                'time': request.created_at.strftime("%H:%M") if request.created_at else "N/A",
                'description': request.description or "Без описания",
                'amount': f"{request.total_amount:,.0f} ₽" if request.total_amount else "0 ₽",
                'items_count': len(request.items) if request.items else 0,
                'status': request.status
            }

            card = self.create_history_card(data)
            self.scroll_layout.addWidget(card)

        self.scroll_layout.addStretch()
        self._update_pagination_info(len(requests))

    def _clear_history_cards(self):
        """Очистить все карточки истории"""
        # Удаляем все виджеты кроме растягивателя
        while self.scroll_layout.count() > 0:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _update_pagination_info(self, total_count):
        """Обновить информацию о пагинации"""
        if total_count == 0:
            self.pagination_info.setText("0 закупок")
        else:
            self.pagination_info.setText(f"1–{total_count} из {total_count} закупок")

    def create_history_card(self, data):
        """Создание карточки одной закупки"""
        card = QFrame()
        card.setObjectName("historyCard")
        card.setFixedHeight(110)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(Spacing.LG, Spacing.SM, Spacing.LG, Spacing.SM)
        layout.setSpacing(Spacing.LG)

        # Блок с датой и иконкой календаря
        date_block = QFrame()
        date_block.setObjectName("dateBlock")
        date_block.setFixedSize(90, 70)

        date_layout = QVBoxLayout(date_block)
        date_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_layout.setSpacing(2)

        # Иконка календаря через IconNames
        icon_label = create_icon_label(IconNames.CALENDAR, size=28)
        date_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        date_text = QLabel(f"{data['date']}\n{data['time']}")
        date_text.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_XSMALL))
        date_text.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        date_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_layout.addWidget(date_text)

        layout.addWidget(date_block)

        # Разделитель
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.VLine)
        separator1.setStyleSheet(f"background-color: {Colors.BORDER};")
        separator1.setFixedWidth(1)
        layout.addWidget(separator1)

        # Номер закупки и описание
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        number_label = QLabel(f"Закупка №{data['number']}")
        number_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        number_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")

        desc_label = QLabel(data['description'])
        desc_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        desc_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")

        info_layout.addWidget(number_label)
        info_layout.addWidget(desc_label)

        layout.addLayout(info_layout)

        # Разделитель
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.VLine)
        separator2.setStyleSheet(f"background-color: {Colors.BORDER};")
        separator2.setFixedWidth(1)
        layout.addWidget(separator2)

        # Сумма
        amount_layout = QVBoxLayout()
        amount_layout.setSpacing(3)

        amount_title = QLabel("Сумма")
        amount_title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        amount_title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")

        amount_value = QLabel(data['amount'])
        amount_value.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        amount_value.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")

        amount_layout.addWidget(amount_title)
        amount_layout.addWidget(amount_value)

        layout.addLayout(amount_layout)

        # Разделитель
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.Shape.VLine)
        separator3.setStyleSheet(f"background-color: {Colors.BORDER};")
        separator3.setFixedWidth(1)
        layout.addWidget(separator3)

        # Количество товаров
        items_layout = QVBoxLayout()
        items_layout.setSpacing(3)

        items_title = QLabel("Товаров")
        items_title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        items_title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")

        items_value = QLabel(str(data['items_count']))
        items_value.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        items_value.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")

        items_layout.addWidget(items_title)
        items_layout.addWidget(items_value)

        layout.addLayout(items_layout)

        layout.addStretch()

        # Кнопки действий
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(Spacing.SM)

        # Кнопка "Открыть"
        open_btn = QPushButton("Открыть")
        open_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        open_btn.setFixedSize(100, Sizes.BUTTON_HEIGHT_SMALL)
        open_btn.setObjectName("openButton")
        open_btn.clicked.connect(lambda: self.open_procurement(data['id']))

        # Кнопка "Экспорт"
        export_btn = QPushButton("Экспорт")
        export_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        export_btn.setFixedSize(100, Sizes.BUTTON_HEIGHT_SMALL)
        export_btn.setObjectName("exportButton")
        export_btn.clicked.connect(lambda: self.export_procurement(data['id']))

        # Кнопка "Удалить"
        delete_btn = QPushButton("Удалить")
        delete_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        delete_btn.setFixedSize(100, Sizes.BUTTON_HEIGHT_SMALL)
        delete_btn.setObjectName("deleteButton")
        delete_btn.clicked.connect(lambda: self.delete_procurement(data['id']))

        buttons_layout.addWidget(open_btn)
        buttons_layout.addWidget(export_btn)
        buttons_layout.addWidget(delete_btn)

        layout.addLayout(buttons_layout)

        return card

    def create_pagination(self):
        """Создание блока пагинации"""
        pagination = QFrame()
        pagination.setObjectName("pagination")

        layout = QHBoxLayout(pagination)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        # Кнопки пагинации
        pages = ["<", "1", "2", "3", "...", "5", ">"]

        for page in pages:
            btn = QPushButton(page)
            btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
            btn.setFixedSize(Sizes.PAGINATION_BUTTON_SIZE, Sizes.PAGINATION_BUTTON_SIZE)

            if page == "1":
                btn.setObjectName("currentPage")
            elif page in ["<", ">"]:
                btn.setObjectName("navButton")
            else:
                btn.setObjectName("pageButton")

            layout.addWidget(btn)

        return pagination

    def open_procurement(self, request_id):
        """Открыть закупку"""
        print(f"Открытие закупки ID: {request_id}")
        # TODO: Открыть детальную страницу заявки

    def export_procurement(self, request_id):
        """Экспорт закупки"""
        print(f"Экспорт закупки ID: {request_id}")
        QMessageBox.information(self, "Экспорт", f"Экспорт заявки #{request_id} будет реализован позже")

    def delete_procurement(self, request_id):
        """Удалить закупку"""
        print(f"Удаление закупки ID: {request_id}")
        QMessageBox.information(self, "Удаление", f"Удаление заявки #{request_id} будет реализовано позже")

    def go_back(self):
        """Вернуться на главную страницу"""
        parent = self.parent()
        while parent is not None:
            if hasattr(parent, 'switch_page'):
                parent.switch_page("Главная")
                return
            parent = parent.parent()

    def apply_styles(self):
        """Применение стилей"""
        self.setStyleSheet(get_history_styles())

# from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#                              QPushButton, QFrame, QScrollArea)
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont, QPixmap
#
# from ui.utils.styles import get_history_styles
#
# class HistoryRequestPage(QWidget):
#     def __init__(self, icons_path, parent=None):
#         super().__init__(parent)
#         self.icons_path = icons_path
#         self.create_widgets()
#         self.apply_styles()
#
#     def create_widgets(self):
#         # Основной контент
#         content_layout = QVBoxLayout()
#         content_layout.setContentsMargins(50, 40, 50, 40)
#         content_layout.setSpacing(30)
#
#         # Заголовок страницы
#         title = QLabel("История закупок")
#         title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
#         title.setStyleSheet("color: #1F2937;")
#
#         subtitle = QLabel("Просматривайте информацию о прошлых закупках")
#         subtitle.setFont(QFont("Segoe UI", 13))
#         subtitle.setStyleSheet("color: #6B7280;")
#
#         content_layout.addWidget(title)
#         content_layout.addWidget(subtitle)
#         content_layout.addSpacing(10)
#
#         # Скроллируемая область для карточек
#         scroll_area = QScrollArea()
#         scroll_area.setWidgetResizable(True)
#         scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
#
#         scroll_widget = QWidget()
#         scroll_layout = QVBoxLayout(scroll_widget)
#         scroll_layout.setContentsMargins(0, 0, 0, 0)
#         scroll_layout.setSpacing(15)
#
#         # Мок-данные для истории закупок
#         history_data = [
#             {
#                 "date": "15.06.2024",
#                 "time": "10:30",
#                 "number": "125",
#                 "description": "Канцелярские товары для офиса",
#                 "amount": "45 230 ₽",
#                 "items_count": 12,
#             },
#             {
#                 "date": "10.06.2024",
#                 "time": "14:15",
#                 "number": "124",
#                 "description": "Расходные материалы для принтеров",
#                 "amount": "18 750 ₽",
#                 "items_count": 7,
#             },
#             {
#                 "date": "05.06.2024",
#                 "time": "09:20",
#                 "number": "123",
#                 "description": "Электротехническая продукция",
#                 "amount": "76 890 ₽",
#                 "items_count": 15,
#             },
#             {
#                 "date": "28.05.2024",
#                 "time": "16:45",
#                 "number": "122",
#                 "description": "Хозяйственные товары",
#                 "amount": "9 430 ₽",
#                 "items_count": 5,
#             },
#             {
#                 "date": "21.05.2024",
#                 "time": "11:05",
#                 "number": "121",
#                 "description": "Компьютерная периферия",
#                 "amount": "34 560 ₽",
#                 "items_count": 9,
#             },
#         ]
#
#         # Создаем карточки закупок
#         for data in history_data:
#             card = self.create_history_card(data)
#             scroll_layout.addWidget(card)
#
#         scroll_layout.addStretch()
#         scroll_area.setWidget(scroll_widget)
#
#         content_layout.addWidget(scroll_area)
#
#         # Нижняя панель: кнопка "Назад" + пагинация
#         bottom_layout = QHBoxLayout()
#         bottom_layout.setSpacing(20)
#
#         # Кнопка "Назад"
#         back_btn = QPushButton("← Назад")
#         back_btn.setFont(QFont("Segoe UI", 12))
#         back_btn.setFixedSize(130, 40)
#         back_btn.setObjectName("backButton")
#         back_btn.clicked.connect(self.go_back)
#
#         bottom_layout.addWidget(back_btn)
#         bottom_layout.addStretch()
#
#         # Информация о пагинации
#         pagination_info = QLabel("1–5 из 25 закупок")
#         pagination_info.setFont(QFont("Segoe UI", 11))
#         pagination_info.setStyleSheet("color: #6B7280;")
#         bottom_layout.addWidget(pagination_info)
#
#         # Кнопки пагинации
#         pagination = self.create_pagination()
#         bottom_layout.addWidget(pagination)
#
#         content_layout.addLayout(bottom_layout)
#         self.setLayout(content_layout)
#
#     def create_history_card(self, data):
#         """Создание карточки одной закупки"""
#         card = QFrame()
#         card.setObjectName("historyCard")
#         card.setFixedHeight(110)
#
#         layout = QHBoxLayout(card)
#         layout.setContentsMargins(25, 20, 25, 20)
#         layout.setSpacing(20)
#
#         # Блок с датой и иконкой календаря
#         date_block = QFrame()
#         date_block.setObjectName("dateBlock")
#         date_block.setFixedSize(90, 70)
#
#         date_layout = QVBoxLayout(date_block)
#         date_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         date_layout.setSpacing(2)
#
#         icon_label = self.create_icon_label("calendar.png", size=28)
#         date_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         date_text = QLabel(f"{data['date']}\n{data['time']}")
#         date_text.setFont(QFont("Segoe UI", 9))
#         date_text.setStyleSheet("color: #6B7280;")
#         date_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         date_layout.addWidget(date_text)
#
#         layout.addWidget(date_block)
#
#         # Разделитель
#         separator1 = QFrame()
#         separator1.setFrameShape(QFrame.Shape.VLine)
#         separator1.setStyleSheet("background-color: #E5E7EB;")
#         separator1.setFixedWidth(1)
#         layout.addWidget(separator1)
#
#         # Номер закупки и описание
#         info_layout = QVBoxLayout()
#         info_layout.setSpacing(5)
#
#         number_label = QLabel(f"Закупка №{data['number']}")
#         number_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
#         number_label.setStyleSheet("color: #1F2937;")
#
#         desc_label = QLabel(data['description'])
#         desc_label.setFont(QFont("Segoe UI", 11))
#         desc_label.setStyleSheet("color: #6B7280;")
#
#         info_layout.addWidget(number_label)
#         info_layout.addWidget(desc_label)
#
#         layout.addLayout(info_layout)
#
#         # Разделитель
#         separator2 = QFrame()
#         separator2.setFrameShape(QFrame.Shape.VLine)
#         separator2.setStyleSheet("background-color: #E5E7EB;")
#         separator2.setFixedWidth(1)
#         layout.addWidget(separator2)
#
#         # Сумма
#         amount_layout = QVBoxLayout()
#         amount_layout.setSpacing(3)
#
#         amount_title = QLabel("Сумма")
#         amount_title.setFont(QFont("Segoe UI", 10))
#         amount_title.setStyleSheet("color: #6B7280;")
#
#         amount_value = QLabel(data['amount'])
#         amount_value.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
#         amount_value.setStyleSheet("color: #1F2937;")
#
#         amount_layout.addWidget(amount_title)
#         amount_layout.addWidget(amount_value)
#
#         layout.addLayout(amount_layout)
#
#         # Разделитель
#         separator3 = QFrame()
#         separator3.setFrameShape(QFrame.Shape.VLine)
#         separator3.setStyleSheet("background-color: #E5E7EB;")
#         separator3.setFixedWidth(1)
#         layout.addWidget(separator3)
#
#         # Количество товаров
#         items_layout = QVBoxLayout()
#         items_layout.setSpacing(3)
#
#         items_title = QLabel("Товаров")
#         items_title.setFont(QFont("Segoe UI", 10))
#         items_title.setStyleSheet("color: #6B7280;")
#
#         items_value = QLabel(str(data['items_count']))
#         items_value.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
#         items_value.setStyleSheet("color: #1F2937;")
#
#         items_layout.addWidget(items_title)
#         items_layout.addWidget(items_value)
#
#         layout.addLayout(items_layout)
#
#         layout.addStretch()
#
#         # Кнопки действий
#         buttons_layout = QHBoxLayout()
#         buttons_layout.setSpacing(10)
#
#         # Кнопка "Открыть"
#         open_btn = QPushButton("Открыть")
#         open_btn.setFont(QFont("Segoe UI", 11))
#         open_btn.setFixedSize(100, 35)
#         open_btn.setObjectName("openButton")
#         open_btn.clicked.connect(lambda: self.open_procurement(data['number']))
#
#         # Кнопка "Экспорт"
#         export_btn = QPushButton("Экспорт")
#         export_btn.setFont(QFont("Segoe UI", 11))
#         export_btn.setFixedSize(100, 35)
#         export_btn.setObjectName("exportButton")
#         export_btn.clicked.connect(lambda: self.export_procurement(data['number']))
#
#         # Кнопка "Удалить"
#         delete_btn = QPushButton("Удалить")
#         delete_btn.setFont(QFont("Segoe UI", 11))
#         delete_btn.setFixedSize(100, 35)
#         delete_btn.setObjectName("deleteButton")
#         delete_btn.clicked.connect(lambda: self.delete_procurement(data['number']))
#
#         buttons_layout.addWidget(open_btn)
#         buttons_layout.addWidget(export_btn)
#         buttons_layout.addWidget(delete_btn)
#
#         layout.addLayout(buttons_layout)
#
#         return card
#
#     def create_pagination(self):
#         """Создание блока пагинации"""
#         pagination = QFrame()
#         pagination.setObjectName("pagination")
#
#         layout = QHBoxLayout(pagination)
#         layout.setContentsMargins(10, 5, 10, 5)
#         layout.setSpacing(5)
#
#         # Кнопки пагинации
#         pages = ["<", "1", "2", "3", "...", "5", ">"]
#
#         for page in pages:
#             btn = QPushButton(page)
#             btn.setFont(QFont("Segoe UI", 11))
#             btn.setFixedSize(35, 35)
#
#             if page == "1":
#                 btn.setObjectName("currentPage")
#             elif page in ["<", ">"]:
#                 btn.setObjectName("navButton")
#             else:
#                 btn.setObjectName("pageButton")
#
#             layout.addWidget(btn)
#
#         return pagination
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
#     def open_procurement(self, number):
#         """Открыть закупку"""
#         print(f"Открытие закупки №{number}")
#
#     def export_procurement(self, number):
#         """Экспорт закупки"""
#         print(f"Экспорт закупки №{number}")
#
#     def delete_procurement(self, number):
#         """Удалить закупку"""
#         print(f"Удаление закупки №{number}")
#
#     def go_back(self):
#         """Вернуться на главную страницу"""
#         parent = self.parent()
#         while parent is not None:
#             if hasattr(parent, 'switch_page'):
#                 parent.switch_page("Главная")
#                 return
#             parent = parent.parent()
#
#     def apply_styles(self):
#         """Применение стилей"""
#         self.setStyleSheet(get_history_styles())
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
# #     window.setWindowTitle("Тест: История закупок")
# #     window.setGeometry(100, 100, 1400, 900)
# #
# #     icons_path = Path(__file__).parent / "icons"
# #     page = HistoryRequestPage(icons_path)
# #     window.setCentralWidget(page)
# #
# #     window.show()
# #     sys.exit(app.exec())