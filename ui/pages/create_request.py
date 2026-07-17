# import sys
# from pathlib import Path
# from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#                              QPushButton, QFrame, QSpinBox, QLineEdit,
#                              QDateEdit, QComboBox, QSizePolicy, QApplication)
# from PyQt6.QtCore import Qt, QDate
# from PyQt6.QtGui import QFont, QPixmap, QIcon
#
# from PyQt6.QtGui import QRegularExpressionValidator
# from PyQt6.QtCore import QRegularExpression
#
# from ui.styles import get_create_request_styles
#
# class CreateRequestPage(QWidget):
#     def __init__(self, icons_path, parent=None):
#         super().__init__(parent)
#         self.icons_path = icons_path
#         self.create_widgets()
#         self.apply_styles()
#
#     def create_widgets(self):
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(50, 40, 50, 40)
#         layout.setSpacing(30)
#
#         title = QLabel("Создание заявки")
#         title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
#         title.setStyleSheet("color: #1F2937;")
#
#         subtitle = QLabel("Укажите параметры закупки для подбора оптимальных предложений")
#         subtitle.setFont(QFont("Segoe UI", 13))
#         subtitle.setStyleSheet("color: #6B7280;")
#
#         layout.addWidget(title)
#         layout.addWidget(subtitle)
#         layout.addSpacing(10)
#
#         form_card = QFrame()
#         form_card.setObjectName("formCard")
#         form_layout = QVBoxLayout(form_card)
#         form_layout.setContentsMargins(40, 40, 40, 40)
#         form_layout.setSpacing(30)
#
#         # ✅ Поле 1: Количество студентов (ОДИН вызов!)
#         self.students_spinbox = self.create_students_input()
#         students_row = self.create_form_row(
#             "group.png",
#             "Количество студентов",
#             self.students_spinbox,  # ← Используем сохранённое поле
#             tooltip_text="Общее количество студентов, которые будут использовать оборудование в течение года"
#         )
#         form_layout.addLayout(students_row)
#         form_layout.addWidget(self.create_separator())
#
#         # ✅ Поле 2: Ограничения по цене (используем create_price_layout)
#         self.min_price_edit, self.max_price_edit = self.create_price_input()
#         price_layout = self.create_price_layout(self.min_price_edit, self.max_price_edit)
#         price_row = self.create_form_row(
#             "ruble.png",
#             "Ограничения по цене",
#             price_layout,  # ← Передаём layout, а не кортеж!
#             tooltip_text="Минимальная и максимальная стоимость за единицу товара в рублях"
#         )
#         form_layout.addLayout(price_row)
#         form_layout.addWidget(self.create_separator())
#
#         # ✅ Поле 3: Желаемая дата доставки (ОДИН вызов!)
#         self.date_edit = self.create_date_input()
#         date_row = self.create_form_row(
#             "calendar.png",
#             "Желаемая дата доставки",
#             self.date_edit,  # ← Используем сохранённое поле
#             tooltip_text="Дата, к которой необходимо получить все товары"
#         )
#         form_layout.addLayout(date_row)
#         form_layout.addWidget(self.create_separator())
#
#         # ✅ Поле 4: Рейтинг товара
#         self.rating_combo = self.create_rating_input()
#         rating_row = self.create_form_row(
#             "star.png",
#             "Рейтинг товара",
#             self.rating_combo,  # ← Используем сохранённое поле
#             tooltip_text="Минимальный рейтинг товара на маркетплейсе"
#         )
#         form_layout.addLayout(rating_row)
#
#         # Кнопки
#         buttons_layout = QHBoxLayout()
#         buttons_layout.setSpacing(15)
#
#         clear_btn = QPushButton("Очистить")
#         clear_btn.setFont(QFont("Segoe UI", 12))
#         clear_btn.setFixedSize(150, 45)
#         clear_btn.setObjectName("clearButton")
#         clear_btn.clicked.connect(self.clear_form)
#
#         next_btn = QPushButton("Далее")
#         next_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         next_btn.setFixedSize(150, 45)
#         next_btn.setObjectName("nextButton")
#         next_btn.clicked.connect(self.on_next)
#
#         buttons_layout.addStretch()
#         buttons_layout.addWidget(clear_btn)
#         buttons_layout.addWidget(next_btn)
#
#         layout.addWidget(form_card)
#         layout.addStretch()
#         layout.addLayout(buttons_layout)
#
#     def create_form_row(self, icon_file, label_text, input_widget, tooltip_text=""):
#         """Создание строки формы с иконкой, заголовком и полем ввода"""
#         row_layout = QHBoxLayout()
#         row_layout.setSpacing(20)
#         row_layout.setContentsMargins(0, 10, 0, 10)
#
#         # Иконка слева
#         icon_container = QFrame()
#         icon_container.setFixedSize(60, 60)
#         icon_container.setObjectName("iconContainer")
#
#         icon_layout = QVBoxLayout(icon_container)
#         icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#
#         icon_label = self.create_icon_label(icon_file, size=30)
#         icon_layout.addWidget(icon_label)
#
#         row_layout.addWidget(icon_container)
#
#         # Правая часть (заголовок + поле ввода)
#         right_layout = QVBoxLayout()
#         right_layout.setSpacing(10)
#
#         # Заголовок с иконкой информации
#         title_layout = QHBoxLayout()
#         title_layout.setSpacing(5)
#
#         title_label = QLabel(label_text)
#         title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
#         title_label.setStyleSheet("color: #1F2937;")
#         title_layout.addWidget(title_label)
#
#         # # Иконка информации (i)
#         # info_icon = QLabel("ⓘ")
#         # info_icon.setFont(QFont("Segoe UI", 12))
#         # info_icon.setStyleSheet("color: #9CA3AF;")
#         # title_layout.addWidget(info_icon)
#         # title_layout.addStretch()
#
#         # Иконка информации (i)
#         info_icon = QLabel("ⓘ")
#         info_icon.setFont(QFont("Segoe UI", 12))
#         info_icon.setStyleSheet("color: #9CA3AF;")
#         info_icon.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
#
#         # ✅ ДОБАВИТЬ ПОДСКАЗКУ
#         if tooltip_text:
#             info_icon.setToolTip(tooltip_text)
#             info_icon.setCursor(Qt.CursorShape.WhatsThisCursor)  # Меняем курсор на "помощь"
#
#         title_layout.addWidget(info_icon)
#         title_layout.addStretch()
#
#         right_layout.addLayout(title_layout)
#         # right_layout.addWidget(input_widget)
#         if isinstance(input_widget, QHBoxLayout) or isinstance(input_widget, QVBoxLayout):
#             right_layout.addLayout(input_widget)
#         else:
#             right_layout.addWidget(input_widget)
#
#         row_layout.addLayout(right_layout)
#
#         return row_layout
#
#     def create_students_input(self):
#         """Поле ввода количества студентов"""
#         spinbox = QSpinBox()
#         spinbox.setMinimum(1)
#         spinbox.setMaximum(10000)
#         spinbox.setValue(100)
#         spinbox.setFont(QFont("Segoe UI", 12))
#         spinbox.setFixedHeight(45)
#         spinbox.setObjectName("inputField")
#         return spinbox
#
#     # def create_price_input(self):
#     #     """Поля ввода мин/макс цены"""
#     #     price_layout = QHBoxLayout()
#     #     price_layout.setSpacing(15)
#     #
#     #     # Валидатор: только цифры и пробелы
#     #     validator = QRegularExpressionValidator(
#     #         QRegularExpression(r'^[0-9\s]*$')  # Разрешаем только цифры и пробелы
#     #     )
#     #
#     #     # Минимум
#     #     min_edit = QLineEdit()
#     #     min_edit.setPlaceholderText("Минимум, ₽")
#     #     min_edit.setText("500")
#     #     min_edit.setFont(QFont("Segoe UI", 12))
#     #     min_edit.setFixedHeight(45)
#     #     min_edit.setObjectName("inputField")
#     #     min_edit.setValidator(validator)
#     #
#     #     # Разделитель "-"
#     #     separator = QLabel("—")
#     #     separator.setFont(QFont("Segoe UI", 14))
#     #     separator.setStyleSheet("color: #6B7280;")
#     #
#     #     # Максимум
#     #     max_edit = QLineEdit()
#     #     max_edit.setPlaceholderText("Максимум, ₽")
#     #     max_edit.setText("2 500")
#     #     max_edit.setFont(QFont("Segoe UI", 12))
#     #     max_edit.setFixedHeight(45)
#     #     max_edit.setObjectName("inputField")
#     #     max_edit.setValidator(validator)
#     #
#     #     price_layout.addWidget(min_edit)
#     #     price_layout.addWidget(separator)
#     #     price_layout.addWidget(max_edit)
#     #
#     #     return price_layout
#
#     def create_price_input(self):
#         """Создание полей мин/макс цены (возвращает сами поля)"""
#         # Создаём валидатор: только цифры и пробелы
#         from PyQt6.QtGui import QRegularExpressionValidator
#         from PyQt6.QtCore import QRegularExpression
#
#         validator = QRegularExpressionValidator(
#             QRegularExpression(r'^[0-9\s]*$')
#         )
#
#         # Минимум
#         min_edit = QLineEdit()
#         min_edit.setPlaceholderText("Минимум, ₽")
#         min_edit.setText("500")
#         min_edit.setFont(QFont("Segoe UI", 12))
#         min_edit.setFixedHeight(45)
#         min_edit.setObjectName("inputField")
#         min_edit.setValidator(validator)
#
#         # Максимум
#         max_edit = QLineEdit()
#         max_edit.setPlaceholderText("Максимум, ₽")
#         max_edit.setText("2 500")
#         max_edit.setFont(QFont("Segoe UI", 12))
#         max_edit.setFixedHeight(45)
#         max_edit.setObjectName("inputField")
#         max_edit.setValidator(validator)
#
#         return min_edit, max_edit
#
#     def create_price_layout(self, min_edit, max_edit):
#         """Создание layout для полей цены"""
#         price_layout = QHBoxLayout()
#         price_layout.setSpacing(15)
#
#         # Разделитель "-"
#         separator = QLabel("—")
#         separator.setFont(QFont("Segoe UI", 14))
#         separator.setStyleSheet("color: #6B7280;")
#
#         price_layout.addWidget(min_edit)
#         price_layout.addWidget(separator)
#         price_layout.addWidget(max_edit)
#
#         return price_layout
#
#     def create_date_input(self):
#         """Поле выбора даты"""
#         date_edit = QDateEdit()
#         date_edit.setDate(QDate(2024, 6, 15))
#         date_edit.setDisplayFormat("dd.MM.yyyy")
#         date_edit.setFont(QFont("Segoe UI", 12))
#         date_edit.setFixedHeight(45)
#         date_edit.setFixedWidth(300)
#         date_edit.setCalendarPopup(True)  # Показывать календарь при клике
#         date_edit.setObjectName("inputField")
#         return date_edit
#
#     def create_rating_input(self):
#         """Поле выбора рейтинга"""
#         rating_layout = QHBoxLayout()
#         rating_layout.setSpacing(15)
#
#         # Выпадающий список
#         combo = QComboBox()
#         combo.addItems(["4 и выше", "3 и выше", "2 и выше", "1 и выше"])
#         combo.setCurrentIndex(0)
#         combo.setFont(QFont("Segoe UI", 12))
#         combo.setFixedHeight(45)
#         combo.setFixedWidth(200)
#         combo.setObjectName("inputField")
#
#         rating_layout.addWidget(combo)
#         rating_layout.addStretch()
#
#         # return rating_layout
#         return combo
#
#     def create_separator(self):
#         """Создание разделительной линии"""
#         separator = QFrame()
#         separator.setFrameShape(QFrame.Shape.HLine)
#         separator.setStyleSheet("background-color: #E5E7EB; border: none;")
#         separator.setFixedHeight(1)
#         return separator
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
#     def clear_form(self):
#         """Очистка формы"""
#         # Сброс количества студентов
#         self.students_spinbox.setValue(100)
#
#         # Сброс цен
#         self.min_price_edit.setText("500")
#         self.max_price_edit.setText("2 500")
#
#         # Сброс даты
#         self.date_edit.setDate(QDate(2024, 6, 15))
#
#         # Сброс рейтинга
#         self.rating_combo.setCurrentIndex(0)  # "4 и выше"
#
#     def on_next(self):
#         """Обработчик кнопки 'Далее'"""
#         print("Переход к следующему шагу")
#         # Здесь будет логика перехода к результатам
#
#     def apply_styles(self):
#         self.setStyleSheet(get_create_request_styles())
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
# #     window.setWindowTitle("Тест: Создание заявки")
# #     window.setGeometry(100, 100, 1400, 900)
# #
# #     icons_path = Path(__file__).parent / "icons"
# #     page = CreateRequestPage(icons_path)
# #     window.setCentralWidget(page)
# #
# #     window.show()
# #     sys.exit(app.exec())

"""
Страница создания заявки
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QSpinBox,
                             QDoubleSpinBox, QDateEdit, QComboBox,
                             QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

from ui.utils.styles import get_create_request_styles
from ui.dialogs import SelectProductsDialog
from backend.database import create_procurement_with_items


class CreateRequestPage(QWidget):
    def __init__(self, icons_path, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path

        # Хранилище товаров в заявке: список словарей
        # [{'product': InternalProduct, 'quantity': int, 'min_price': float, 'max_price': float}]
        self.request_items = []

        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        """Создание интерфейса страницы"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(25)

        # === ЗАГОЛОВОК ===
        title = QLabel("Создание заявки")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")
        layout.addWidget(title)

        subtitle = QLabel("Добавьте товары из справочника и укажите параметры закупки")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #6B7280;")
        layout.addWidget(subtitle)
        layout.addSpacing(10)

        # === БЛОК 1: ОБЩИЕ ФИЛЬТРЫ ===
        common_group = QFrame()
        common_group.setObjectName("formCard")
        common_layout = QVBoxLayout(common_group)
        common_layout.setContentsMargins(30, 25, 30, 25)
        common_layout.setSpacing(20)

        section_title = QLabel("Общие параметры (применяются ко всем товарам)")
        section_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        section_title.setStyleSheet("color: #1F2937;")
        common_layout.addWidget(section_title)

        filters_row = QHBoxLayout()
        filters_row.setSpacing(20)

        # Дата доставки
        date_layout = QVBoxLayout()
        date_label = QLabel("📅 Желаемая дата доставки")
        date_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        date_layout.addWidget(date_label)

        self.delivery_date = QDateEdit()
        self.delivery_date.setDate(QDate.currentDate().addMonths(3))
        self.delivery_date.setDisplayFormat("dd.MM.yyyy")
        self.delivery_date.setCalendarPopup(True)
        self.delivery_date.setFixedHeight(40)
        self.delivery_date.setObjectName("inputField")
        date_layout.addWidget(self.delivery_date)
        filters_row.addLayout(date_layout)

        # Минимальный рейтинг
        rating_layout = QVBoxLayout()
        rating_label = QLabel("⭐ Минимальный рейтинг")
        rating_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        rating_layout.addWidget(rating_label)

        self.min_rating = QComboBox()
        self.min_rating.addItems(["4.5 и выше", "4.0 и выше", "3.5 и выше", "3.0 и выше", "Любой"])
        self.min_rating.setCurrentIndex(1)
        self.min_rating.setFixedHeight(40)
        self.min_rating.setFixedWidth(150)
        self.min_rating.setObjectName("inputField")
        rating_layout.addWidget(self.min_rating)
        filters_row.addLayout(rating_layout)

        # Количество студентов
        students_layout = QVBoxLayout()
        students_label = QLabel("👥 Количество студентов")
        students_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        students_layout.addWidget(students_label)

        self.students_count = QSpinBox()
        self.students_count.setRange(1, 10000)
        self.students_count.setValue(100)
        self.students_count.setFixedHeight(40)
        self.students_count.setFixedWidth(120)
        self.students_count.setObjectName("inputField")
        students_layout.addWidget(self.students_count)
        filters_row.addLayout(students_layout)

        filters_row.addStretch()
        common_layout.addLayout(filters_row)

        # Описание заявки
        desc_label = QLabel("📝 Описание заявки (необязательно)")
        desc_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        common_layout.addWidget(desc_label)

        from PyQt6.QtWidgets import QTextEdit
        self.description = QTextEdit()
        self.description.setPlaceholderText("Например: Закупка для лаборатории робототехники на 2025 год")
        self.description.setFixedHeight(60)
        self.description.setObjectName("inputField")
        common_layout.addWidget(self.description)

        layout.addWidget(common_group)

        # === БЛОК 2: СПИСОК ТОВАРОВ В ЗАЯВКЕ ===
        items_group = QFrame()
        items_group.setObjectName("formCard")
        items_layout = QVBoxLayout(items_group)
        items_layout.setContentsMargins(30, 25, 30, 25)
        items_layout.setSpacing(15)

        items_header = QHBoxLayout()
        items_title = QLabel("Товары в заявке")
        items_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        items_title.setStyleSheet("color: #1F2937;")
        items_header.addWidget(items_title)
        items_header.addStretch()

        # Кнопка "Добавить из справочника"
        add_from_catalog_btn = QPushButton("+ Добавить из справочника")
        add_from_catalog_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        add_from_catalog_btn.setFixedHeight(35)
        add_from_catalog_btn.setFixedWidth(220)
        add_from_catalog_btn.setObjectName("addButton")
        add_from_catalog_btn.clicked.connect(self.open_select_products_dialog)
        items_header.addWidget(add_from_catalog_btn)

        items_layout.addLayout(items_header)

        # Таблица товаров
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels([
            "№", "Наименование товара", "Количество", "Мин. цена, ₽", "Макс. цена, ₽"
        ])
        self.items_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.items_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.verticalHeader().setVisible(False)
        self.items_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.items_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.items_table.setFixedHeight(300)
        items_layout.addWidget(self.items_table)

        # Кнопка удаления выбранного товара
        remove_btn = QPushButton(" Удалить выбранные")
        remove_btn.setFont(QFont("Segoe UI", 11))
        remove_btn.setFixedHeight(35)
        remove_btn.setFixedWidth(180)
        remove_btn.setObjectName("dangerButton")
        remove_btn.clicked.connect(self.remove_selected_items)
        items_layout.addWidget(remove_btn, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(items_group)

        # === БЛОК 3: КНОПКИ ДЕЙСТВИЙ ===
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)

        clear_btn = QPushButton(" Очистить всё")
        clear_btn.setFont(QFont("Segoe UI", 12))
        clear_btn.setFixedSize(180, 45)
        clear_btn.setObjectName("clearButton")
        clear_btn.clicked.connect(self.clear_all)

        actions_layout.addStretch()
        actions_layout.addWidget(clear_btn)

        create_btn = QPushButton("🚀 Создать заявку и найти товары")
        create_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        create_btn.setFixedSize(280, 45)
        create_btn.setObjectName("nextButton")
        create_btn.clicked.connect(self.create_and_search)
        actions_layout.addWidget(create_btn)

        layout.addLayout(actions_layout)
        layout.addStretch()

    def open_select_products_dialog(self):
        """Открыть диалог выбора товаров из справочника"""
        dialog = SelectProductsDialog(self.icons_path, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Добавляем выбранные товары в заявку
            for product in dialog.selected_products:
                # Проверяем, нет ли уже этого товара
                if any(item['product'].id == product.id for item in self.request_items):
                    continue
                self.request_items.append({
                    'product': product,
                    'quantity': 10,
                    'min_price': 0.0,
                    'max_price': 0.0
                })
            self.refresh_items_table()

    def refresh_items_table(self):
        """Обновить таблицу товаров в заявке"""
        self.items_table.setRowCount(0)

        for i, item in enumerate(self.request_items, 1):
            row = self.items_table.rowCount()
            self.items_table.insertRow(row)

            # Номер
            num_item = QTableWidgetItem(str(i))
            num_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_table.setItem(row, 0, num_item)

            # Название
            name_item = QTableWidgetItem(item['product'].name)
            name_item.setFont(QFont("Segoe UI", 11))
            self.items_table.setItem(row, 1, name_item)

            # Количество (редактируемое)
            qty_widget = QSpinBox()
            qty_widget.setRange(1, 100000)
            qty_widget.setValue(item['quantity'])
            qty_widget.setFixedHeight(30)
            qty_widget.setObjectName("inputField")
            qty_widget.valueChanged.connect(lambda val, idx=row: self.update_item_quantity(idx, val))
            self.items_table.setCellWidget(row, 2, qty_widget)

            # Мин. цена
            min_widget = QDoubleSpinBox()
            min_widget.setRange(0, 1000000)
            min_widget.setValue(item['min_price'])
            min_widget.setPrefix("")
            min_widget.setSuffix(" ₽")
            min_widget.setFixedHeight(30)
            min_widget.setObjectName("inputField")
            min_widget.valueChanged.connect(lambda val, idx=row: self.update_item_min_price(idx, val))
            self.items_table.setCellWidget(row, 3, min_widget)

            # Макс. цена
            max_widget = QDoubleSpinBox()
            max_widget.setRange(0, 1000000)
            max_widget.setValue(item['max_price'])
            max_widget.setSuffix(" ₽")
            max_widget.setFixedHeight(30)
            max_widget.setObjectName("inputField")
            max_widget.valueChanged.connect(lambda val, idx=row: self.update_item_max_price(idx, val))
            self.items_table.setCellWidget(row, 4, max_widget)

            self.items_table.setRowHeight(row, 40)

    def update_item_quantity(self, row, value):
        if 0 <= row < len(self.request_items):
            self.request_items[row]['quantity'] = value

    def update_item_min_price(self, row, value):
        if 0 <= row < len(self.request_items):
            self.request_items[row]['min_price'] = value

    def update_item_max_price(self, row, value):
        if 0 <= row < len(self.request_items):
            self.request_items[row]['max_price'] = value

    def remove_selected_items(self):
        """Удалить выбранные товары из заявки"""
        selected_rows = set()
        for item in self.items_table.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите товары для удаления!")
            return

        # Удаляем в обратном порядке, чтобы индексы не сбились
        for row in sorted(selected_rows, reverse=True):
            if 0 <= row < len(self.request_items):
                self.request_items.pop(row)

        self.refresh_items_table()

    def clear_all(self):
        """Очистить всю форму"""
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите очистить все данные заявки?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.request_items.clear()
            self.refresh_items_table()
            self.description.clear()

    def create_and_search(self):
        """Создать заявку и запустить поиск"""
        # Валидация
        if not self.request_items:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один товар в заявку!")
            return

        # Собираем данные
        request_data = {
            'description': self.description.toPlainText(),
            'delivery_date': self.delivery_date.date().toString("dd.MM.yyyy"),
            'min_rating': self.min_rating.currentText(),
            'students_count': self.students_count.value()
        }

        items_data = [
            {
                'internal_product_id': item['product'].id,
                'quantity': item['quantity'],
                'min_price': item['min_price'],
                'max_price': item['max_price']
            }
            for item in self.request_items
        ]

        # Создаём заявку в БД
        request_id, request_number = create_procurement_with_items(request_data, items_data)

        if request_id:
            QMessageBox.information(
                self, "Успех",
                f"Заявка №{request_number} создана!\n\n"
                f"Товаров: {len(self.request_items)}\n"
                f"Дата доставки: {request_data['delivery_date']}\n\n"
                f"Сейчас начнётся поиск товаров на маркетплейсах..."
            )

            # TODO: Здесь запуск парсинга и переход на страницу результатов
            # self.start_parsing(request_id)
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать заявку!")

    def apply_styles(self):
        self.setStyleSheet(get_create_request_styles())