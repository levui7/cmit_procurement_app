"""
Страница справочника товаров
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QApplication,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QLineEdit, QAbstractItemView, QDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from ui.utils.styles import get_catalog_styles

from ui.dialogs import EditProductDialog

from backend.database import (
    get_all_internal_products,
    search_internal_products,
    add_internal_product,
    update_internal_product,
    delete_internal_product
)


class ProductCatalogPage(QWidget):
    def __init__(self, icons_path, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path

        # ✅ Храним текущие товары и параметры пагинации
        self.current_products = []
        self.current_page = 1
        self.items_per_page = 10

        self.create_widgets()
        self.apply_styles()

        # ✅ Загружаем товары после создания виджетов
        self.load_products()

    def create_widgets(self):
        """Создание контента страницы"""
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

        self.search_input = QLineEdit()  # ✅ Сохраняем ссылку для поиска
        self.search_input.setPlaceholderText("Поиск по названию товара...")
        self.search_input.setFont(QFont("Segoe UI", 12))
        self.search_input.setObjectName("searchInput")
        self.search_input.setStyleSheet("border: none; padding: 0; background-color: transparent;")
        self.search_input.textChanged.connect(self.on_search_changed)  # ✅ Подключаем поиск
        search_layout.addWidget(self.search_input)

        toolbar.addWidget(search_container, stretch=1)

        # Кнопка "Добавить товар"
        add_btn = QPushButton("+ Добавить товар")
        add_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        add_btn.setFixedHeight(45)
        add_btn.setFixedWidth(180)
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.add_internal_product)
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

        # ✅ Таблица товаров (создаём один раз, сохраняем ссылку)
        self.table = self.create_products_table()
        layout.addWidget(self.table)

        # Нижняя панель: пагинация
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setSpacing(20)

        self.pagination_info = QLabel("0 товаров")
        self.pagination_info.setFont(QFont("Segoe UI", 11))
        self.pagination_info.setStyleSheet("color: #6B7280;")
        self.bottom_layout.addWidget(self.pagination_info)

        self.bottom_layout.addStretch()

        self.pagination = self.create_pagination()
        self.bottom_layout.addWidget(self.pagination)

        layout.addLayout(self.bottom_layout)

    def create_products_table(self):
        """Создание таблицы товаров"""
        table = QTableWidget()
        table.setObjectName("productsTable")
        table.setColumnCount(4)  # Ровно 4 колонки

        # ✅ Новые заголовки
        headers = ["ID", "Наименование товара", "Ключевые слова", "Изменить"]
        table.setHorizontalHeaderLabels(headers)

        # ✅ Настройка ширины для 4 колонок (индексы 0, 1, 2, 3)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Наименование
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Ключевые слова
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Изменить

        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        table.horizontalHeader().setFixedHeight(45)
        return table

    def load_products(self):
        """Загрузка товаров из БД"""
        # ✅ Получаем товары из БД
        self.current_products = get_all_internal_products()
        self.refresh_table()

    def refresh_table(self):
        """Обновление таблицы с учётом пагинации"""
        total_items = len(self.current_products)
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_products = self.current_products[start_idx:end_idx]

        self.table.setRowCount(0)

        for product in page_products:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Колонка 0: ID (внутренний код или ID из БД)
            id_text = product.internal_code if product.internal_code else str(product.id)
            id_item = QTableWidgetItem(id_text)
            id_item.setFont(QFont("Segoe UI", 10))
            id_item.setForeground(Qt.GlobalColor.darkGray)
            self.table.setItem(row, 0, id_item)

            # Колонка 1: Наименование товара
            name_item = QTableWidgetItem(product.name)
            name_item.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
            self.table.setItem(row, 1, name_item)

            # Колонка 2: Ключевые слова
            keywords_item = QTableWidgetItem(product.keywords or "")
            keywords_item.setFont(QFont("Segoe UI", 10))
            self.table.setItem(row, 2, keywords_item)

            # Колонка 3: Кнопка "Изменить"
            # ⚠️ ВАЖНО: индекс 3, а не 4!
            edit_btn = QPushButton("Изменить")
            edit_btn.setFont(QFont("Segoe UI", 10))
            edit_btn.setFixedSize(100, 32)
            edit_btn.setObjectName("editButton")

            # Передаем в лямбду словарь данных, а не ORM-объект, чтобы избежать краша
            product_data = {
                'id': product.id,
                'internal_code': product.internal_code,
                'name': product.name,
                'category': product.category,
                'keywords': product.keywords
            }
            edit_btn.clicked.connect(lambda checked, data=product_data: self.edit_product(data))

            self.table.setCellWidget(row, 3, edit_btn)  # ✅ ИСПРАВЛЕНО: было 4, стало 3

            self.table.setRowHeight(row, 50)

        self.update_pagination_info(total_items)

    def update_pagination_info(self, total_items):
        """Обновление текста пагинации"""
        if total_items == 0:
            self.pagination_info.setText("0 товаров")
        else:
            start = (self.current_page - 1) * self.items_per_page + 1
            end = min(self.current_page * self.items_per_page, total_items)
            self.pagination_info.setText(f"{start}–{end} из {total_items} товаров")

    def on_search_changed(self, text):
        """Обработчик изменения текста поиска"""
        if text.strip():
            # ✅ Поиск через БД
            self.current_products = search_internal_products(text.strip())
            self.current_page = 1  # Сбрасываем на первую страницу
        else:
            # ✅ Загружаем все товары
            self.current_products = get_all_internal_products()

        self.refresh_table()

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

            # ✅ Подключаем обработчики пагинации
            if page == "<":
                btn.clicked.connect(self.go_to_previous_page)
            elif page == ">":
                btn.clicked.connect(self.go_to_next_page)
            elif page.isdigit():
                btn.clicked.connect(lambda checked, p=int(page): self.go_to_page(p))

            layout.addWidget(btn)

        return pagination

    def go_to_page(self, page_number):
        """Переход на конкретную страницу"""
        self.current_page = page_number
        self.refresh_table()

    def go_to_previous_page(self):
        """Переход на предыдущую страницу"""
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_table()

    def go_to_next_page(self):
        """Переход на следующую страницу"""
        total_pages = (len(self.current_products) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_table()

    def add_internal_product(self):
        # """Добавить товар через диалог"""
        # # ✅ Диалог ввода данных
        # name, ok = QInputDialog.getText(self, "Добавить товар", "Название товара:")
        # if not ok or not name.strip():
        #     return
        #
        # category, ok = QInputDialog.getText(self, "Добавить товар", "Категория:")
        # if not ok or not category.strip():
        #     return
        #
        # damage, ok = QInputDialog.getDouble(self, "Добавить товар", "% поломки:", 0.0, 0.0, 100.0, 1)
        # if not ok:
        #     return
        #
        # keywords, ok = QInputDialog.getText(self, "Добавить товар", "Ключевые слова (через запятую):")
        # if not ok:
        #     keywords = ""
        #
        # # ✅ Добавляем в БД
        # product_id = add_internal_product(
        #     name=name.strip(),
        #     category=category.strip(),
        #     damage_percent=damage,
        #     keywords=keywords.strip()
        # )
        #
        # if product_id:
        #     QMessageBox.information(self, "Успех", f"Товар '{name}' добавлен!")
        #     self.load_products()  # ✅ Перезагружаем таблицу
        # else:
        #     QMessageBox.critical(self, "Ошибка", "Не удалось добавить товар")

        """Добавить товар через модальное окно"""
        # Создаем пустой объект товара для передачи в диалог
        # Или можно передать None и обработать это в диалоге
        empty_product_data = {
            'internal_code': '',
            'name': '',
            'category': '',
            'keywords': ''
        }

        # Открываем диалог (переименуем заголовок)
        dialog = EditProductDialog(empty_product_data, parent=None)
        dialog.setWindowTitle("Добавить новый товар")  # Меняем заголовок

        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Получаем данные из диалога
            data = dialog.get_product_data()

            # Проверяем обязательные поля
            if not data['name']:
                QMessageBox.warning(self, "Ошибка", "Название товара обязательно!")
                return

            if not data['category']:
                QMessageBox.warning(self, "Ошибка", "Категория обязательна!")
                return

            # Получаем глобальный процент поломки из настроек
            from backend.database import get_app_setting
            damage_percent = float(get_app_setting("default_damage_percent", "2.5"))

            # Добавляем в БД
            product_id = add_internal_product(
                internal_code=data['internal_code'],
                name=data['name'],
                category=data['category'],
                damage_percent=damage_percent,  # Берем из настроек
                keywords=data['keywords']
            )

            if product_id:
                QMessageBox.information(self, "Успех", f"Товар '{data['name']}' добавлен!")
                self.load_products()  # Перезагружаем таблицу
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось добавить товар")

    def edit_product(self, product_data):
        """Редактировать товар через модальное окно"""
        # product_data теперь словарь, а не объект БД

        # Открываем диалог с parent=None (это предотвращает краш в Windows)
        dialog = EditProductDialog(product_data, parent=None)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Получаем обновленные данные из диалога
            updated_data = dialog.get_product_data()
            product_id = updated_data.pop('id')  # Извлекаем ID, его не обновляем

            # Обновляем в БД
            success = update_internal_product(product_id, **updated_data)

            if success:
                QMessageBox.information(self, "Успех", f"Товар '{updated_data['name']}' обновлён!")
                self.load_products()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось обновить товар")

    def delete_internal_product(self, product_id):
        """Удалить товар"""
        product = next((p for p in self.current_products if p.id == product_id), None)
        if not product:
            return

        # Подтверждение удаления
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить товар '{product.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if delete_internal_product(product_id):
                QMessageBox.information(self, "Успех", "Товар удалён!")
                self.load_products()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось удалить товар")

    def import_excel(self):
        """Импорт из Excel"""
        QMessageBox.information(self, "Импорт", "Функция импорта из Excel будет реализована позже")

    def export_excel(self):
        """Экспорт в Excel"""
        QMessageBox.information(self, "Экспорт", "Функция экспорта в Excel будет реализована позже")

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
            print(f"⚠️ Иконка не найдена: {icon_path}")

        label.setFixedSize(size, size)
        return label

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

    icons_path = Path(__file__).parent.parent / "icons"
    page = ProductCatalogPage(icons_path)
    window.setCentralWidget(page)

    window.show()
    sys.exit(app.exec())