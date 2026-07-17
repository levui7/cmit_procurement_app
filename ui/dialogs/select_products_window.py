"""
Диалог выбора товаров из справочника для добавления в заявку
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QLineEdit,
                             QFrame)
from PyQt6.QtGui import QFont

from backend.database import get_all_internal_products


class SelectProductsDialog(QDialog):
    """Модальное окно для выбора товаров из справочника"""

    def __init__(self, icons_path, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path
        self.selected_products = []  # Список выбранных товаров

        self.setWindowTitle("Выбрать товары из справочника")
        self.setFixedSize(700, 500)
        self.setModal(True)

        self.create_widgets()
        self.load_products()
        self.apply_styles()

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        title = QLabel("Выберите товары для добавления в заявку")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")
        layout.addWidget(title)

        # Поиск
        search_container = QFrame()
        search_container.setObjectName("searchContainer")
        search_container.setFixedHeight(40)

        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(10, 0, 10, 0)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Поиск по названию...")
        self.search_input.setFont(QFont("Segoe UI", 11))
        self.search_input.setStyleSheet("border: none; background: transparent;")
        self.search_input.textChanged.connect(self.filter_products)
        search_layout.addWidget(self.search_input)

        layout.addWidget(search_container)

        # Таблица товаров
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Код", "Название", "Категория"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        # Информация о выборе
        self.info_label = QLabel("Выбрано товаров: 0")
        self.info_label.setFont(QFont("Segoe UI", 11))
        self.info_label.setStyleSheet("color: #6B7280;")
        layout.addWidget(self.info_label)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setFixedHeight(40)
        self.cancel_btn.setFixedWidth(120)
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        self.add_btn = QPushButton("Добавить выбранные")
        self.add_btn.setFixedHeight(40)
        self.add_btn.setFixedWidth(200)
        self.add_btn.setObjectName("saveButton")
        self.add_btn.clicked.connect(self.confirm_selection)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.add_btn)

        layout.addLayout(buttons_layout)

        # Подключаем сигнал изменения выделения
        self.table.itemSelectionChanged.connect(self.update_selection_info)

    def load_products(self):
        """Загрузить все товары из справочника"""
        self.all_products = get_all_internal_products()
        self.refresh_table(self.all_products)

    def refresh_table(self, products):
        """Обновить таблицу"""
        self.table.setRowCount(0)
        for product in products:
            row = self.table.rowCount()
            self.table.insertRow(row)

            code_item = QTableWidgetItem(product.internal_code or str(product.id))
            code_item.setFont(QFont("Segoe UI", 10))
            self.table.setItem(row, 0, code_item)

            name_item = QTableWidgetItem(product.name)
            name_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row, 1, name_item)

            cat_item = QTableWidgetItem(product.category)
            cat_item.setFont(QFont("Segoe UI", 10))
            self.table.setItem(row, 2, cat_item)

    def filter_products(self, text):
        """Фильтрация товаров по поиску"""
        if text.strip():
            filtered = [p for p in self.all_products
                        if text.lower() in p.name.lower()
                        or (p.internal_code and text.lower() in p.internal_code.lower())]
        else:
            filtered = self.all_products
        self.refresh_table(filtered)

    def update_selection_info(self):
        """Обновить счётчик выбранных товаров"""
        count = len(self.table.selectedItems()) // 3  # 3 колонки на товар
        self.info_label.setText(f"Выбрано товаров: {count}")

    def confirm_selection(self):
        """Подтвердить выбор"""
        # Собираем уникальные выбранные товары (по строкам)
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Внимание", "Выберите хотя бы один товар!")
            return

        self.selected_products = []
        for row in sorted(selected_rows):
            product_id = int(self.table.item(row, 0).text()) if self.table.item(row, 0).text().isdigit() else None
            # Находим товар по коду или ID
            for p in self.all_products:
                if (p.internal_code == self.table.item(row, 0).text()) or (p.id == product_id):
                    self.selected_products.append(p)
                    break

        self.accept()

    def apply_styles(self):
        from ui.utils.styles import get_dialog_styles
        self.setStyleSheet(get_dialog_styles())