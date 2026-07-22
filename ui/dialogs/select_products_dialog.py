"""
Диалог выбора товаров из справочника для добавления в заявку
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QLineEdit,
                             QFrame, QMessageBox)
from PyQt6.QtGui import QFont

from backend.crud.crud_internal_product import get_all_internal_products
from backend.database import get_session
from ui.utils.icons import create_icon_label, IconNames

class SelectProductsDialog(QDialog):
    """Модальное окно для выбора товаров из справочника"""

    def __init__(self, icons_path=None, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path
        self.selected_products = []  # Список выбранных товаров (словари)
        self.all_products = []       # Кэш всех товаров

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
        search_layout.setSpacing(10)

        search_icon = create_icon_label(IconNames.MAGNIFYING_GLASS, size=20)
        search_layout.addWidget(search_icon)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию или коду...")
        self.search_input.setFont(QFont("Segoe UI", 11))
        self.search_input.setStyleSheet("border: none; background: transparent;")
        self.search_input.textChanged.connect(self.filter_products)
        search_layout.addWidget(self.search_input)

        layout.addWidget(search_container)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Код", "Название"])

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
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
        db = get_session()
        try:
            self.all_products = get_all_internal_products(db)
            self.refresh_table(self.all_products)
        finally:
            db.close()

    def refresh_table(self, products):
        """Обновить таблицу"""
        self.table.setRowCount(0)
        for product in products:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Колонка 0: Код
            code_item = QTableWidgetItem(product.internal_code or str(product.id))
            code_item.setFont(QFont("Segoe UI", 10))
            self.table.setItem(row, 0, code_item)

            # Колонка 1: Название
            name_item = QTableWidgetItem(product.name)
            name_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row, 1, name_item)

            # ✅ Колонка с категорией полностью удалена

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
        # ✅ ИСПРАВЛЕНО: теперь 2 колонки на товар, а не 3
        count = len(self.table.selectedItems()) // 2
        self.info_label.setText(f"Выбрано товаров: {count}")

    def confirm_selection(self):
        """Подтвердить выбор"""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите хотя бы один товар!")
            return

        self.selected_products = []
        for row in sorted(selected_rows):
            code_text = self.table.item(row, 0).text()
            name_text = self.table.item(row, 1).text()

            # Находим товар в кэше и сохраняем как словарь
            for p in self.all_products:
                if p.internal_code == code_text or p.name == name_text:
                    self.selected_products.append({
                        'id': p.id,
                        'internal_code': p.internal_code,
                        'name': p.name,
                        # ✅ УДАЛЕНО: 'category': p.category,
                        'keywords': p.keywords
                    })
                    break

        self.accept()

    def apply_styles(self):
        from ui.utils.styles import get_dialog_styles
        self.setStyleSheet(get_dialog_styles())