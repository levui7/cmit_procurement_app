"""
Страница создания заявки
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QSpinBox,
                             QDoubleSpinBox, QDateEdit, QComboBox,
                             QMessageBox, QDialog, QTextEdit)
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QFont

from datetime import datetime
from backend.database import get_session
from ui.dialogs.parsing_progress_dialog import ParsingProgressDialog

from ui.utils.config import Colors, Fonts, Spacing, Sizes
from ui.utils.icons import create_icon_label, IconNames
from ui.utils.styles import get_create_request_styles
from ui.dialogs.select_products_dialog import SelectProductsDialog
from backend.crud.crud_procurement import create_procurement_with_items, get_request_by_id


class CreateRequestPage(QWidget):
    def __init__(self, icons_path=None, parent=None):
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
        layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
        layout.setSpacing(Spacing.LG)

        # === ЗАГОЛОВОК ===
        title = QLabel("Создание заявки")
        title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_DISPLAY, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)

        subtitle = QLabel("Добавьте товары из справочника и укажите параметры закупки")
        subtitle.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(subtitle)
        layout.addSpacing(Spacing.SM)

        # === БЛОК 1: ОБЩИЕ ФИЛЬТРЫ ===
        common_group = QFrame()
        common_group.setObjectName("formCard")
        common_layout = QVBoxLayout(common_group)
        common_layout.setContentsMargins(Spacing.XL, Spacing.LG, Spacing.XL, Spacing.LG)
        common_layout.setSpacing(Spacing.LG)

        section_title = QLabel("Общие параметры (применяются ко всем товарам)")
        section_title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        section_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        common_layout.addWidget(section_title)

        filters_row = QHBoxLayout()
        filters_row.setSpacing(Spacing.LG)

        # Дата доставки
        date_layout = QVBoxLayout()
        date_header = QHBoxLayout()
        date_header.setSpacing(Spacing.SM)

        date_icon = create_icon_label(IconNames.CALENDAR, size=Sizes.ICON_SMALL)
        date_header.addWidget(date_icon)

        date_label = QLabel("Желаемая дата доставки")
        date_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL, QFont.Weight.Bold))
        date_header.addWidget(date_label)
        date_header.addStretch()

        date_layout.addLayout(date_header)

        self.delivery_date = QDateEdit()
        self.delivery_date.setDate(QDate.currentDate().addMonths(3))
        self.delivery_date.setDisplayFormat("dd.MM.yyyy")
        self.delivery_date.setCalendarPopup(True)
        self.delivery_date.setFixedHeight(Sizes.INPUT_HEIGHT)
        self.delivery_date.setObjectName("inputField")
        date_layout.addWidget(self.delivery_date)
        filters_row.addLayout(date_layout)

        # Минимальный рейтинг
        rating_layout = QVBoxLayout()
        rating_header = QHBoxLayout()
        rating_header.setSpacing(Spacing.SM)

        rating_icon = create_icon_label(IconNames.STAR, size=Sizes.ICON_SMALL)
        rating_header.addWidget(rating_icon)

        rating_label = QLabel("Минимальный рейтинг")
        rating_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL, QFont.Weight.Bold))
        rating_header.addWidget(rating_label)
        rating_header.addStretch()

        rating_layout.addLayout(rating_header)

        self.min_rating = QComboBox()
        self.min_rating.addItems(["4.5 и выше", "4.0 и выше", "3.5 и выше", "3.0 и выше", "Любой"])
        self.min_rating.setCurrentIndex(1)
        self.min_rating.setFixedHeight(Sizes.INPUT_HEIGHT)
        self.min_rating.setFixedWidth(150)
        self.min_rating.setObjectName("inputField")
        rating_layout.addWidget(self.min_rating)
        filters_row.addLayout(rating_layout)

        # Количество студентов
        students_layout = QVBoxLayout()
        students_header = QHBoxLayout()
        students_header.setSpacing(Spacing.SM)

        students_icon = create_icon_label(IconNames.GROUP, size=Sizes.ICON_SMALL)
        students_header.addWidget(students_icon)

        students_label = QLabel("Количество студентов")
        students_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL, QFont.Weight.Bold))
        students_header.addWidget(students_label)
        students_header.addStretch()

        students_layout.addLayout(students_header)

        self.students_count = QSpinBox()
        self.students_count.setRange(1, 10000)
        self.students_count.setValue(100)
        self.students_count.setFixedHeight(Sizes.INPUT_HEIGHT)
        self.students_count.setFixedWidth(120)
        self.students_count.setObjectName("inputField")
        students_layout.addWidget(self.students_count)
        filters_row.addLayout(students_layout)

        filters_row.addStretch()
        common_layout.addLayout(filters_row)

        # Описание заявки
        desc_header = QHBoxLayout()
        desc_header.setSpacing(Spacing.SM)

        desc_icon = create_icon_label(IconNames.DOCUMENT, size=Sizes.ICON_SMALL)
        desc_header.addWidget(desc_icon)

        desc_label = QLabel("Описание заявки (необязательно)")
        desc_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL, QFont.Weight.Bold))
        desc_header.addWidget(desc_label)
        desc_header.addStretch()

        common_layout.addLayout(desc_header)

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
        items_layout.setContentsMargins(Spacing.XL, Spacing.LG, Spacing.XL, Spacing.LG)
        items_layout.setSpacing(Spacing.SM)

        items_header = QHBoxLayout()
        items_title = QLabel("Товары в заявке")
        items_title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        items_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        items_header.addWidget(items_title)
        items_header.addStretch()

        # Кнопка "Добавить из справочника"
        add_from_catalog_btn = QPushButton("+ Добавить из справочника")
        add_from_catalog_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL, QFont.Weight.Bold))
        add_from_catalog_btn.setFixedHeight(Sizes.BUTTON_HEIGHT_SMALL)
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
        remove_btn = QPushButton("Удалить выбранные")
        remove_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        remove_btn.setFixedHeight(Sizes.BUTTON_HEIGHT_SMALL)
        remove_btn.setFixedWidth(180)
        remove_btn.setObjectName("dangerButton")
        remove_btn.clicked.connect(self.remove_selected_items)
        items_layout.addWidget(remove_btn, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(items_group)

        # === БЛОК 3: КНОПКИ ДЕЙСТВИЙ ===
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(Spacing.SM)

        clear_btn = QPushButton("Очистить всё")
        clear_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        clear_btn.setFixedSize(180, Sizes.BUTTON_HEIGHT)
        clear_btn.setObjectName("clearButton")
        clear_btn.clicked.connect(self.clear_all)

        actions_layout.addStretch()
        actions_layout.addWidget(clear_btn)

        create_btn = QPushButton(" Создать заявку и найти товары")
        create_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        create_btn.setFixedSize(280, Sizes.BUTTON_HEIGHT)
        create_btn.setObjectName("nextButton")
        create_btn.clicked.connect(self.create_and_search)
        actions_layout.addWidget(create_btn)

        layout.addLayout(actions_layout)
        layout.addStretch()

    def open_select_products_dialog(self):
        """Открыть диалог выбора товаров из справочника"""
        dialog = SelectProductsDialog(self.icons_path, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # ✅ Теперь работаем со словарями, а не ORM-объектами
            for product_data in dialog.selected_products:
                # Проверяем, нет ли уже этого товара
                if any(item['product']['id'] == product_data['id'] for item in self.request_items):
                    continue
                self.request_items.append({
                    'product': product_data,  # ← теперь это словарь
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

            # ✅ Название из словаря
            product_data = item['product']
            name_item = QTableWidgetItem(product_data['name'])
            name_item.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
            self.items_table.setItem(row, 1, name_item)

            # Количество
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

            self.items_table.setRowHeight(row, Sizes.TABLE_ROW_HEIGHT - 10)

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
                'product': item['product'],
                'quantity': item['quantity'],
                'min_price': item['min_price'],
                'max_price': item['max_price']
            }
            for item in self.request_items
        ]

        # 1. Показываем диалог подтверждения
        from ui.dialogs.confirm_request_dialog import ConfirmRequestDialog
        confirm_dialog = ConfirmRequestDialog(request_data, items_data, parent=self)

        if confirm_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        # 2. Создаём заявку в БД
        from backend.crud.crud_procurement import create_procurement_with_items
        items_for_db = [
            {
                'internal_product_id': item['product']['id'],
                'quantity': item['quantity'],
                'min_price': item['min_price'],
                'max_price': item['max_price']
            }
            for item in items_data
        ]

        request_id, request_number = create_procurement_with_items(request_data, items_for_db)

        print(f" request_id={request_id}, type={type(request_id)}")
        print(f"🔍 request_number={request_number}, type={type(request_number)}")

        if not request_id:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать заявку!")
            return

        # ✅ Если это ORM-объекты, извлеките ID
        if hasattr(request_id, 'id'):
            request_id = request_id.id
        if hasattr(request_number, 'number'):
            request_number = request_number.number

        # ✅ Получаем дату создания заявки из БД
        db = get_session()
        try:
            req = get_request_by_id(db, request_id)
            request_date = req.created_at.strftime("%d.%m.%Y") if req and req.created_at else datetime.now().strftime(
                "%d.%m.%Y")
        finally:
            db.close()

        # 3. Запускаем парсинг (ПРАВКА: добавлен request_id первым аргументом)
        parsing_dialog = ParsingProgressDialog(request_id, request_number, len(items_data), request_date, parent=self)

        result = parsing_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # ✅ Сохраняем ID активной заявки (без локального импорта get_session!)
            from backend.crud.crud_settings import set_app_setting

            db = get_session()  # ← Из глобального импорта
            try:
                set_app_setting(db, "active_request_id", str(request_id))
            finally:
                db.close()

            # ✅ Безопасный переход с задержкой
            QTimer.singleShot(100, lambda: self._switch_to_results(request_id))

    def _switch_to_results(self, request_id):
        """Безопасный переход на страницу результатов"""
        parent = self.parent()
        while parent is not None:
            if hasattr(parent, 'switch_page'):
                parent.current_request_id = request_id
                parent.switch_page("Активная заявка")
                return
            parent = parent.parent()

    def apply_styles(self):
        self.setStyleSheet(get_create_request_styles())