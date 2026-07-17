# """
# Диалог редактирования товара
# """
# from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
#                              QLineEdit, QPushButton, QFormLayout, QMessageBox)
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont
#
# from ui.styles import get_dialog_styles
#
#
# class EditProductDialog(QDialog):
#     """Модальное окно для редактирования/добавления товара"""
#
#     def __init__(self, product_data, parent=None):
#         super().__init__(parent)
#         # product_data может быть словарем (при добавлении) или объектом (при редактировании)
#         # Приводим всё к словарю для единообразия
#         if isinstance(product_data, dict):
#             self.product_data = product_data
#         else:
#             self.product_data = {
#                 'id': getattr(product_data, 'id', None),
#                 'internal_code': getattr(product_data, 'internal_code', ''),
#                 'name': getattr(product_data, 'name', ''),
#                 'category': getattr(product_data, 'category', ''),
#                 'keywords': getattr(product_data, 'keywords', '')
#             }
#
#         self.setWindowTitle("Редактировать товар")
#         self.setFixedSize(500, 400)
#         self.setModal(True)
#         self.create_widgets()
#         self.apply_styles()
#
#     def create_widgets(self):
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 20, 30, 20)
#         layout.setSpacing(20)
#
#         # Заголовок
#         title = QLabel("Редактирование товара")
#         title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
#         title.setStyleSheet("color: #1F2937;")
#         layout.addWidget(title)
#
#         # Форма с полями
#         form_layout = QFormLayout()
#         form_layout.setSpacing(15)
#
#         # # Внутренний код
#         # self.code_input = QLineEdit()
#         # self.code_input.setText(self.product_data.get('internal_code') or "")
#         # self.code_input.setPlaceholderText("Например: INT-001")
#         # form_layout.addRow("Внутренний код:", self.code_input)
#
#         # Внутренний код
#         self.code_input = QLineEdit()
#
#         # АВТОЗАПОЛНЕНИЕ: если это новый товар (id=None), генерируем код
#         if self.product_data.get('id') is None:
#             from backend.database import get_next_internal_code
#             next_code = get_next_internal_code()
#             self.code_input.setText(next_code)
#             self.code_input.setReadOnly(True)  # Делаем поле только для чтения
#             # self.code_input.setStyleSheet("background-color: #F3F4F6; color: #6B7280;")
#         else:
#             # Для редактирования — показываем существующий код
#             self.code_input.setText(self.product_data.get('internal_code') or "")
#
#         self.code_input.setPlaceholderText("Например: INT-001")
#         form_layout.addRow("Внутренний код:", self.code_input)
#
#         # Название
#         self.name_input = QLineEdit()
#         self.name_input.setText(self.product_data.get('name', ""))
#         self.name_input.setPlaceholderText("Название товара")
#         form_layout.addRow("Название:", self.name_input)
#
#         # Категория
#         self.category_input = QLineEdit()
#         self.category_input.setText(self.product_data.get('category', ""))
#         self.category_input.setPlaceholderText("Категория")
#         form_layout.addRow("Категория:", self.category_input)
#
#         # Ключевые слова
#         self.keywords_input = QLineEdit()
#         self.keywords_input.setText(self.product_data.get('keywords') or "")
#         self.keywords_input.setPlaceholderText("Ключевые слова через запятую")
#         form_layout.addRow("Ключевые слова:", self.keywords_input)
#
#         layout.addLayout(form_layout)
#         layout.addStretch()
#
#         # Кнопки
#         buttons_layout = QHBoxLayout()
#         buttons_layout.setSpacing(15)
#
#         self.clear_btn = QPushButton("Очистить")
#         self.clear_btn.setFixedHeight(40)
#         self.clear_btn.setObjectName("secondaryButton")
#         self.clear_btn.clicked.connect(self.clear_form)
#
#         self.cancel_btn = QPushButton("Отмена")
#         self.cancel_btn.setFixedHeight(40)
#         self.cancel_btn.setObjectName("cancelButton")
#         self.cancel_btn.clicked.connect(self.reject)
#
#         self.save_btn = QPushButton("Сохранить")
#         self.save_btn.setFixedHeight(40)
#         self.save_btn.setObjectName("saveButton")
#         self.save_btn.clicked.connect(self.save_changes)
#
#         buttons_layout.addWidget(self.clear_btn)
#         buttons_layout.addWidget(self.cancel_btn)
#         buttons_layout.addWidget(self.save_btn)
#
#         layout.addLayout(buttons_layout)
#
#     def apply_styles(self):
#         self.setStyleSheet(get_dialog_styles())
#
#     def clear_form(self):
#         self.code_input.clear()
#         self.name_input.clear()
#         self.category_input.clear()
#         self.keywords_input.clear()
#         self.code_input.setFocus()
#
#     def save_changes(self):
#         if not self.name_input.text().strip():
#             QMessageBox.warning(self, "Ошибка", "Название товара обязательно!")
#             return
#         if not self.category_input.text().strip():
#             QMessageBox.warning(self, "Ошибка", "Категория обязательна!")
#             return
#         self.accept()
#
#     def get_product_data(self):
#         """Возвращаем обновленные данные, сохраняя ID"""
#         return {
#             'id': self.product_data.get('id'),
#             'internal_code': self.code_input.text().strip(),
#             'name': self.name_input.text().strip(),
#             'category': self.category_input.text().strip(),
#             'keywords': self.keywords_input.text().strip(),
#         }

"""
Диалог редактирования товара
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from ui.utils.styles import get_dialog_styles

from pathlib import Path


class EditProductDialog(QDialog):
    """Модальное окно для редактирования/добавления товара"""

    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        # product_data может быть словарем (при добавлении) или объектом (при редактировании)
        # Приводим всё к словарю для единообразия
        if isinstance(product_data, dict):
            self.product_data = product_data
        else:
            self.product_data = {
                'id': getattr(product_data, 'id', None),
                'internal_code': getattr(product_data, 'internal_code', ''),
                'name': getattr(product_data, 'name', ''),
                'category': getattr(product_data, 'category', ''),
                'keywords': getattr(product_data, 'keywords', '')
            }

        self.setWindowTitle("Редактировать товар")
        self.setFixedSize(500, 450)  # ✅ Немного увеличил высоту для иконки
        self.setModal(True)
        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # ✅ ИКОНКА ВВЕРХУ
        icon_container = QHBoxLayout()
        icon_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Создаем QLabel для иконки
        icon_label = QLabel()
        icon_label.setFixedSize(80, 80)

        # Пытаемся загрузить иконку товара (или используем заглушку)
        icon_path = Path(__file__).parent.parent / "icons" / "product.png"
        if not icon_path.exists():
            # Если иконки нет, создаем текстовую заглушку
            icon_label.setText("📦")
            icon_label.setFont(QFont("Segoe UI", 48))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            # Загружаем PNG иконку
            pixmap = QPixmap(str(icon_path))
            scaled_pixmap = pixmap.scaled(80, 80,
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_container.addWidget(icon_label)
        layout.addLayout(icon_container)

        # Заголовок
        title = QLabel("Редактирование товара")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Форма с полями
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Внутренний код
        self.code_input = QLineEdit()

        # АВТОЗАПОЛНЕНИЕ: если это новый товар (id=None), генерируем код
        if self.product_data.get('id') is None:
            from backend.database import get_next_internal_code
            next_code = get_next_internal_code()
            self.code_input.setText(next_code)
            self.code_input.setReadOnly(True)  # Делаем поле только для чтения
            self.code_input.setStyleSheet("background-color: #F3F4F6; color: #6B7280;")
        else:
            # Для редактирования — показываем существующий код
            self.code_input.setText(self.product_data.get('internal_code') or "")

        self.code_input.setPlaceholderText("Например: INT-001")
        form_layout.addRow("Внутренний код:", self.code_input)

        # Название
        self.name_input = QLineEdit()
        self.name_input.setText(self.product_data.get('name', ""))
        self.name_input.setPlaceholderText("Название товара")
        form_layout.addRow("Название:", self.name_input)

        # Ключевые слова
        self.keywords_input = QLineEdit()
        self.keywords_input.setText(self.product_data.get('keywords') or "")
        self.keywords_input.setPlaceholderText("Ключевые слова через запятую")
        form_layout.addRow("Ключевые слова:", self.keywords_input)

        layout.addLayout(form_layout)
        layout.addStretch()

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.clear_btn = QPushButton("️ Очистить")
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
        # self.category_input.clear()  # ← УБРАНО
        self.keywords_input.clear()
        self.code_input.setFocus()

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
            'category': self.product_data.get('category', 'Общее'),  # ✅ Возвращаем дефолтную категорию
            'keywords': self.keywords_input.text().strip(),
        }