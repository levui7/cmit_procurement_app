import sys
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QSizePolicy, QApplication,
                             QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView,
                             QLineEdit, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from ui.styles import get_catalog_styles


class ProductCatalogPage(QWidget):
    def __init__(self, icons_path, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path
        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        """Создание контента страницы (БЕЗ сайдбара и exit card)"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)

        # Заголовок страницы
        title = QLabel("Справочник товаров")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")

        subtitle = QLabel("Управляйте внутренним каталогом товаров для закупки")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #6B7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)

        # Панель инструментов: поиск + кнопки
        toolbar = QHBoxLayout()
        toolbar.setSpacing(15)

        # Поле поиска с иконкой
        search_container = QFrame()
        search_container.setObjectName("searchContainer")
        search_container.setFixedHeight(45)

        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(15, 0, 15, 0)
        search_layout.setSpacing(10)

        search_icon = self.create_icon_label("magnifying-glass.png", size=20)
        search_layout.addWidget(search_icon)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Поиск по названию товара...")
        search_input.setFont(QFont("Segoe UI", 12))
        search_input.setObjectName("searchInput")
        search_input.setStyleSheet("border: none; padding: 0; background-color: transparent;")
        search_layout.addWidget(search_input)

        toolbar.addWidget(search_container, stretch=1)

        # Кнопка "Добавить товар"
        add_btn = QPushButton("+ Добавить товар")
        add_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        add_btn.setFixedHeight(45)
        add_btn.setFixedWidth(180)
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.add_product)
        toolbar.addWidget(add_btn)

        # Кнопка "Импорт из Excel"
        import_btn = QPushButton()
        import_btn.setFixedHeight(45)
        import_btn.setFixedWidth(180)
        import_btn.setObjectName("importButton")
        import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        import_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        import_layout = QHBoxLayout(import_btn)
        import_layout.setContentsMargins(15, 10, 15, 10)
        import_layout.setSpacing(10)

        import_icon = self.create_icon_label("stats.png", size=20)
        import_text = QLabel("Импорт из Excel")
        import_text.setFont(QFont("Segoe UI", 12))
        import_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        import_layout.addWidget(import_icon)
        import_layout.addWidget(import_text)
        import_layout.addStretch()

        import_btn.clicked.connect(self.import_excel)
        toolbar.addWidget(import_btn)

        # Кнопка "Экспорт в Excel"
        export_btn = QPushButton("Экспорт в Excel")
        export_btn.setFont(QFont("Segoe UI", 12))
        export_btn.setFixedHeight(45)
        export_btn.setFixedWidth(180)
        export_btn.setObjectName("exportButton")
        export_btn.clicked.connect(self.export_excel)
        toolbar.addWidget(export_btn)

        layout.addLayout(toolbar)

        # Таблица товаров
        table = self.create_products_table()
        layout.addWidget(table)

        # Нижняя панель: пагинация
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        pagination_info = QLabel("1–10 из 120 товаров")
        pagination_info.setFont(QFont("Segoe UI", 11))
        pagination_info.setStyleSheet("color: #6B7280;")
        bottom_layout.addWidget(pagination_info)

        bottom_layout.addStretch()

        pagination = self.create_pagination()
        bottom_layout.addWidget(pagination)

        layout.addLayout(bottom_layout)

    def create_products_table(self):
        """Создание таблицы товаров"""
        table = QTableWidget()
        table.setObjectName("productsTable")
        table.setRowCount(10)
        table.setColumnCount(5)

        headers = ["Название", "Категория", "% поломки", "Ключевые слова", "Действия"]
        table.setHorizontalHeaderLabels(headers)

        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        products_data = [
            ("Бумага офисная A4, 80 г/м²", "Канцелярские товары", "2.5%", "бумага, офисная, A4, 80 г/м2"),
            ("Картридж HP LaserJet 12A", "Расходные материалы", "4.2%", "картридж, HP, 12A, принтер"),
            ("Ручка шариковая синяя", "Канцелярские товары", "1.1%", "ручка, шариковая, синяя"),
            ("Кабель витая пара UTP Cat.5e", "Кабельная продукция", "3.3%", "кабель, витая пара, UTP, Cat.5e"),
            ("Светильник LED 36W", "Электрика", "2.8%", "светильник, LED, 36W, офисный"),
            ("Степлер №24/6", "Канцелярские товары", "1.7%", "степлер, №24/6, канцелярский"),
            ("Папка-регистратор A4, 75 мм", "Канцелярские товары", "2.0%", "папка, регистратор, A4, 75 мм"),
            ("Мышь компьютерная USB", "Компьютерная периферия", "3.9%", "мышь, USB, компьютерная"),
            ("Клавиатура проводная USB", "Компьютерная периферия", "3.6%", "клавиатура, USB, проводная"),
            ("Батарейка AA (LR6)", "Электрика", "0.9%", "батарейка, AA, LR6, щелочная"),
        ]

        for row, (name, category, damage, keywords) in enumerate(products_data):
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("Segoe UI", 11))
            table.setItem(row, 0, name_item)

            category_item = QTableWidgetItem(category)
            category_item.setFont(QFont("Segoe UI", 11))
            table.setItem(row, 1, category_item)

            damage_item = QTableWidgetItem(damage)
            damage_item.setFont(QFont("Segoe UI", 11))
            damage_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 2, damage_item)

            keywords_item = QTableWidgetItem(keywords)
            keywords_item.setFont(QFont("Segoe UI", 11))
            table.setItem(row, 3, keywords_item)

            edit_btn = QPushButton("✏️ Изменить")
            edit_btn.setFont(QFont("Segoe UI", 10))
            edit_btn.setFixedSize(120, 32)
            edit_btn.setObjectName("editButton")
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_product(r))
            table.setCellWidget(row, 4, edit_btn)

        for row in range(table.rowCount()):
            table.setRowHeight(row, 50)

        table.horizontalHeader().setFixedHeight(45)
        return table

    def create_pagination(self):
        """Создание блока пагинации"""
        pagination = QFrame()
        pagination.setObjectName("pagination")

        layout = QHBoxLayout(pagination)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        pages = ["<", "1", "2", "3", "...", "12", ">"]

        for page in pages:
            btn = QPushButton(page)
            btn.setFont(QFont("Segoe UI", 11))
            btn.setFixedSize(35, 35)

            if page == "1":
                btn.setObjectName("currentPage")
            elif page in ["<", ">"]:
                btn.setObjectName("navButton")
            else:
                btn.setObjectName("pageButton")

            layout.addWidget(btn)

        return pagination

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

    def add_product(self):
        print("Добавление нового товара")

    def import_excel(self):
        print("Импорт из Excel")

    def export_excel(self):
        print("Экспорт в Excel")

    def edit_product(self, row):
        print(f"Редактирование товара в строке {row}")

    def apply_styles(self):
        """Применение стилей"""
        self.setStyleSheet(get_catalog_styles())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    # Для тестирования создаем временное окно
    from PyQt6.QtWidgets import QMainWindow

    window = QMainWindow()
    window.setWindowTitle("Тест: Справочник товаров")
    window.setGeometry(100, 100, 1400, 900)

    icons_path = Path(__file__).parent / "icons"
    page = ProductCatalogPage(icons_path)
    window.setCentralWidget(page)

    window.show()
    sys.exit(app.exec())