import sys
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout,
                             QSizePolicy, QDialog)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройки окна
        self.setWindowTitle("Закупки ЦМИТ ЛЮКС")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)

        # Путь к папке с иконками
        self.icons_path = Path(__file__).parent / "icons"

        self.setWindowIcon(QIcon(str(self.icons_path / "cmit_logo_parody.png")))

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Создаем боковую панель и контент
        sidebar = self.create_sidebar()
        content = self.create_main_content()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        # Применяем стили
        self.apply_styles()

    def load_icon(self, filename, size=24):
        """
        Загрузка иконки из PNG файла
        :param filename: имя файла в папке icons
        :param size: размер иконки в пикселях
        :return: QPixmap или QLabel с иконкой
        """
        icon_path = self.icons_path / filename

        if icon_path.exists():
            pixmap = QPixmap(str(icon_path))
            # Масштабируем иконку до нужного размера
            scaled_pixmap = pixmap.scaled(size, size,
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            return scaled_pixmap
        else:
            # Если файл не найден, возвращаем пустую метку
            print(f"!!! Иконка не найдена: {icon_path}")
            return QPixmap(size, size)  # Пустая иконка

    def create_icon_label(self, filename, size=24):
        """Создание QLabel с иконкой"""
        label = QLabel()
        pixmap = self.load_icon(filename, size)
        label.setPixmap(pixmap)
        label.setFixedSize(size, size)
        return label

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
            ("home.png", "Главная", True),
            ("add.png", "Создать заявку", False),
            ("search.png", "История заявок", False),
            # ("suppliers.png", "Поставщики", False),
            ("product.png", "Справочник товаров", False),
            # ("contracts.png", "Договоры", False),
            # ("analytics.png", "Аналитика", False),
            ("light-bulb.png", "О предприятии", False),
            ("settings.png", "Настройки", False),
        ]

        for icon_file, text, is_active in menu_items:
            btn = self.create_menu_button(icon_file, text, is_active)
            menu_layout.addWidget(btn)

        menu_layout.addStretch()
        layout.addWidget(menu_frame)

        # # Профиль пользователя
        # profile_frame = QFrame()
        # profile_frame.setObjectName("profileFrame")
        # profile_frame.setFixedHeight(80)
        # profile_layout = QHBoxLayout(profile_frame)
        # profile_layout.setContentsMargins(20, 15, 20, 15)
        # profile_layout.setSpacing(15)

        # # Аватар (PNG иконка)
        # avatar = self.create_icon_label("user_avatar.png", size=50)
        # avatar.setStyleSheet("border-radius: 25px;")

        # Информация
        info_layout = QVBoxLayout()
        info_layout.setSpacing(3)

        # name_label = QLabel("Иванов И. И.")
        # name_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        # name_label.setStyleSheet("color: #1F2937;")
        #
        # role_label = QLabel("Отдел снабжения")
        # role_label.setFont(QFont("Segoe UI", 10))
        # role_label.setStyleSheet("color: #6B7280;")

        # info_layout.addWidget(name_label)
        # info_layout.addWidget(role_label)
        #
        # profile_layout.addWidget(avatar)
        # profile_layout.addLayout(info_layout)
        # profile_layout.addStretch()
        #
        # layout.addWidget(profile_frame)

        return sidebar

    def create_menu_button(self, icon_file, text, is_active):
        """Создание кнопки меню с иконкой"""
        btn = QPushButton()
        btn.setObjectName("activeMenu" if is_active else "menuButton")
        btn.setFixedHeight(50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont("Segoe UI", 13))

        # Создаем layout для кнопки
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(20, 10, 20, 10)
        btn_layout.setSpacing(15)

        # Иконка
        icon_label = self.create_icon_label(icon_file, size=24)

        # Текст
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(text_label)
        btn_layout.addStretch()

        return btn

    def create_main_content(self):
        """Создание основного контента"""
        content = QWidget()
        content.setObjectName("mainContent")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(30)

        # Заголовок страницы
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)

        title = QLabel("Главная")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")

        subtitle = QLabel("Добро пожаловать в систему автоматизации закупок ЦМИТ ЛЮКС")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #6B7280;")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        layout.addLayout(header_layout)
        layout.addSpacing(20)

        # Сетка карточек (2x2)
        cards_widget = QWidget()
        cards_layout = QGridLayout(cards_widget)
        cards_layout.setSpacing(25)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        # Данные карточек с PNG иконками
        cards_data = [
            ("add.png", "Создание новой заявки",
             "Создайте новую заявку на закупку товаров",
             "#3B82F6", "#EFF6FF"),

            ("search.png", "История заявок",
             "Просмотрите ваши предыдущие заявки",
             "#10B981", "#D1FAE5"),

            ("product.png", "Справочник товаров",
             "Просмотрите или редактируйте актуальные товары предприятия",
             "#8B5CF6", "#FFFACD"),

            ("door.png", "Выход из приложения",
             "Завершить работу и выйти из системы",
             "#EF4444", "#FEE2E2"),
        ]

        # Создаем карточки
        for i, (icon_file, title, description, icon_color, bg_color) in enumerate(cards_data):
            card = self.create_card(icon_file, title, description, bg_color)
            row = i // 2
            col = i % 2
            cards_layout.addWidget(card, row, col)

        layout.addWidget(cards_widget)
        layout.addStretch()

        return content

    def create_card(self, icon_file, title, description, bg_color):
        """Создание карточки с PNG иконкой"""
        card = QFrame()
        card.setObjectName("card")
        card.setFixedHeight(200)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(25)

        # Иконка с фоном
        icon_container = QFrame()
        icon_container.setFixedSize(90, 90)
        icon_container.setStyleSheet(f"background-color: {bg_color}; border-radius: 15px;")

        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # PNG иконка
        icon_label = self.create_icon_label(icon_file, size=50)
        icon_layout.addWidget(icon_label)

        # Текст
        text_layout = QVBoxLayout()
        text_layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1F2937;")
        title_label.setWordWrap(True)

        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 12))
        desc_label.setStyleSheet("color: #6B7280;")
        desc_label.setWordWrap(True)

        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)

        layout.addWidget(icon_container)
        layout.addLayout(text_layout)
        layout.addStretch()

        # Стрелка
        arrow = QLabel("→")
        arrow.setFont(QFont("Segoe UI", 28))
        arrow.setStyleSheet("color: #9CA3AF;")
        layout.addWidget(arrow)

        # Подключение клика
        card.mousePressEvent = lambda event, t=title: self.on_card_click(t)

        return card

    def on_card_click(self, card_title):
        """Обработчик клика на карточку"""
        if card_title == "Выход из приложения":
            self.show_exit_confirmation()
        elif card_title == "Создание новой заявки":
            # Переход на экран создания заявки
            print("Переход к созданию заявки")
        elif card_title == "История заявок":
            print("Переход к истории заявок")
        elif card_title == "Справочник товаров":
            print("Переход к справочнику товаров")

# ОБРАБОТКА КНОПКИ ВЫХОДА ИЗ ПРИЛОЖЕНИЯ
    def show_exit_confirmation(self):
        """Показать окно подтверждения выхода"""
        # Создаем модальное окно
        dialog = QDialog(self)
        dialog.setWindowTitle("Выход из приложения")
        dialog.setFixedSize(450, 200)
        dialog.setWindowIcon(QIcon(str(self.icons_path / "warning.png")))

        # Layout для диалога
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Жирный заголовок
        title_label = QLabel("Вы точно хотите уйти?")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Серый подтекст
        subtitle_label = QLabel("Возможно, остались незавершенные дела")
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setStyleSheet("color: #6B7280;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setWordWrap(True)
        layout.addWidget(subtitle_label)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        # Кнопка "Отмена"
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
        cancel_btn.clicked.connect(dialog.reject)  # Закрыть диалог

        # Кнопка "Выйти"
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

        # Показываем диалог модально
        dialog.exec()

    def confirm_exit(self, dialog):
        """Подтверждение выхода"""
        dialog.accept()  # Закрываем диалог
        self.close()  # Закрываем главное окно

    def apply_styles(self):
        """Применение стилей (CSS)"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F9FAFB;
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
            }

            #profileFrame {
                background-color: #F9FAFB;
                border-top: 1px solid #E5E7EB;
            }

            #mainContent {
                background-color: #F9FAFB;
            }

            #card {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
            }

            #card:hover {
                border: 2px solid #3B82F6;
                background-color: #FFFFFF;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Устанавливаем современный стиль
    app.setStyle("Fusion")

    # Устанавливаем шрифт по умолчанию
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())