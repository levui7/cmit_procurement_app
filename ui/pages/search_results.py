"""
Страница результатов поиска на маркетплейсах
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QScrollArea, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from backend.database import get_marketplace_matches, get_all_internal_products


class SearchResultsPage(QWidget):
    def __init__(self, icons_path, request_id, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path
        self.request_id = request_id
        self.create_widgets()
        self.load_results()

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)

        # Заголовок
        title = QLabel("Результаты поиска на маркетплейсах")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        layout.addWidget(title)

        subtitle = QLabel("Выберите лучшие варианты для закупки")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #6B7280;")
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        # Таблица результатов
        self.table = QTableWidget()
        self.table.setObjectName("resultsTable")
        self.table.setColumnCount(7)

        headers = ["Товар", "Маркетплейс", "Название", "Цена", "Рейтинг", "Выбрать", ""]
        self.table.setHorizontalHeaderLabels(headers)

        # Настройка колонок
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.table)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        # Кнопка "Экспорт в Excel" с иконкой
        self.export_btn = QPushButton()
        self.export_btn.setFixedHeight(45)
        self.export_btn.setFixedWidth(220)
        self.export_btn.setObjectName("exportButton")
        self.export_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Layout для кнопки с иконкой
        export_layout = QHBoxLayout(self.export_btn)
        export_layout.setContentsMargins(15, 10, 15, 10)
        export_layout.setSpacing(10)

        # Иконка экспорта
        export_icon = self.create_icon_label("stats.png", size=20)
        export_text = QLabel("Экспорт в Excel")
        export_text.setFont(QFont("Segoe UI", 12))
        export_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        export_layout.addWidget(export_icon)
        export_layout.addWidget(export_text)
        export_layout.addStretch()

        self.export_btn.clicked.connect(self.export_to_excel)

        # Кнопка "Сохранить заявку" с иконкой
        self.save_btn = QPushButton()
        self.save_btn.setFixedHeight(45)
        self.save_btn.setFixedWidth(220)
        self.save_btn.setObjectName("saveButton")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Layout для кнопки с иконкой
        save_layout = QHBoxLayout(self.save_btn)
        save_layout.setContentsMargins(15, 10, 15, 10)
        save_layout.setSpacing(10)

        # Иконка сохранения
        save_icon = self.create_icon_label("save.png", size=20)
        save_text = QLabel("Сохранить заявку")
        save_text.setFont(QFont("Segoe UI", 12))
        save_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        save_layout.addWidget(save_icon)
        save_layout.addWidget(save_text)
        save_layout.addStretch()

        self.save_btn.clicked.connect(self.save_selection)

        buttons_layout.addWidget(self.export_btn)
        buttons_layout.addWidget(self.save_btn)

        layout.addLayout(buttons_layout)

    def load_results(self):
        """Загрузка результатов парсинга"""
        # Получаем все товары из заявки
        internal_products = get_all_internal_products()

        self.table.setRowCount(0)

        for product in internal_products:
            # Получаем найденные варианты для этого товара
            matches = get_marketplace_matches(product.id)

            for i, match in enumerate(matches):
                row = self.table.rowCount()
                self.table.insertRow(row)

                # Внутренний товар
                self.table.setItem(row, 0, QTableWidgetItem(product.name))

                # Маркетплейс
                marketplace_item = QTableWidgetItem(match.marketplace_name)
                marketplace_item.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
                self.table.setItem(row, 1, marketplace_item)

                # Название на маркетплейсе
                self.table.setItem(row, 2, QTableWidgetItem(match.name))

                # Цена
                price_item = QTableWidgetItem(f"{match.price:,.0f} ₽")
                price_item.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
                self.table.setItem(row, 3, price_item)

                # Рейтинг
                rating_item = QTableWidgetItem(f"⭐ {match.rating}" if match.rating else "N/A")
                self.table.setItem(row, 4, rating_item)

                # Кнопка "Выбрать"
                select_btn = QPushButton("✅")
                select_btn.setFixedSize(40, 30)
                select_btn.clicked.connect(lambda checked, p=product.id, m=match.id:
                                           self.select_product(p, m))
                self.table.setCellWidget(row, 5, select_btn)

    def select_product(self, internal_id, marketplace_id):
        """Выбор товара для закупки"""
        # Здесь логика выбора лучшего варианта
        QMessageBox.information(self, "Выбрано", f"Товар {marketplace_id} выбран!")
        # TODO: Сохранить выбор в БД

    def export_to_excel(self):
        """Экспорт результатов в Excel"""
        # TODO: Реализовать экспорт
        QMessageBox.information(self, "Экспорт", "Экспорт в Excel будет реализован")

    def save_selection(self):
        """Сохранение выбранной конфигурации"""
        # TODO: Сохранить финальную заявку
        QMessageBox.information(self, "Сохранено", "Заявка сохранена!")