"""
Страница результатов поиска товаров на маркетплейсах
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QRadioButton,
                             QButtonGroup, QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.utils.config import Colors, Fonts, Spacing, Sizes
from ui.utils.icons import create_icon_label, IconNames
from ui.utils.styles import get_catalog_styles


class SearchResultsPage(QWidget):
    """Страница отображения результатов поиска товаров"""

    def __init__(self, request_id, parent=None):
        super().__init__(parent)
        self.request_id = request_id
        self.selected_items = {}  # {internal_product_id: marketplace_product_id}

        self.create_widgets()
        self.apply_styles()
        self.load_results()

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
        layout.setSpacing(Spacing.LG)

        # Заголовок
        title = QLabel("Результаты поиска товаров")
        title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_DISPLAY, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)

        subtitle = QLabel(f"Заявка #{self.request_id} • Найдено вариантов на маркетплейсах")
        subtitle.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(subtitle)

        # Скроллируемая область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(Spacing.LG)

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        # Итоговая панель
        summary_card = QFrame()
        summary_card.setObjectName("formCard")
        summary_layout = QHBoxLayout(summary_card)
        summary_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)

        # Сумма
        total_layout = QVBoxLayout()
        total_label = QLabel("Итоговая сумма:")
        total_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL, QFont.Weight.Bold))
        total_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        total_layout.addWidget(total_label)

        self.total_amount_label = QLabel("0 ₽")
        self.total_amount_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_HEADING, QFont.Weight.Bold))
        self.total_amount_label.setStyleSheet(f"color: {Colors.PRIMARY};")
        total_layout.addWidget(self.total_amount_label)

        summary_layout.addLayout(total_layout)
        summary_layout.addStretch()

        # Кнопки
        save_btn = QPushButton("💾 Сохранить заявку")
        save_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        save_btn.setFixedSize(220, Sizes.BUTTON_HEIGHT)
        save_btn.setObjectName("saveButton")
        save_btn.clicked.connect(self.save_results)
        summary_layout.addWidget(save_btn)

        back_btn = QPushButton("← Назад")
        back_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        back_btn.setFixedSize(120, Sizes.BUTTON_HEIGHT)
        back_btn.setObjectName("clearButton")
        back_btn.clicked.connect(self.go_back)
        summary_layout.addWidget(back_btn)

        layout.addWidget(summary_card)

    def load_results(self):
        """Загрузка результатов поиска (заглушка)"""
        # TODO: Загрузить реальные данные из БД
        mock_data = [
            {
                'internal_product_id': 1,
                'product_name': 'Светодиоды 5мм красные',
                'variants': [
                    {'marketplace': 'Ozon', 'name': 'Светодиоды красные 5мм (20шт)', 'price': 150.0, 'rating': 4.5, 'url': 'https://ozon.ru/...'},
                    {'marketplace': 'Wildberries', 'name': 'LED красные 5мм набор', 'price': 120.0, 'rating': 4.2, 'url': 'https://wb.ru/...'},
                ]
            },
        ]

        for product_data in mock_data:
            card = self.create_product_card(product_data)
            self.scroll_layout.addWidget(card)

        self.scroll_layout.addStretch()

    def create_product_card(self, product_data):
        """Создание карточки товара с вариантами"""
        card = QFrame()
        card.setObjectName("formCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        card_layout.setSpacing(Spacing.SM)

        # Заголовок товара
        product_title = QLabel(product_data['product_name'])
        product_title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        product_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        card_layout.addWidget(product_title)

        # Таблица вариантов
        variants_table = QTableWidget()
        variants_table.setColumnCount(5)
        variants_table.setHorizontalHeaderLabels(["Выбрать", "Маркетплейс", "Название", "Цена, ₽", "Рейтинг"])
        variants_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        variants_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        variants_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        variants_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        variants_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        variants_table.verticalHeader().setVisible(False)
        variants_table.setFixedHeight(150)

        for i, variant in enumerate(product_data['variants']):
            row = variants_table.rowCount()
            variants_table.insertRow(row)

            # Радиокнопка выбора
            radio = QRadioButton()
            radio_widget = QWidget()
            radio_layout = QHBoxLayout(radio_widget)
            radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            radio_layout.setContentsMargins(0, 0, 0, 0)
            radio_layout.addWidget(radio)
            variants_table.setCellWidget(row, 0, radio_widget)

            # Маркетплейс
            marketplace_item = QTableWidgetItem(variant['marketplace'])
            variants_table.setItem(row, 1, marketplace_item)

            # Название
            name_item = QTableWidgetItem(variant['name'])
            variants_table.setItem(row, 2, name_item)

            # Цена
            price_item = QTableWidgetItem(f"{variant['price']:.0f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            variants_table.setItem(row, 3, price_item)

            # Рейтинг
            rating_item = QTableWidgetItem(f"⭐ {variant['rating']}")
            rating_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            variants_table.setItem(row, 4, rating_item)

        card_layout.addWidget(variants_table)
        return card

    def save_results(self):
        """Сохранить выбранные варианты"""
        QMessageBox.information(self, "Успех", "Заявка сохранена!")
        # TODO: Сохранить выбранные варианты в БД

    def go_back(self):
        """Вернуться на главную"""
        parent = self.parent()
        while parent is not None:
            if hasattr(parent, 'switch_page'):
                parent.switch_page("Главная")
                return
            parent = parent.parent()

    def apply_styles(self):
        self.setStyleSheet(get_catalog_styles())