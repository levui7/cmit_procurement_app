"""
Диалог редактирования/добавления товара
"""
from pathlib import Path
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtGui import QFont, QPixmap, QIcon

from ui.utils.styles import get_dialog_styles
from ui.utils.icons import create_icon_label, IconNames  # ✅ ДОБАВЛЕНО
from ui.utils.icons import create_icon_label, IconNames, get_icon_path

class EditProductDialog(QDialog):
    """Модальное окно для редактирования/добавления товара"""

    def __init__(self, product_data, parent=None):
        super().__init__(parent)

        # ✅ УСТАНОВКА ИКОНКИ ОКНА
        icon_path = get_icon_path(IconNames.LOGO)  # Получаем путь к логотипу
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))  # Устанавливаем иконку окна

        # Приводим всё к словарю для единообразия
        if isinstance(product_data, dict):
            self.product_data = product_data
        else:
            self.product_data = {
                'id': getattr(product_data, 'id', None),
                'internal_code': getattr(product_data, 'internal_code', ''),
                'name': getattr(product_data, 'name', ''),
                'keywords': getattr(product_data, 'keywords', '')
            }

        self.setWindowTitle("Редактировать товар" if self.product_data.get('id') else "Добавить новый товар")
        self.setFixedSize(500, 450)
        self.setModal(True)
        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)


        # ✅ 2. ЗАГОЛОВОК ПО ЦЕНТРУ (без иконки)
        title = QLabel("Редактирование товара" if self.product_data.get('id') else "Добавление товара")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Подзаголовок (опционально)
        subtitle = QLabel("Заполните информацию о товаре")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #6B7280;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(10)  # Отступ перед формой

        # Форма с полями
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # === ВНУТРЕННИЙ КОД ===
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Например: INT-001")

        # ✅ ИСПРАВЛЕНО: Мы просто берем код, который уже передан из product_catalog.py
        existing_code = self.product_data.get('internal_code', '')
        self.code_input.setText(existing_code)

        # Если это новый товар (нет ID), делаем поле только для чтения
        if not self.product_data.get('id'):
            self.code_input.setReadOnly(True)
            self.code_input.setStyleSheet("background-color: #F3F4F6; color: #6B7280;")

        form_layout.addRow("Внутренний код:", self.code_input)

        # === НАЗВАНИЕ ===
        self.name_input = QLineEdit()
        self.name_input.setText(self.product_data.get('name', ""))
        self.name_input.setPlaceholderText("Название товара")
        form_layout.addRow("Название:", self.name_input)

        # === КЛЮЧЕВЫЕ СЛОВА ===
        self.keywords_input = QLineEdit()
        self.keywords_input.setText(self.product_data.get('keywords') or "")
        self.keywords_input.setPlaceholderText("Ключевые слова через запятую")
        form_layout.addRow("Ключевые слова:", self.keywords_input)

        layout.addLayout(form_layout)
        layout.addStretch()

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.setFixedHeight(40)
        self.clear_btn.setObjectName("secondaryButton")
        self.clear_btn.clicked.connect(self.clear_form)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setFixedHeight(40)
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setFixedHeight(40)
        self.save_btn.setObjectName("saveButton")
        self.save_btn.clicked.connect(self.save_changes)

        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)

        layout.addLayout(buttons_layout)

    def apply_styles(self):
        self.setStyleSheet(get_dialog_styles())

    def clear_form(self):
        self.code_input.clear()
        self.name_input.clear()
        self.keywords_input.clear()
        self.name_input.setFocus()

    def save_changes(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Название товара обязательно!")
            return

        self.accept()

    def get_product_data(self):
        """Возвращаем обновленные данные, сохраняя ID"""
        return {
            'id': self.product_data.get('id'),
            'internal_code': self.code_input.text().strip(),
            'name': self.name_input.text().strip(),
            'keywords': self.keywords_input.text().strip(),
        }