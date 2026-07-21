"""
Диалог подтверждения заявки перед парсингом
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.utils.config import Colors, Fonts, Spacing, Sizes
from ui.utils.icons import create_icon_label, IconNames
from ui.utils.styles import get_dialog_styles


class ConfirmRequestDialog(QDialog):
    """Диалог подтверждения заявки перед запуском парсинга"""

    def __init__(self, request_data, items_data, parent=None):
        """
        Args:
            request_data: dict с общими параметрами заявки
            items_data: список товаров в заявке
        """
        super().__init__(parent)
        self.request_data = request_data
        self.items_data = items_data

        self.setWindowTitle("Подтверждение заявки")
        self.setFixedSize(800, 600)
        self.setModal(True)

        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
        layout.setSpacing(Spacing.LG)

        # Заголовок
        header = QHBoxLayout()
        header.setSpacing(Spacing.SM)

        icon = create_icon_label(IconNames.DOCUMENT, size=32)
        header.addWidget(icon)

        title = QLabel("Подтверждение заявки")
        title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_HEADING, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        header.addWidget(title)
        header.addStretch()

        layout.addLayout(header)

        # Блок с фильтрами
        filters_card = QFrame()
        filters_card.setObjectName("formCard")
        filters_layout = QVBoxLayout(filters_card)
        filters_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        filters_layout.setSpacing(Spacing.SM)

        filters_title = QLabel("Параметры закупки")
        filters_title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        filters_layout.addWidget(filters_title)

        filters_grid = QHBoxLayout()
        filters_grid.setSpacing(Spacing.XL)

        # Дата доставки
        date_layout = QVBoxLayout()
        date_label = QLabel("📅 Дата доставки")
        date_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL, QFont.Weight.Bold))
        date_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        date_layout.addWidget(date_label)

        date_value = QLabel(self.request_data.get('delivery_date', 'Не указана'))
        date_value.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        date_value.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        date_layout.addWidget(date_value)

        filters_grid.addLayout(date_layout)

        # Рейтинг
        rating_layout = QVBoxLayout()
        rating_label = QLabel("⭐ Мин. рейтинг")
        rating_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL, QFont.Weight.Bold))
        rating_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        rating_layout.addWidget(rating_label)

        rating_value = QLabel(self.request_data.get('min_rating', 'Любой'))
        rating_value.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        rating_value.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        rating_layout.addWidget(rating_value)

        filters_grid.addLayout(rating_layout)

        # Студенты
        students_layout = QVBoxLayout()
        students_label = QLabel("👥 Студентов")
        students_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL, QFont.Weight.Bold))
        students_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        students_layout.addWidget(students_label)

        students_value = QLabel(str(self.request_data.get('students_count', 0)))
        students_value.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        students_value.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        students_layout.addWidget(students_value)

        filters_grid.addLayout(students_layout)
        filters_grid.addStretch()

        filters_layout.addLayout(filters_grid)
        layout.addWidget(filters_card)

        # Таблица товаров
        items_title = QLabel(f"Товары в заявке ({len(self.items_data)} шт.)")
        items_title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        items_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(items_title)

        self.items_table = QTableWidget()
        self.items_table.setColumnCount(4)
        self.items_table.setHorizontalHeaderLabels([
            "№", "Наименование", "Количество", "Диапазон цен, ₽"
        ])
        self.items_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.items_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.verticalHeader().setVisible(False)
        self.items_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.items_table.setFixedHeight(250)

        # Заполняем таблицу
        for i, item in enumerate(self.items_data, 1):
            row = self.items_table.rowCount()
            self.items_table.insertRow(row)

            num_item = QTableWidgetItem(str(i))
            num_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_table.setItem(row, 0, num_item)

            name_item = QTableWidgetItem(item['product']['name'])
            name_item.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
            self.items_table.setItem(row, 1, name_item)

            qty_item = QTableWidgetItem(str(item['quantity']))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_table.setItem(row, 2, qty_item)

            price_range = f"{item['min_price']:.0f} – {item['max_price']:.0f}" if item['max_price'] > 0 else "Любая"
            price_item = QTableWidgetItem(price_range)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_table.setItem(row, 3, price_item)

        layout.addWidget(self.items_table)

        # Предупреждение
        warning_layout = QHBoxLayout()
        warning_layout.setSpacing(Spacing.SM)

        warning_icon = create_icon_label(IconNames.WARNING, size=20)
        warning_layout.addWidget(warning_icon)

        warning_text = QLabel("После подтверждения начнётся поиск товаров на маркетплейсах. Это может занять несколько минут.")
        warning_text.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        warning_text.setStyleSheet(f"color: {Colors.WARNING};")
        warning_text.setWordWrap(True)
        warning_layout.addWidget(warning_text)
        warning_layout.addStretch()

        layout.addLayout(warning_layout)
        layout.addStretch()

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(Spacing.SM)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        cancel_btn.setFixedSize(150, Sizes.BUTTON_HEIGHT)
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.clicked.connect(self.reject)

        confirm_btn = QPushButton("✅ Подтвердить и начать поиск")
        confirm_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        confirm_btn.setFixedSize(280, Sizes.BUTTON_HEIGHT)
        confirm_btn.setObjectName("saveButton")
        confirm_btn.clicked.connect(self.accept)

        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(confirm_btn)

        layout.addLayout(buttons_layout)

    def apply_styles(self):
        self.setStyleSheet(get_dialog_styles())