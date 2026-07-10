import sys
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QSizePolicy, QApplication, QDialog,
                             QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon


class HistoryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Путь к папке с иконками
        self.icons_path = Path(__file__).parent / "icons"

        # Настройки окна
        self.setWindowTitle("История закупок - Закупки ЦМИТ ЛЮКС")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)

        # Иконка окна
        icon_path = self.icons_path / "cmit_logo_parody.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Создаем интерфейс
        self.create_widgets()
        self.apply_styles()

    def create_sidebar(self):
        """Создание боковой панели"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Логотип и название приложения
        logo_frame = QFrame()
        logo_frame.setObjectName("logoFrame")
        logo_frame.setFixedHeight(80)
        logo_layout = QHBoxLayout(logo_frame)
        logo_layout.setContentsMargins(25, 20, 20, 20)
        logo_layout.setSpacing(15)

        logo_icon = self.create_icon_label("cmit_logo_parody.png", size=40)
        logo_text = QLabel("ЦМИТ ЛЮКС")
        logo_text.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        logo_text.setStyleSheet("color: #1F2937;")

        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()

        layout.addWidget(logo_frame)

        # Меню навигации
        menu_frame = QFrame()
        menu_frame.setObjectName("menuFrame")
        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setContentsMargins(10, 20, 10, 20)
        menu_layout.setSpacing(5)

        menu_items = [
            ("home.png", "Главная", False),
            ("add.png", "Создать заявку", False),
            ("search.png", "История заявок", True),  # ← Активная кнопка
            ("product.png", "Справочник товаров", False),
            ("light-bulb.png", "О предприятии", False),
            ("settings.png", "Настройки", False),
        ]

        for icon_file, text, is_active in menu_items:
            btn = self.create_menu_button(icon_file, text, is_active)
            menu_layout.addWidget(btn)

        menu_layout.addStretch()
        layout.addWidget(menu_frame)

        return sidebar

    def create_menu_button(self, icon_file, text, is_active):
        """Создание кнопки меню с иконкой"""
        btn = QPushButton()
        btn.setObjectName("activeMenu" if is_active else "menuButton")
        btn.setFixedHeight(50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont("Segoe UI", 13))
        btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(20, 10, 20, 10)
        btn_layout.setSpacing(15)

        icon_label = self.create_icon_label(icon_file, size=24)
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(text_label)
        btn_layout.addStretch()

        return btn

    def create_widgets(self):
        """Создание элементов интерфейса"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Основной контент
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(50, 40, 50, 40)
        content_layout.setSpacing(30)

        # Заголовок страницы
        title = QLabel("История закупок")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")

        subtitle = QLabel("Просматривайте информацию о прошлых закупках")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #6B7280;")

        content_layout.addWidget(title)
        content_layout.addWidget(subtitle)
        content_layout.addSpacing(10)

        # Скроллируемая область для карточек
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(15)

        # Мок-данные для истории закупок
        history_data = [
            {
                "date": "15.06.2024",
                "time": "10:30",
                "number": "125",
                "description": "Канцелярские товары для офиса",
                "amount": "45 230 ₽",
                "items_count": 12,
            },
            {
                "date": "10.06.2024",
                "time": "14:15",
                "number": "124",
                "description": "Расходные материалы для принтеров",
                "amount": "18 750 ₽",
                "items_count": 7,
            },
            {
                "date": "05.06.2024",
                "time": "09:20",
                "number": "123",
                "description": "Электротехническая продукция",
                "amount": "76 890 ₽",
                "items_count": 15,
            },
            {
                "date": "28.05.2024",
                "time": "16:45",
                "number": "122",
                "description": "Хозяйственные товары",
                "amount": "9 430 ₽",
                "items_count": 5,
            },
            {
                "date": "21.05.2024",
                "time": "11:05",
                "number": "121",
                "description": "Компьютерная периферия",
                "amount": "34 560 ₽",
                "items_count": 9,
            },
        ]

        # Создаем карточки закупок
        for data in history_data:
            card = self.create_history_card(data)
            scroll_layout.addWidget(card)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)

        content_layout.addWidget(scroll_area)

        # Нижняя панель: кнопка "Назад" + пагинация
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Кнопка "Назад"
        back_btn = QPushButton("← Назад")
        back_btn.setFont(QFont("Segoe UI", 12))
        back_btn.setFixedSize(130, 40)
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.go_back)

        bottom_layout.addWidget(back_btn)
        bottom_layout.addStretch()

        # Информация о пагинации
        pagination_info = QLabel("1–5 из 25 закупок")
        pagination_info.setFont(QFont("Segoe UI", 11))
        pagination_info.setStyleSheet("color: #6B7280;")
        bottom_layout.addWidget(pagination_info)

        # Кнопки пагинации
        pagination = self.create_pagination()
        bottom_layout.addWidget(pagination)

        content_layout.addLayout(bottom_layout)

        # Мини-карточка выхода в правом нижнем углу
        exit_layout = QHBoxLayout()
        exit_layout.addStretch()

        exit_card = self.create_exit_card()
        exit_card.mousePressEvent = lambda event: self.show_exit_confirmation()

        exit_layout.addWidget(exit_card)

        content_layout.addLayout(exit_layout)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def create_history_card(self, data):
        """Создание карточки одной закупки"""
        card = QFrame()
        card.setObjectName("historyCard")
        card.setFixedHeight(110)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(20)

        # Блок с датой и иконкой календаря
        date_block = QFrame()
        date_block.setObjectName("dateBlock")
        date_block.setFixedSize(90, 70)

        date_layout = QVBoxLayout(date_block)
        date_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_layout.setSpacing(2)

        icon_label = self.create_icon_label("calendar.png", size=28)
        date_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        date_text = QLabel(f"{data['date']}\n{data['time']}")
        date_text.setFont(QFont("Segoe UI", 9))
        date_text.setStyleSheet("color: #6B7280;")
        date_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_layout.addWidget(date_text)

        layout.addWidget(date_block)

        # Разделитель
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.VLine)
        separator1.setStyleSheet("background-color: #E5E7EB;")
        separator1.setFixedWidth(1)
        layout.addWidget(separator1)

        # Номер закупки и описание
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        number_label = QLabel(f"Закупка №{data['number']}")
        number_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        number_label.setStyleSheet("color: #1F2937;")

        desc_label = QLabel(data['description'])
        desc_label.setFont(QFont("Segoe UI", 11))
        desc_label.setStyleSheet("color: #6B7280;")

        info_layout.addWidget(number_label)
        info_layout.addWidget(desc_label)

        layout.addLayout(info_layout)

        # Разделитель
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.VLine)
        separator2.setStyleSheet("background-color: #E5E7EB;")
        separator2.setFixedWidth(1)
        layout.addWidget(separator2)

        # Сумма
        amount_layout = QVBoxLayout()
        amount_layout.setSpacing(3)

        amount_title = QLabel("Сумма")
        amount_title.setFont(QFont("Segoe UI", 10))
        amount_title.setStyleSheet("color: #6B7280;")

        amount_value = QLabel(data['amount'])
        amount_value.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        amount_value.setStyleSheet("color: #1F2937;")

        amount_layout.addWidget(amount_title)
        amount_layout.addWidget(amount_value)

        layout.addLayout(amount_layout)

        # Разделитель
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.Shape.VLine)
        separator3.setStyleSheet("background-color: #E5E7EB;")
        separator3.setFixedWidth(1)
        layout.addWidget(separator3)

        # Количество товаров
        items_layout = QVBoxLayout()
        items_layout.setSpacing(3)

        items_title = QLabel("Товаров")
        items_title.setFont(QFont("Segoe UI", 10))
        items_title.setStyleSheet("color: #6B7280;")

        items_value = QLabel(str(data['items_count']))
        items_value.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        items_value.setStyleSheet("color: #1F2937;")

        items_layout.addWidget(items_title)
        items_layout.addWidget(items_value)

        layout.addLayout(items_layout)

        layout.addStretch()

        # Кнопки действий
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Кнопка "Открыть"
        open_btn = QPushButton("Открыть")
        open_btn.setFont(QFont("Segoe UI", 11))
        open_btn.setFixedSize(100, 35)
        open_btn.setObjectName("openButton")
        open_btn.clicked.connect(lambda: self.open_procurement(data['number']))

        # Кнопка "Экспорт"
        export_btn = QPushButton("Экспорт")
        export_btn.setFont(QFont("Segoe UI", 11))
        export_btn.setFixedSize(100, 35)
        export_btn.setObjectName("exportButton")
        export_btn.clicked.connect(lambda: self.export_procurement(data['number']))

        # Кнопка "Удалить"
        delete_btn = QPushButton("Удалить")
        delete_btn.setFont(QFont("Segoe UI", 11))
        delete_btn.setFixedSize(100, 35)
        delete_btn.setObjectName("deleteButton")
        delete_btn.clicked.connect(lambda: self.delete_procurement(data['number']))

        buttons_layout.addWidget(open_btn)
        buttons_layout.addWidget(export_btn)
        buttons_layout.addWidget(delete_btn)

        layout.addLayout(buttons_layout)

        return card

    def create_pagination(self):
        """Создание блока пагинации"""
        pagination = QFrame()
        pagination.setObjectName("pagination")

        layout = QHBoxLayout(pagination)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        # Кнопки пагинации
        pages = ["<", "1", "2", "3", "...", "5", ">"]

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

    def create_exit_card(self):
        """Создание мини-карточки выхода"""
        card = QFrame()
        card.setObjectName("exitCard")
        card.setFixedSize(220, 90)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Иконка с розовым фоном
        icon_container = QFrame()
        icon_container.setFixedSize(50, 50)
        icon_container.setStyleSheet("background-color: #FEE2E2; border-radius: 10px;")

        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = self.create_icon_label("door.png", size=30)
        icon_layout.addWidget(icon_label)

        # Текст
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)

        title_label = QLabel("Выход")
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1F2937;")

        # desc_label = QLabel("Завершить работу")
        # desc_label.setFont(QFont("Segoe UI", 10))
        # desc_label.setStyleSheet("color: #6B7280;")

        text_layout.addWidget(title_label)
        # text_layout.addWidget(desc_label)

        layout.addWidget(icon_container)
        layout.addLayout(text_layout)
        layout.addStretch()

        # Стрелка
        arrow = QLabel("→")
        arrow.setFont(QFont("Segoe UI", 18))
        arrow.setStyleSheet("color: #9CA3AF;")
        layout.addWidget(arrow)

        return card

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

    def open_procurement(self, number):
        """Открыть закупку"""
        print(f"Открытие закупки №{number}")

    def export_procurement(self, number):
        """Экспорт закупки"""
        print(f"Экспорт закупки №{number}")

    def delete_procurement(self, number):
        """Удалить закупку"""
        print(f"Удаление закупки №{number}")

    def go_back(self):
        """Вернуться назад"""
        self.close()

    def show_exit_confirmation(self):
        """Показать окно подтверждения выхода"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Выход из приложения")
        dialog.setFixedSize(450, 220)
        dialog.setWindowIcon(self.windowIcon())

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        icon_label = self.create_icon_label("warning.png", size=50)
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("Вы точно хотите уйти?")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        subtitle_label = QLabel("Возможно, остались незавершенные дела")
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setStyleSheet("color: #6B7280;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setFont(QFont("Segoe UI", 12))
        cancel_btn.setFixedSize(150, 45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                color: #374151;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)

        exit_btn = QPushButton("Выйти")
        exit_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        exit_btn.setFixedSize(150, 45)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        exit_btn.clicked.connect(lambda: self.confirm_exit(dialog))

        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(exit_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        dialog.exec()

    def confirm_exit(self, dialog):
        """Подтверждение выхода"""
        dialog.accept()
        self.close()

    def apply_styles(self):
        """Применение стилей"""
        self.setStyleSheet("""
            QWidget {
                background-color: #F9FAFB;
            }

            QLabel {
                selection-background-color: transparent;
                selection-color: transparent;
                background-color: transparent;
            }

            QToolTip {
                background-color: #F9FAFB;
                color: #334155;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 12px;
                font-family: 'Segoe UI';
            }

            QPushButton {
                selection-background-color: transparent;
                selection-color: transparent;
                outline: none;
            }

            #sidebar {
                background-color: #FFFFFF;
                border-right: 1px solid #E5E7EB;
            }

            #logoFrame {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E5E7EB;
            }

            #menuFrame {
                background-color: #FFFFFF;
            }

            QPushButton#menuButton {
                background-color: transparent;
                border: none;
                color: #4B5563;
                border-radius: 10px;
                text-align: left;
            }

            QPushButton#menuButton:hover {
                background-color: #F3F4F6;
                color: #3B82F6;
            }

            QPushButton#activeMenu {
                background-color: #EFF6FF;
                border: none;
                color: #3B82F6;
                border-radius: 10px;
                text-align: left;
                border-left: 4px solid #3B82F6;
                font-weight: bold;
            }

            #historyCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }

            #historyCard:hover {
                border: 2px solid #3B82F6;
            }

            #dateBlock {
                background-color: #F3F4FF;
                border-radius: 8px;
            }

            #openButton {
                background-color: #EFF6FF;
                color: #3B82F6;
                border: 1px solid #BFDBFE;
                border-radius: 6px;
            }

            #openButton:hover {
                background-color: #DBEAFE;
            }

            #exportButton {
                background-color: #FFFFFF;
                color: #374151;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
            }

            #exportButton:hover {
                background-color: #F3F4F6;
            }

            #deleteButton {
                background-color: #FFFFFF;
                color: #EF4444;
                border: 1px solid #FECACA;
                border-radius: 6px;
            }

            #deleteButton:hover {
                background-color: #FEE2E2;
            }

            #backButton {
                background-color: #FFFFFF;
                color: #374151;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
            }

            #backButton:hover {
                background-color: #F3F4F6;
            }

            #currentPage {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 6px;
            }

            #pageButton {
                background-color: #FFFFFF;
                color: #374151;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
            }

            #pageButton:hover {
                background-color: #F3F4F6;
            }

            #navButton {
                background-color: #FFFFFF;
                color: #6B7280;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
            }

            #navButton:hover {
                background-color: #F3F4F6;
            }

            #exitCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }

            #exitCard:hover {
                border: 2px solid #EF4444;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    window = HistoryWindow()
    window.show()

    sys.exit(app.exec())