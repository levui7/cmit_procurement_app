import sys
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QSizePolicy, QApplication, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon


class AboutWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Путь к папке с иконками
        self.icons_path = Path(__file__).parent / "icons"

        # Настройки окна
        self.setWindowTitle("О предприятии - Закупки ЦМИТ ЛЮКС")
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

        # Логотип (PNG иконка)
        logo_icon = self.create_icon_label("cmit_logo_parody.png", size=40)

        # Название
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

        # Элементы меню с PNG иконками
        menu_items = [
            ("home.png", "Главная", False),
            ("add.png", "Создать заявку", False),
            ("search.png", "История заявок", False),
            ("product.png", "Справочник товаров", False),
            ("light-bulb.png", "О предприятии", True),  # ← Активная кнопка
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

        # Создаем layout для кнопки
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(20, 10, 20, 10)
        btn_layout.setSpacing(15)

        # Иконка
        icon_label = self.create_icon_label(icon_file, size=24)

        # Текст
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        text_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(text_label)
        btn_layout.addStretch()

        return btn

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # ГЛАВНЫЙ LAYOUT С SIDEBAR
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Основной контент (справа от sidebar)
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(50, 40, 50, 40)
        content_layout.setSpacing(30)

        # Заголовок страницы
        title = QLabel("О предприятии ЦМИТ ЛЮКС")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")

        subtitle = QLabel("Малое инновационное предприятие "
                          "\nЦентр Молодежного Инновационного Творчества "
                          "\nЛаборатория Юных Конструкторов")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #6B7280;")

        content_layout.addWidget(title)
        content_layout.addWidget(subtitle)
        content_layout.addSpacing(10)

        # Карточка с информацией
        info_card = QFrame()
        info_card.setObjectName("infoCard")
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(40, 40, 40, 40)
        info_layout.setSpacing(25)

        # Описание предприятия
        description = QLabel(
            "Это площадка, на которой собран комплект уникального оборудования и специализированного программного обеспечения (ПО) "
            "для быстрого прототипирования и мелкосерийного производства. "
            "\n"
            "\nЦМИТ предоставляет открытый доступ молодым ученым и школьникам, начиная с первого класса, "
            "к самым современным инструментам и подходам для производства сложных систем с использованием аддитивных технологий."
        )
        description.setFont(QFont("Segoe UI", 13))
        description.setStyleSheet("color: #374151;")
        description.setWordWrap(True)
        info_layout.addWidget(description)

        # # Разделитель
        # info_layout.addWidget(self.create_separator())
        #
        # # Направления деятельности
        # directions_title = QLabel("Направления деятельности")
        # directions_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        # directions_title.setStyleSheet("color: #1F2937;")
        # info_layout.addWidget(directions_title)
        #
        # # Карточки направлений
        # directions_layout = QHBoxLayout()
        # directions_layout.setSpacing(20)
        #
        # directions = [
        #     ("robot.png", "Робототехника", "Разработка автономных роботизированных систем"),
        #     ("exoskeleton.png", "Экзоскелеты", "Проектирование вспомогательных устройств"),
        #     ("automation.png", "Автоматизация", "Создание систем управления процессами"),
        # ]

        # for icon_file, title_text, desc_text in directions:
        #     direction_card = self.create_direction_card(icon_file, title_text, desc_text)
        #     directions_layout.addWidget(direction_card)
        #
        # info_layout.addLayout(directions_layout)

        content_layout.addWidget(info_card)
        content_layout.addStretch()

        # # Кнопка выхода в правом нижнем углу
        # exit_layout = QHBoxLayout()
        # exit_layout.addStretch()
        #
        # exit_btn = QPushButton("Выход")
        # exit_btn.setFont(QFont("Segoe UI", 11))
        # exit_btn.setFixedSize(100, 35)
        # exit_btn.setObjectName("exitButton")
        # exit_btn.clicked.connect(self.show_exit_confirmation)
        #
        # exit_layout.addWidget(exit_btn)
        #
        # content_layout.addLayout(exit_layout)

        # Мини-карточка выхода в правом нижнем углу
        exit_layout = QHBoxLayout()
        exit_layout.addStretch()

        exit_card = self.create_exit_card()
        exit_card.mousePressEvent = lambda event: self.show_exit_confirmation()

        exit_layout.addWidget(exit_card)

        content_layout.addLayout(exit_layout)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def create_direction_card(self, icon_file, title_text, description_text):
        """Создание карточки направления деятельности"""
        card = QFrame()
        card.setObjectName("directionCard")
        card.setFixedSize(280, 150)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Иконка
        icon_label = self.create_icon_label(icon_file, size=40)
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Заголовок
        title = QLabel(title_text)
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Описание
        desc = QLabel(description_text)
        desc.setFont(QFont("Segoe UI", 11))
        desc.setStyleSheet("color: #6B7280;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        return card

    def create_exit_card(self):
        """Создание мини-карточки выхода в стиле главной страницы"""
        card = QFrame()
        card.setObjectName("exitCard")
        card.setFixedSize(220, 90)  # Уменьшенный размер
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

    def show_exit_confirmation(self):
        """Показать окно подтверждения выхода"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Выход из приложения")
        dialog.setFixedSize(450, 220)
        dialog.setWindowIcon(self.windowIcon())

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        # Иконка
        icon_label = self.create_icon_label("warning.png", size=50)
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Жирный заголовок
        title_label = QLabel("Вы точно хотите уйти?")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Серый подтекст
        subtitle_label = QLabel("Возможно, остались несохраненные дела")
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setStyleSheet("color: #6B7280;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)

        # Кнопки
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

            #infoCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
            }

            #directionCard {
                background-color: #F9FAFB;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }

            #directionCard:hover {
                border: 2px solid #3B82F6;
                background-color: #FFFFFF;
            }

            #exitButton {
    background-color: #EF4444;
    color: white;
    border: none;
    border-radius: 6px;
}

#exitButton:hover {
    background-color: #DC2626;
}

#exitCard {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
}

#exitCard:hover {
    border: 2px solid #EF4444;
    background-color: #FFFFFF;
}

            #exitButton:hover {
                background-color: #DC2626;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    window = AboutWindow()
    window.show()

    sys.exit(app.exec())