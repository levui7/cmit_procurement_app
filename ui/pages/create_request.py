import sys
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QSpinBox, QLineEdit,
                             QDateEdit, QComboBox, QSizePolicy, QApplication)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QPixmap, QIcon

from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

from ui.styles import get_create_request_styles

class CreateRequestPage(QWidget):
    def __init__(self, icons_path, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path
        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(30)

        title = QLabel("Создание заявки")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")

        subtitle = QLabel("Укажите параметры закупки для подбора оптимальных предложений")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #6B7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)

        form_card = QFrame()
        form_card.setObjectName("formCard")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(30)

        # ✅ Поле 1: Количество студентов (ОДИН вызов!)
        self.students_spinbox = self.create_students_input()
        students_row = self.create_form_row(
            "group.png",
            "Количество студентов",
            self.students_spinbox,  # ← Используем сохранённое поле
            tooltip_text="Общее количество студентов, которые будут использовать оборудование в течение года"
        )
        form_layout.addLayout(students_row)
        form_layout.addWidget(self.create_separator())

        # ✅ Поле 2: Ограничения по цене (используем create_price_layout)
        self.min_price_edit, self.max_price_edit = self.create_price_input()
        price_layout = self.create_price_layout(self.min_price_edit, self.max_price_edit)
        price_row = self.create_form_row(
            "ruble.png",
            "Ограничения по цене",
            price_layout,  # ← Передаём layout, а не кортеж!
            tooltip_text="Минимальная и максимальная стоимость за единицу товара в рублях"
        )
        form_layout.addLayout(price_row)
        form_layout.addWidget(self.create_separator())

        # ✅ Поле 3: Желаемая дата доставки (ОДИН вызов!)
        self.date_edit = self.create_date_input()
        date_row = self.create_form_row(
            "calendar.png",
            "Желаемая дата доставки",
            self.date_edit,  # ← Используем сохранённое поле
            tooltip_text="Дата, к которой необходимо получить все товары"
        )
        form_layout.addLayout(date_row)
        form_layout.addWidget(self.create_separator())

        # ✅ Поле 4: Рейтинг товара
        self.rating_combo = self.create_rating_input()
        rating_row = self.create_form_row(
            "star.png",
            "Рейтинг товара",
            self.rating_combo,  # ← Используем сохранённое поле
            tooltip_text="Минимальный рейтинг товара на маркетплейсе"
        )
        form_layout.addLayout(rating_row)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        clear_btn = QPushButton("Очистить")
        clear_btn.setFont(QFont("Segoe UI", 12))
        clear_btn.setFixedSize(150, 45)
        clear_btn.setObjectName("clearButton")
        clear_btn.clicked.connect(self.clear_form)

        next_btn = QPushButton("Далее")
        next_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        next_btn.setFixedSize(150, 45)
        next_btn.setObjectName("nextButton")
        next_btn.clicked.connect(self.on_next)

        buttons_layout.addStretch()
        buttons_layout.addWidget(clear_btn)
        buttons_layout.addWidget(next_btn)

        layout.addWidget(form_card)
        layout.addStretch()
        layout.addLayout(buttons_layout)

    def create_form_row(self, icon_file, label_text, input_widget, tooltip_text=""):
        """Создание строки формы с иконкой, заголовком и полем ввода"""
        row_layout = QHBoxLayout()
        row_layout.setSpacing(20)
        row_layout.setContentsMargins(0, 10, 0, 10)

        # Иконка слева
        icon_container = QFrame()
        icon_container.setFixedSize(60, 60)
        icon_container.setObjectName("iconContainer")

        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = self.create_icon_label(icon_file, size=30)
        icon_layout.addWidget(icon_label)

        row_layout.addWidget(icon_container)

        # Правая часть (заголовок + поле ввода)
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

        # Заголовок с иконкой информации
        title_layout = QHBoxLayout()
        title_layout.setSpacing(5)

        title_label = QLabel(label_text)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1F2937;")
        title_layout.addWidget(title_label)

        # # Иконка информации (i)
        # info_icon = QLabel("ⓘ")
        # info_icon.setFont(QFont("Segoe UI", 12))
        # info_icon.setStyleSheet("color: #9CA3AF;")
        # title_layout.addWidget(info_icon)
        # title_layout.addStretch()

        # Иконка информации (i)
        info_icon = QLabel("ⓘ")
        info_icon.setFont(QFont("Segoe UI", 12))
        info_icon.setStyleSheet("color: #9CA3AF;")
        info_icon.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        # ✅ ДОБАВИТЬ ПОДСКАЗКУ
        if tooltip_text:
            info_icon.setToolTip(tooltip_text)
            info_icon.setCursor(Qt.CursorShape.WhatsThisCursor)  # Меняем курсор на "помощь"

        title_layout.addWidget(info_icon)
        title_layout.addStretch()

        right_layout.addLayout(title_layout)
        # right_layout.addWidget(input_widget)
        if isinstance(input_widget, QHBoxLayout) or isinstance(input_widget, QVBoxLayout):
            right_layout.addLayout(input_widget)
        else:
            right_layout.addWidget(input_widget)

        row_layout.addLayout(right_layout)

        return row_layout

    def create_students_input(self):
        """Поле ввода количества студентов"""
        spinbox = QSpinBox()
        spinbox.setMinimum(1)
        spinbox.setMaximum(10000)
        spinbox.setValue(100)
        spinbox.setFont(QFont("Segoe UI", 12))
        spinbox.setFixedHeight(45)
        spinbox.setObjectName("inputField")
        return spinbox

    # def create_price_input(self):
    #     """Поля ввода мин/макс цены"""
    #     price_layout = QHBoxLayout()
    #     price_layout.setSpacing(15)
    #
    #     # Валидатор: только цифры и пробелы
    #     validator = QRegularExpressionValidator(
    #         QRegularExpression(r'^[0-9\s]*$')  # Разрешаем только цифры и пробелы
    #     )
    #
    #     # Минимум
    #     min_edit = QLineEdit()
    #     min_edit.setPlaceholderText("Минимум, ₽")
    #     min_edit.setText("500")
    #     min_edit.setFont(QFont("Segoe UI", 12))
    #     min_edit.setFixedHeight(45)
    #     min_edit.setObjectName("inputField")
    #     min_edit.setValidator(validator)
    #
    #     # Разделитель "-"
    #     separator = QLabel("—")
    #     separator.setFont(QFont("Segoe UI", 14))
    #     separator.setStyleSheet("color: #6B7280;")
    #
    #     # Максимум
    #     max_edit = QLineEdit()
    #     max_edit.setPlaceholderText("Максимум, ₽")
    #     max_edit.setText("2 500")
    #     max_edit.setFont(QFont("Segoe UI", 12))
    #     max_edit.setFixedHeight(45)
    #     max_edit.setObjectName("inputField")
    #     max_edit.setValidator(validator)
    #
    #     price_layout.addWidget(min_edit)
    #     price_layout.addWidget(separator)
    #     price_layout.addWidget(max_edit)
    #
    #     return price_layout

    def create_price_input(self):
        """Создание полей мин/макс цены (возвращает сами поля)"""
        # Создаём валидатор: только цифры и пробелы
        from PyQt6.QtGui import QRegularExpressionValidator
        from PyQt6.QtCore import QRegularExpression

        validator = QRegularExpressionValidator(
            QRegularExpression(r'^[0-9\s]*$')
        )

        # Минимум
        min_edit = QLineEdit()
        min_edit.setPlaceholderText("Минимум, ₽")
        min_edit.setText("500")
        min_edit.setFont(QFont("Segoe UI", 12))
        min_edit.setFixedHeight(45)
        min_edit.setObjectName("inputField")
        min_edit.setValidator(validator)

        # Максимум
        max_edit = QLineEdit()
        max_edit.setPlaceholderText("Максимум, ₽")
        max_edit.setText("2 500")
        max_edit.setFont(QFont("Segoe UI", 12))
        max_edit.setFixedHeight(45)
        max_edit.setObjectName("inputField")
        max_edit.setValidator(validator)

        return min_edit, max_edit

    def create_price_layout(self, min_edit, max_edit):
        """Создание layout для полей цены"""
        price_layout = QHBoxLayout()
        price_layout.setSpacing(15)

        # Разделитель "-"
        separator = QLabel("—")
        separator.setFont(QFont("Segoe UI", 14))
        separator.setStyleSheet("color: #6B7280;")

        price_layout.addWidget(min_edit)
        price_layout.addWidget(separator)
        price_layout.addWidget(max_edit)

        return price_layout

    def create_date_input(self):
        """Поле выбора даты"""
        date_edit = QDateEdit()
        date_edit.setDate(QDate(2024, 6, 15))
        date_edit.setDisplayFormat("dd.MM.yyyy")
        date_edit.setFont(QFont("Segoe UI", 12))
        date_edit.setFixedHeight(45)
        date_edit.setFixedWidth(300)
        date_edit.setCalendarPopup(True)  # Показывать календарь при клике
        date_edit.setObjectName("inputField")
        return date_edit

    def create_rating_input(self):
        """Поле выбора рейтинга"""
        rating_layout = QHBoxLayout()
        rating_layout.setSpacing(15)

        # Выпадающий список
        combo = QComboBox()
        combo.addItems(["4 и выше", "3 и выше", "2 и выше", "1 и выше"])
        combo.setCurrentIndex(0)
        combo.setFont(QFont("Segoe UI", 12))
        combo.setFixedHeight(45)
        combo.setFixedWidth(200)
        combo.setObjectName("inputField")

        rating_layout.addWidget(combo)
        rating_layout.addStretch()

        # return rating_layout
        return combo

    def create_separator(self):
        """Создание разделительной линии"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #E5E7EB; border: none;")
        separator.setFixedHeight(1)
        return separator

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

    def clear_form(self):
        """Очистка формы"""
        # Сброс количества студентов
        self.students_spinbox.setValue(100)

        # Сброс цен
        self.min_price_edit.setText("500")
        self.max_price_edit.setText("2 500")

        # Сброс даты
        self.date_edit.setDate(QDate(2024, 6, 15))

        # Сброс рейтинга
        self.rating_combo.setCurrentIndex(0)  # "4 и выше"

    def on_next(self):
        """Обработчик кнопки 'Далее'"""
        print("Переход к следующему шагу")
        # Здесь будет логика перехода к результатам

    def apply_styles(self):
        self.setStyleSheet(get_create_request_styles())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    # Для тестирования создаем временное окно
    from PyQt6.QtWidgets import QMainWindow

    window = QMainWindow()
    window.setWindowTitle("Тест: Создание заявки")
    window.setGeometry(100, 100, 1400, 900)

    icons_path = Path(__file__).parent / "icons"
    page = CreateRequestPage(icons_path)
    window.setCentralWidget(page)

    window.show()
    sys.exit(app.exec())