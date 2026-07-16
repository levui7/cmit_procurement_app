# import sys
# import json
# from pathlib import Path
# from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#                              QPushButton, QFrame, QSizePolicy, QApplication, QDialog,
#                              QRadioButton, QButtonGroup, QCheckBox, QComboBox,
#                              QLineEdit, QSpinBox, QScrollArea, QGroupBox)
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont, QPixmap, QIcon
#
#
# class SettingsWindow(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         # Путь к папке с иконками
#         self.icons_path = Path(__file__).parent / "icons"
#
#         # Путь к файлу настроек
#         self.settings_path = Path(__file__).parent / "settings.json"
#
#         # Текущая тема
#         self.current_theme = "light"
#
#         # Настройки окна
#         self.setWindowTitle("Настройки - Закупки ЦМИТ ЛЮКС")
#         self.setGeometry(100, 100, 1400, 900)
#         self.setMinimumSize(1200, 800)
#
#         # Иконка окна
#         icon_path = self.icons_path / "cmit_logo_parody.png"
#         if icon_path.exists():
#             self.setWindowIcon(QIcon(str(icon_path)))
#
#         # Загружаем сохраненные настройки
#         self.load_settings()
#
#         # Создаем интерфейс
#         self.create_widgets()
#         self.apply_theme(self.current_theme)
#
#     def load_settings(self):
#         """Загрузка настроек из файла"""
#         if self.settings_path.exists():
#             try:
#                 with open(self.settings_path, "r", encoding="utf-8") as f:
#                     settings = json.load(f)
#                 self.current_theme = settings.get("theme", "light")
#             except Exception:
#                 self.current_theme = "light"
#         else:
#             self.current_theme = "light"
#
#     def save_settings(self):
#         """Сохранение настроек в файл"""
#         settings = {
#             "theme": self.current_theme,
#         }
#         with open(self.settings_path, "w", encoding="utf-8") as f:
#             json.dump(settings, f, ensure_ascii=False, indent=2)
#
#     def create_sidebar(self):
#         """Создание боковой панели"""
#         sidebar = QFrame()
#         sidebar.setObjectName("sidebar")
#         sidebar.setFixedWidth(280)
#
#         layout = QVBoxLayout(sidebar)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)
#
#         # Логотип и название приложения
#         logo_frame = QFrame()
#         logo_frame.setObjectName("logoFrame")
#         logo_frame.setFixedHeight(80)
#         logo_layout = QHBoxLayout(logo_frame)
#         logo_layout.setContentsMargins(25, 20, 20, 20)
#         logo_layout.setSpacing(15)
#
#         logo_icon = self.create_icon_label("cmit_logo_parody.png", size=40)
#         logo_text = QLabel("ЦМИТ ЛЮКС")
#         logo_text.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
#         logo_text.setStyleSheet("color: #1F2937;")
#
#         logo_layout.addWidget(logo_icon)
#         logo_layout.addWidget(logo_text)
#         logo_layout.addStretch()
#
#         layout.addWidget(logo_frame)
#
#         # Меню навигации
#         menu_frame = QFrame()
#         menu_frame.setObjectName("menuFrame")
#         menu_layout = QVBoxLayout(menu_frame)
#         menu_layout.setContentsMargins(10, 20, 10, 20)
#         menu_layout.setSpacing(5)
#
#         menu_items = [
#             ("home.png", "Главная", False),
#             ("add.png", "Создать заявку", False),
#             ("search.png", "История заявок", False),
#             ("product.png", "Справочник товаров", False),
#             ("light-bulb.png", "О предприятии", False),
#             ("settings.png", "Настройки", True),  # ← Активная кнопка
#         ]
#
#         for icon_file, text, is_active in menu_items:
#             btn = self.create_menu_button(icon_file, text, is_active)
#             menu_layout.addWidget(btn)
#
#         menu_layout.addStretch()
#         layout.addWidget(menu_frame)
#
#         return sidebar
#
#     def create_menu_button(self, icon_file, text, is_active):
#         """Создание кнопки меню с иконкой"""
#         btn = QPushButton()
#         btn.setObjectName("activeMenu" if is_active else "menuButton")
#         btn.setFixedHeight(50)
#         btn.setCursor(Qt.CursorShape.PointingHandCursor)
#         btn.setFont(QFont("Segoe UI", 13))
#         btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
#
#         btn_layout = QHBoxLayout(btn)
#         btn_layout.setContentsMargins(20, 10, 20, 10)
#         btn_layout.setSpacing(15)
#
#         icon_label = self.create_icon_label(icon_file, size=24)
#         text_label = QLabel(text)
#         text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
#         text_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
#
#         btn_layout.addWidget(icon_label)
#         btn_layout.addWidget(text_label)
#         btn_layout.addStretch()
#
#         btn.clicked.connect(lambda checked, page=text: self.navigate_to(page))
#
#         return btn
#
#     def create_widgets(self):
#         """Создание элементов интерфейса"""
#         main_layout = QHBoxLayout()
#         main_layout.setContentsMargins(0, 0, 0, 0)
#         main_layout.setSpacing(0)
#
#         # SIDEBAR
#         sidebar = self.create_sidebar()
#         main_layout.addWidget(sidebar)
#
#         # Скроллируемая область для контента
#         scroll_area = QScrollArea()
#         scroll_area.setWidgetResizable(True)
#         scroll_area.setObjectName("scrollArea")
#
#         scroll_widget = QWidget()
#         content_layout = QVBoxLayout(scroll_widget)
#         content_layout.setContentsMargins(50, 40, 50, 40)
#         content_layout.setSpacing(25)
#
#         # Заголовок страницы
#         title = QLabel("Настройки")
#         title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
#         title.setObjectName("mainTitle")
#
#         subtitle = QLabel("Настройте приложение под свои предпочтения")
#         subtitle.setFont(QFont("Segoe UI", 13))
#         subtitle.setObjectName("subtitle")
#
#         content_layout.addWidget(title)
#         content_layout.addWidget(subtitle)
#         content_layout.addSpacing(10)
#
#         # Секция 1: Оформление
#         appearance_group = self.create_settings_group(
#             "Оформление",
#             "Выберите тему и внешний вид приложения"
#         )
#         appearance_layout = QVBoxLayout()
#         appearance_layout.setSpacing(15)
#
#         # Переключатель темы
#         theme_label = QLabel("Тема оформления")
#         theme_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         appearance_layout.addWidget(theme_label)
#
#         theme_options_layout = QHBoxLayout()
#         theme_options_layout.setSpacing(15)
#
#         self.theme_group = QButtonGroup()
#
#         self.light_radio = QRadioButton("️Светлая")
#         self.light_radio.setFont(QFont("Segoe UI", 12))
#         self.light_radio.setObjectName("themeRadio")
#         self.light_radio.setChecked(self.current_theme == "light")
#         self.light_radio.toggled.connect(lambda: self.on_theme_change("light"))
#
#         self.dark_radio = QRadioButton("Темная")
#         self.dark_radio.setFont(QFont("Segoe UI", 12))
#         self.dark_radio.setObjectName("themeRadio")
#         self.dark_radio.setChecked(self.current_theme == "dark")
#         self.dark_radio.toggled.connect(lambda: self.on_theme_change("dark"))
#
#         self.system_radio = QRadioButton("Системная")
#         self.system_radio.setFont(QFont("Segoe UI", 12))
#         self.system_radio.setObjectName("themeRadio")
#         self.system_radio.setChecked(self.current_theme == "system")
#         self.system_radio.toggled.connect(lambda: self.on_theme_change("system"))
#
#         self.theme_group.addButton(self.light_radio)
#         self.theme_group.addButton(self.dark_radio)
#         self.theme_group.addButton(self.system_radio)
#
#         theme_options_layout.addWidget(self.light_radio)
#         theme_options_layout.addWidget(self.dark_radio)
#         theme_options_layout.addWidget(self.system_radio)
#         theme_options_layout.addStretch()
#
#         appearance_layout.addLayout(theme_options_layout)
#
#         # Размер шрифта
#         font_size_layout = QHBoxLayout()
#         font_size_layout.setSpacing(15)
#
#         font_size_label = QLabel("Размер шрифта интерфейса")
#         font_size_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         font_size_layout.addWidget(font_size_label)
#
#         font_size_layout.addStretch()
#
#         self.font_size_combo = QComboBox()
#         self.font_size_combo.addItems(["Маленький (10)", "Обычный (12)", "Крупный (14)", "Очень крупный (16)"])
#         self.font_size_combo.setCurrentIndex(1)
#         self.font_size_combo.setFixedWidth(200)
#         self.font_size_combo.setFixedHeight(40)
#         self.font_size_combo.setObjectName("settingsCombo")
#         font_size_layout.addWidget(self.font_size_combo)
#
#         appearance_layout.addLayout(font_size_layout)
#
#         appearance_group.layout().addLayout(appearance_layout)
#         content_layout.addWidget(appearance_group)
#
#         # Секция 2: Общие настройки
#         general_group = self.create_settings_group(
#             "Общие",
#             "Основные параметры работы приложения"
#         )
#         general_layout = QVBoxLayout()
#         general_layout.setSpacing(15)
#
#         # Язык интерфейса
#         lang_layout = QHBoxLayout()
#         lang_layout.setSpacing(15)
#
#         lang_label = QLabel("Язык интерфейса")
#         lang_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         lang_layout.addWidget(lang_label)
#
#         lang_layout.addStretch()
#
#         self.lang_combo = QComboBox()
#         self.lang_combo.addItems(["Русский", "English"])
#         self.lang_combo.setCurrentIndex(0)
#         self.lang_combo.setFixedWidth(200)
#         self.lang_combo.setFixedHeight(40)
#         self.lang_combo.setObjectName("settingsCombo")
#         lang_layout.addWidget(self.lang_combo)
#
#         general_layout.addLayout(lang_layout)
#
#         # Уведомления
#         self.notify_checkbox = QCheckBox("Показывать уведомления о завершении операций")
#         self.notify_checkbox.setFont(QFont("Segoe UI", 12))
#         self.notify_checkbox.setChecked(True)
#         self.notify_checkbox.setObjectName("settingsCheckbox")
#         general_layout.addWidget(self.notify_checkbox)
#
#         # Автосохранение
#         self.autosave_checkbox = QCheckBox("Автосохранение настроек при изменении")
#         self.autosave_checkbox.setFont(QFont("Segoe UI", 12))
#         self.autosave_checkbox.setChecked(True)
#         self.autosave_checkbox.setObjectName("settingsCheckbox")
#         general_layout.addWidget(self.autosave_checkbox)
#
#         general_group.layout().addLayout(general_layout)
#         content_layout.addWidget(general_group)
#
#         # Секция 3: Парсинг
#         parsing_group = self.create_settings_group(
#             "Парсинг маркетплейсов",
#             "Настройки поиска товаров на внешних площадках"
#         )
#         parsing_layout = QVBoxLayout()
#         parsing_layout.setSpacing(15)
#
#         # Таймаут между запросами
#         timeout_layout = QHBoxLayout()
#         timeout_layout.setSpacing(15)
#
#         timeout_label = QLabel("Таймаут между запросами (секунды)")
#         timeout_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         timeout_layout.addWidget(timeout_label)
#
#         timeout_layout.addStretch()
#
#         self.timeout_spin = QSpinBox()
#         self.timeout_spin.setRange(1, 30)
#         self.timeout_spin.setValue(5)
#         self.timeout_spin.setFixedWidth(100)
#         self.timeout_spin.setFixedHeight(40)
#         self.timeout_spin.setObjectName("settingsSpin")
#         timeout_layout.addWidget(self.timeout_spin)
#
#         parsing_layout.addLayout(timeout_layout)
#
#         # Максимум товаров
#         max_items_layout = QHBoxLayout()
#         max_items_layout.setSpacing(15)
#
#         max_items_label = QLabel("Максимум товаров на запрос")
#         max_items_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         max_items_layout.addWidget(max_items_label)
#
#         max_items_layout.addStretch()
#
#         self.max_items_spin = QSpinBox()
#         self.max_items_spin.setRange(5, 100)
#         self.max_items_spin.setValue(20)
#         self.max_items_spin.setFixedWidth(100)
#         self.max_items_spin.setFixedHeight(40)
#         self.max_items_spin.setObjectName("settingsSpin")
#         max_items_layout.addWidget(self.max_items_spin)
#
#         parsing_layout.addLayout(max_items_layout)
#
#         # Использовать прокси
#         self.proxy_checkbox = QCheckBox("Использовать прокси-сервер для парсинга")
#         self.proxy_checkbox.setFont(QFont("Segoe UI", 12))
#         self.proxy_checkbox.setChecked(False)
#         self.proxy_checkbox.setObjectName("settingsCheckbox")
#         parsing_layout.addWidget(self.proxy_checkbox)
#
#         parsing_group.layout().addLayout(parsing_layout)
#         content_layout.addWidget(parsing_group)
#
#         # Секция 4: База данных
#         database_group = self.create_settings_group(
#             "База данных",
#             "Управление локальной базой данных приложения"
#         )
#         database_layout = QVBoxLayout()
#         database_layout.setSpacing(15)
#
#         # Путь к базе данных
#         db_path_layout = QHBoxLayout()
#         db_path_layout.setSpacing(15)
#
#         db_path_label = QLabel("Путь к базе данных")
#         db_path_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         db_path_layout.addWidget(db_path_label)
#
#         db_path_layout.addStretch()
#
#         self.db_path_edit = QLineEdit()
#         self.db_path_edit.setText(str(Path(__file__).parent.parent / "data" / "database.db"))
#         self.db_path_edit.setReadOnly(True)
#         self.db_path_edit.setFixedWidth(400)
#         self.db_path_edit.setFixedHeight(40)
#         self.db_path_edit.setObjectName("settingsInput")
#         db_path_layout.addWidget(self.db_path_edit)
#
#         browse_btn = QPushButton("Обзор")
#         browse_btn.setFixedHeight(40)
#         browse_btn.setFixedWidth(100)
#         browse_btn.setObjectName("secondaryButton")
#         browse_btn.clicked.connect(self.browse_database)
#         db_path_layout.addWidget(browse_btn)
#
#         database_layout.addLayout(db_path_layout)
#
#         # Кнопки действий с БД
#         db_buttons_layout = QHBoxLayout()
#         db_buttons_layout.setSpacing(15)
#
#         clear_cache_btn = QPushButton("Очистить кэш")
#         clear_cache_btn.setFixedHeight(40)
#         clear_cache_btn.setObjectName("secondaryButton")
#         clear_cache_btn.clicked.connect(self.clear_cache)
#
#         reset_db_btn = QPushButton("Сбросить базу данных")
#         reset_db_btn.setFixedHeight(40)
#         reset_db_btn.setObjectName("dangerButton")
#         reset_db_btn.clicked.connect(self.reset_database)
#
#         db_buttons_layout.addWidget(clear_cache_btn)
#         db_buttons_layout.addWidget(reset_db_btn)
#         db_buttons_layout.addStretch()
#
#         database_layout.addLayout(db_buttons_layout)
#
#         database_group.layout().addLayout(database_layout)
#         content_layout.addWidget(database_group)
#
#         content_layout.addStretch()
#
#         # Кнопки сохранения
#         save_buttons_layout = QHBoxLayout()
#         save_buttons_layout.setSpacing(15)
#
#         reset_btn = QPushButton("Сбросить по умолчанию")
#         reset_btn.setFont(QFont("Segoe UI", 12))
#         reset_btn.setFixedSize(200, 45)
#         reset_btn.setObjectName("secondaryButton")
#         reset_btn.clicked.connect(self.reset_to_default)
#
#         save_btn = QPushButton("Сохранить настройки")
#         save_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         save_btn.setFixedSize(200, 45)
#         save_btn.setObjectName("saveButton")
#         save_btn.clicked.connect(self.save_current_settings)
#
#         save_buttons_layout.addStretch()
#         save_buttons_layout.addWidget(reset_btn)
#         save_buttons_layout.addWidget(save_btn)
#
#         content_layout.addLayout(save_buttons_layout)
#
#         # Мини-карточка выхода в правом нижнем углу
#         exit_layout = QHBoxLayout()
#         exit_layout.addStretch()
#
#         exit_card = self.create_exit_card()
#         exit_card.mousePressEvent = lambda event: self.show_exit_confirmation()
#
#         exit_layout.addWidget(exit_card)
#
#         content_layout.addLayout(exit_layout)
#
#         scroll_area.setWidget(scroll_widget)
#         main_layout.addWidget(scroll_area)
#
#         self.setLayout(main_layout)
#
#     def create_settings_group(self, title, description):
#         """Создание группы настроек (карточки)"""
#         group = QFrame()
#         group.setObjectName("settingsGroup")
#
#         layout = QVBoxLayout(group)
#         layout.setContentsMargins(30, 25, 30, 25)
#         layout.setSpacing(15)
#
#         # Заголовок группы
#         title_label = QLabel(title)
#         title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
#         title_label.setObjectName("groupTitle")
#
#         # Описание
#         desc_label = QLabel(description)
#         desc_label.setFont(QFont("Segoe UI", 11))
#         desc_label.setObjectName("groupDescription")
#
#         layout.addWidget(title_label)
#         layout.addWidget(desc_label)
#
#         # Разделитель
#         separator = QFrame()
#         separator.setFrameShape(QFrame.Shape.HLine)
#         separator.setObjectName("groupSeparator")
#         separator.setFixedHeight(1)
#         layout.addWidget(separator)
#
#         return group
#
#     def on_theme_change(self, theme):
#         """Обработчик смены темы"""
#         if self.light_radio.isChecked():
#             self.current_theme = "light"
#         elif self.dark_radio.isChecked():
#             self.current_theme = "dark"
#         elif self.system_radio.isChecked():
#             self.current_theme = "system"
#
#         self.apply_theme(self.current_theme)
#
#     def apply_theme(self, theme):
#         """Применение выбранной темы"""
#         if theme == "dark":
#             self.apply_dark_theme()
#         else:
#             self.apply_light_theme()
#
#     def apply_light_theme(self):
#         """Светлая тема"""
#         self.setStyleSheet(self.get_light_styles())
#
#     def apply_dark_theme(self):
#         """Темная тема"""
#         self.setStyleSheet(self.get_dark_styles())
#
#     def get_light_styles(self):
#         """Стили светлой темы"""
#         return """
#             QWidget#scrollArea {
#                 background-color: #F9FAFB;
#             }
#
#             QLabel {
#                 selection-background-color: transparent;
#                 selection-color: transparent;
#                 background-color: transparent;
#                 color: #1F2937;
#             }
#
#             #mainTitle {
#                 color: #1F2937;
#             }
#
#             #subtitle {
#                 color: #6B7280;
#             }
#
#             QToolTip {
#                 background-color: #F9FAFB;
#                 color: #334155;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 8px;
#                 padding: 10px 14px;
#                 font-size: 12px;
#                 font-family: 'Segoe UI';
#             }
#
#             QPushButton {
#                 selection-background-color: transparent;
#                 selection-color: transparent;
#                 outline: none;
#             }
#
#             #sidebar {
#                 background-color: #FFFFFF;
#                 border-right: 1px solid #E5E7EB;
#             }
#
#             #logoFrame {
#                 background-color: #FFFFFF;
#                 border-bottom: 1px solid #E5E7EB;
#             }
#
#             #menuFrame {
#                 background-color: #FFFFFF;
#             }
#
#             QPushButton#menuButton {
#                 background-color: transparent;
#                 border: none;
#                 color: #4B5563;
#                 border-radius: 10px;
#                 text-align: left;
#             }
#
#             QPushButton#menuButton:hover {
#                 background-color: #F3F4F6;
#                 color: #3B82F6;
#             }
#
#             QPushButton#activeMenu {
#                 background-color: #EFF6FF;
#                 border: none;
#                 color: #3B82F6;
#                 border-radius: 10px;
#                 text-align: left;
#                 border-left: 4px solid #3B82F6;
#                 font-weight: bold;
#             }
#
#             #settingsGroup {
#                 background-color: #FFFFFF;
#                 border: 1px solid #E5E7EB;
#                 border-radius: 12px;
#             }
#
#             #groupTitle {
#                 color: #1F2937;
#             }
#
#             #groupDescription {
#                 color: #6B7280;
#             }
#
#             #groupSeparator {
#                 background-color: #E5E7EB;
#             }
#
#             QRadioButton#themeRadio {
#                 color: #374151;
#                 spacing: 8px;
#             }
#
#             QRadioButton#themeRadio::indicator {
#                 width: 20px;
#                 height: 20px;
#                 border-radius: 10px;
#                 border: 2px solid #D1D5DB;
#                 background-color: #FFFFFF;
#             }
#
#             QRadioButton#themeRadio::indicator:checked {
#                 border: 2px solid #3B82F6;
#                 background-color: #3B82F6;
#             }
#
#             QCheckBox#settingsCheckbox {
#                 color: #374151;
#                 spacing: 8px;
#             }
#
#             QCheckBox#settingsCheckbox::indicator {
#                 width: 20px;
#                 height: 20px;
#                 border-radius: 4px;
#                 border: 2px solid #D1D5DB;
#                 background-color: #FFFFFF;
#             }
#
#             QCheckBox#settingsCheckbox::indicator:checked {
#                 background-color: #3B82F6;
#                 border: 2px solid #3B82F6;
#             }
#
#             QComboBox#settingsCombo {
#                 background-color: #FFFFFF;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 8px;
#                 padding: 5px 10px;
#                 color: #1F2937;
#             }
#
#             QComboBox#settingsCombo:focus {
#                 border: 2px solid #3B82F6;
#             }
#
#             QComboBox#settingsCombo::drop-down {
#                 border: none;
#                 width: 30px;
#             }
#
#             QSpinBox#settingsSpin {
#                 background-color: #FFFFFF;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 8px;
#                 padding: 5px 10px;
#                 color: #1F2937;
#             }
#
#             QSpinBox#settingsSpin:focus {
#                 border: 2px solid #3B82F6;
#             }
#
#             QLineEdit#settingsInput {
#                 background-color: #F9FAFB;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 8px;
#                 padding: 5px 10px;
#                 color: #1F2937;
#             }
#
#             QPushButton#saveButton {
#                 background-color: #3B82F6;
#                 color: white;
#                 border: none;
#                 border-radius: 8px;
#             }
#
#             QPushButton#saveButton:hover {
#                 background-color: #2563EB;
#             }
#
#             QPushButton#secondaryButton {
#                 background-color: #FFFFFF;
#                 color: #374151;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 8px;
#             }
#
#             QPushButton#secondaryButton:hover {
#                 background-color: #F3F4F6;
#             }
#
#             QPushButton#dangerButton {
#                 background-color: #FFFFFF;
#                 color: #EF4444;
#                 border: 1px solid #FECACA;
#                 border-radius: 8px;
#             }
#
#             QPushButton#dangerButton:hover {
#                 background-color: #FEE2E2;
#             }
#
#             #exitCard {
#                 background-color: #FFFFFF;
#                 border: 1px solid #E5E7EB;
#                 border-radius: 10px;
#             }
#
#             #exitCard:hover {
#                 border: 2px solid #EF4444;
#             }
#         """
#
#     def get_dark_styles(self):
#         """Стили темной темы"""
#         return """
#             QWidget#scrollArea {
#                 background-color: #111827;
#             }
#
#             QLabel {
#                 selection-background-color: transparent;
#                 selection-color: transparent;
#                 background-color: transparent;
#                 color: #F3F4F6;
#             }
#
#             #mainTitle {
#                 color: #F9FAFB;
#             }
#
#             #subtitle {
#                 color: #9CA3AF;
#             }
#
#             QToolTip {
#                 background-color: #1F2937;
#                 color: #F3F4F6;
#                 border: 1px solid #374151;
#                 border-radius: 8px;
#                 padding: 10px 14px;
#                 font-size: 12px;
#                 font-family: 'Segoe UI';
#             }
#
#             QPushButton {
#                 selection-background-color: transparent;
#                 selection-color: transparent;
#                 outline: none;
#             }
#
#             #sidebar {
#                 background-color: #1F2937;
#                 border-right: 1px solid #374151;
#             }
#
#             #logoFrame {
#                 background-color: #1F2937;
#                 border-bottom: 1px solid #374151;
#             }
#
#             #menuFrame {
#                 background-color: #1F2937;
#             }
#
#             QPushButton#menuButton {
#                 background-color: transparent;
#                 border: none;
#                 color: #D1D5DB;
#                 border-radius: 10px;
#                 text-align: left;
#             }
#
#             QPushButton#menuButton:hover {
#                 background-color: #374151;
#                 color: #60A5FA;
#             }
#
#             QPushButton#activeMenu {
#                 background-color: #1E3A8A;
#                 border: none;
#                 color: #60A5FA;
#                 border-radius: 10px;
#                 text-align: left;
#                 border-left: 4px solid #3B82F6;
#                 font-weight: bold;
#             }
#
#             #settingsGroup {
#                 background-color: #1F2937;
#                 border: 1px solid #374151;
#                 border-radius: 12px;
#             }
#
#             #groupTitle {
#                 color: #F9FAFB;
#             }
#
#             #groupDescription {
#                 color: #9CA3AF;
#             }
#
#             #groupSeparator {
#                 background-color: #374151;
#             }
#
#             QRadioButton#themeRadio {
#                 color: #D1D5DB;
#                 spacing: 8px;
#             }
#
#             QRadioButton#themeRadio::indicator {
#                 width: 20px;
#                 height: 20px;
#                 border-radius: 10px;
#                 border: 2px solid #4B5563;
#                 background-color: #111827;
#             }
#
#             QRadioButton#themeRadio::indicator:checked {
#                 border: 2px solid #3B82F6;
#                 background-color: #3B82F6;
#             }
#
#             QCheckBox#settingsCheckbox {
#                 color: #D1D5DB;
#                 spacing: 8px;
#             }
#
#             QCheckBox#settingsCheckbox::indicator {
#                 width: 20px;
#                 height: 20px;
#                 border-radius: 4px;
#                 border: 2px solid #4B5563;
#                 background-color: #111827;
#             }
#
#             QCheckBox#settingsCheckbox::indicator:checked {
#                 background-color: #3B82F6;
#                 border: 2px solid #3B82F6;
#             }
#
#             QComboBox#settingsCombo {
#                 background-color: #111827;
#                 border: 1px solid #374151;
#                 border-radius: 8px;
#                 padding: 5px 10px;
#                 color: #F3F4F6;
#             }
#
#             QComboBox#settingsCombo:focus {
#                 border: 2px solid #3B82F6;
#             }
#
#             QComboBox#settingsCombo::drop-down {
#                 border: none;
#                 width: 30px;
#             }
#
#             QSpinBox#settingsSpin {
#                 background-color: #111827;
#                 border: 1px solid #374151;
#                 border-radius: 8px;
#                 padding: 5px 10px;
#                 color: #F3F4F6;
#             }
#
#             QSpinBox#settingsSpin:focus {
#                 border: 2px solid #3B82F6;
#             }
#
#             QLineEdit#settingsInput {
#                 background-color: #111827;
#                 border: 1px solid #374151;
#                 border-radius: 8px;
#                 padding: 5px 10px;
#                 color: #F3F4F6;
#             }
#
#             QPushButton#saveButton {
#                 background-color: #3B82F6;
#                 color: white;
#                 border: none;
#                 border-radius: 8px;
#             }
#
#             QPushButton#saveButton:hover {
#                 background-color: #2563EB;
#             }
#
#             QPushButton#secondaryButton {
#                 background-color: #374151;
#                 color: #F3F4F6;
#                 border: 1px solid #4B5563;
#                 border-radius: 8px;
#             }
#
#             QPushButton#secondaryButton:hover {
#                 background-color: #4B5563;
#             }
#
#             QPushButton#dangerButton {
#                 background-color: #374151;
#                 color: #FCA5A5;
#                 border: 1px solid #7F1D1D;
#                 border-radius: 8px;
#             }
#
#             QPushButton#dangerButton:hover {
#                 background-color: #7F1D1D;
#             }
#
#             #exitCard {
#                 background-color: #1F2937;
#                 border: 1px solid #374151;
#                 border-radius: 10px;
#             }
#
#             #exitCard:hover {
#                 border: 2px solid #EF4444;
#             }
#         """
#
#     def create_exit_card(self):
#         """Создание мини-карточки выхода"""
#         card = QFrame()
#         card.setObjectName("exitCard")
#         card.setFixedSize(180, 70)
#         card.setCursor(Qt.CursorShape.PointingHandCursor)
#
#         layout = QHBoxLayout(card)
#         layout.setContentsMargins(15, 10, 15, 10)
#         layout.setSpacing(12)
#
#         # Иконка с розовым фоном
#         icon_container = QFrame()
#         icon_container.setFixedSize(45, 45)
#         icon_container.setStyleSheet("background-color: #FEE2E2; border-radius: 8px;")
#
#         icon_layout = QVBoxLayout(icon_container)
#         icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#
#         icon_label = self.create_icon_label("door.png", size=25)
#         icon_layout.addWidget(icon_label)
#
#         # Только текст "Выход"
#         title_label = QLabel("Выход")
#         title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         title_label.setStyleSheet("color: #1F2937;")
#
#         layout.addWidget(icon_container)
#         layout.addWidget(title_label)
#         layout.addStretch()
#
#         # Стрелка
#         arrow = QLabel("→")
#         arrow.setFont(QFont("Segoe UI", 16))
#         arrow.setStyleSheet("color: #9CA3AF;")
#         layout.addWidget(arrow)
#
#         return card
#
#     def create_icon_label(self, filename, size=24):
#         """Создание QLabel с иконкой"""
#         label = QLabel()
#         icon_path = self.icons_path / filename
#
#         if icon_path.exists():
#             pixmap = QPixmap(str(icon_path))
#             scaled_pixmap = pixmap.scaled(size, size,
#                                           Qt.AspectRatioMode.KeepAspectRatio,
#                                           Qt.TransformationMode.SmoothTransformation)
#             label.setPixmap(scaled_pixmap)
#         else:
#             print(f"⚠️ Иконка не найдена: {icon_path}")
#
#         label.setFixedSize(size, size)
#         return label
#
#     def browse_database(self):
#         """Выбор пути к базе данных"""
#         print("Открытие диалога выбора файла БД")
#
#     def clear_cache(self):
#         """Очистка кэша"""
#         print("Кэш очищен")
#
#     def reset_database(self):
#         """Сброс базы данных"""
#         print("База данных сброшена")
#
#     def reset_to_default(self):
#         """Сброс настроек к значениям по умолчанию"""
#         self.light_radio.setChecked(True)
#         self.current_theme = "light"
#         self.font_size_combo.setCurrentIndex(1)
#         self.lang_combo.setCurrentIndex(0)
#         self.notify_checkbox.setChecked(True)
#         self.autosave_checkbox.setChecked(True)
#         self.timeout_spin.setValue(5)
#         self.max_items_spin.setValue(20)
#         self.proxy_checkbox.setChecked(False)
#         self.apply_theme("light")
#         print("Настройки сброшены по умолчанию")
#
#     def save_current_settings(self):
#         """Сохранение текущих настроек"""
#         self.save_settings()
#         print(f"Настройки сохранены. Тема: {self.current_theme}")
#
#     def show_exit_confirmation(self):
#         """Показать окно подтверждения выхода"""
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Выход из приложения")
#         dialog.setFixedSize(450, 220)
#         dialog.setWindowIcon(self.windowIcon())
#
#         layout = QVBoxLayout(dialog)
#         layout.setContentsMargins(40, 30, 40, 30)
#         layout.setSpacing(15)
#
#         icon_label = self.create_icon_label("warning.png", size=50)
#         layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         title_label = QLabel("Вы точно хотите уйти?")
#         title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
#         title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         title_label.setWordWrap(True)
#         layout.addWidget(title_label)
#
#         subtitle_label = QLabel("Возможно, остались несохраненные дела")
#         subtitle_label.setFont(QFont("Segoe UI", 11))
#         subtitle_label.setStyleSheet("color: #6B7280;")
#         subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(subtitle_label)
#
#         buttons_layout = QHBoxLayout()
#         buttons_layout.setSpacing(15)
#
#         cancel_btn = QPushButton("Отмена")
#         cancel_btn.setFont(QFont("Segoe UI", 12))
#         cancel_btn.setFixedSize(150, 45)
#         cancel_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #F3F4F6;
#                 color: #374151;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 8px;
#             }
#             QPushButton:hover {
#                 background-color: #E5E7EB;
#             }
#         """)
#         cancel_btn.clicked.connect(dialog.reject)
#
#         exit_btn = QPushButton("Выйти")
#         exit_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         exit_btn.setFixedSize(150, 45)
#         exit_btn.setStyleSheet("""
#             QPushButton {
#                 background-color: #EF4444;
#                 color: white;
#                 border: none;
#                 border-radius: 8px;
#             }
#             QPushButton:hover {
#                 background-color: #DC2626;
#             }
#         """)
#         exit_btn.clicked.connect(lambda: self.confirm_exit(dialog))
#
#         buttons_layout.addStretch()
#         buttons_layout.addWidget(cancel_btn)
#         buttons_layout.addWidget(exit_btn)
#         buttons_layout.addStretch()
#
#         layout.addLayout(buttons_layout)
#
#         dialog.exec()
#
#     def confirm_exit(self, dialog):
#         """Подтверждение выхода"""
#         dialog.accept()
#         self.close()
#
#
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     app.setStyle("Fusion")
# #     app.setFont(QFont("Segoe UI", 10))
# #
# #     window = SettingsWindow()
# #     window.show()
# #
# #     sys.exit(app.exec())
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     app.setFont(QFont("Segoe UI", 10))
#
#     from ui.navigation import nav_manager
#
#     sys.exit(app.exec())

import sys
import json
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QSizePolicy, QApplication, QDialog,
                             QRadioButton, QButtonGroup, QCheckBox, QComboBox,
                             QLineEdit, QSpinBox, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon


class SettingsPage(QWidget):
    def __init__(self, icons_path, parent=None):
        super().__init__(parent)

        # Получаем путь к иконкам от родительского окна
        self.icons_path = icons_path

        # Путь к файлу настроек
        self.settings_path = Path(__file__).parent / "settings.json"

        # Текущая тема
        self.current_theme = "light"

        # Загружаем сохраненные настройки
        self.load_settings()

        # Создаем интерфейс
        self.create_widgets()
        self.apply_theme(self.current_theme)

    def load_settings(self):
        """Загрузка настроек из файла"""
        if self.settings_path.exists():
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                self.current_theme = settings.get("theme", "light")
            except Exception:
                self.current_theme = "light"
        else:
            self.current_theme = "light"

    def save_settings(self):
        """Сохранение настроек в файл"""
        settings = {
            "theme": self.current_theme,
        }
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        """Создание элементов интерфейса СТРАНИЦЫ настроек"""
        # Скроллируемая область для контента
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("scrollArea")

        scroll_widget = QWidget()
        content_layout = QVBoxLayout(scroll_widget)
        content_layout.setContentsMargins(50, 40, 50, 40)
        content_layout.setSpacing(25)

        # 1. Заголовок страницы
        title = QLabel("Настройки")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setObjectName("mainTitle")

        subtitle = QLabel("Настройте приложение под свои предпочтения")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setObjectName("subtitle")

        content_layout.addWidget(title)
        content_layout.addWidget(subtitle)
        content_layout.addSpacing(10)

        # 2. Секция: Оформление
        appearance_group = self.create_settings_group(
            "Оформление",
            "Выберите тему и внешний вид приложения"
        )
        appearance_layout = QVBoxLayout()
        appearance_layout.setSpacing(15)

        # Переключатель темы
        theme_label = QLabel("Тема оформления")
        theme_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        appearance_layout.addWidget(theme_label)

        theme_options_layout = QHBoxLayout()
        theme_options_layout.setSpacing(15)

        self.theme_group = QButtonGroup()

        self.light_radio = QRadioButton("☀️ Светлая")
        self.light_radio.setFont(QFont("Segoe UI", 12))
        self.light_radio.setObjectName("themeRadio")
        self.light_radio.setChecked(self.current_theme == "light")
        self.light_radio.toggled.connect(lambda: self.on_theme_change("light"))

        self.dark_radio = QRadioButton("🌙 Темная")
        self.dark_radio.setFont(QFont("Segoe UI", 12))
        self.dark_radio.setObjectName("themeRadio")
        self.dark_radio.setChecked(self.current_theme == "dark")
        self.dark_radio.toggled.connect(lambda: self.on_theme_change("dark"))

        self.system_radio = QRadioButton("💻 Системная")
        self.system_radio.setFont(QFont("Segoe UI", 12))
        self.system_radio.setObjectName("themeRadio")
        self.system_radio.setChecked(self.current_theme == "system")
        self.system_radio.toggled.connect(lambda: self.on_theme_change("system"))

        self.theme_group.addButton(self.light_radio)
        self.theme_group.addButton(self.dark_radio)
        self.theme_group.addButton(self.system_radio)

        theme_options_layout.addWidget(self.light_radio)
        theme_options_layout.addWidget(self.dark_radio)
        theme_options_layout.addWidget(self.system_radio)
        theme_options_layout.addStretch()

        appearance_layout.addLayout(theme_options_layout)

        # Размер шрифта
        font_size_layout = QHBoxLayout()
        font_size_layout.setSpacing(15)

        font_size_label = QLabel("Размер шрифта интерфейса")
        font_size_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        font_size_layout.addWidget(font_size_label)

        font_size_layout.addStretch()

        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["Маленький (10)", "Обычный (12)", "Крупный (14)", "Очень крупный (16)"])
        self.font_size_combo.setCurrentIndex(1)
        self.font_size_combo.setFixedWidth(200)
        self.font_size_combo.setFixedHeight(40)
        self.font_size_combo.setObjectName("settingsCombo")
        font_size_layout.addWidget(self.font_size_combo)

        appearance_layout.addLayout(font_size_layout)

        appearance_group.layout().addLayout(appearance_layout)
        content_layout.addWidget(appearance_group)

        # 3. Секция: Общие настройки
        general_group = self.create_settings_group(
            "Общие",
            "Основные параметры работы приложения"
        )
        general_layout = QVBoxLayout()
        general_layout.setSpacing(15)

        # Язык интерфейса
        lang_layout = QHBoxLayout()
        lang_layout.setSpacing(15)

        lang_label = QLabel("Язык интерфейса")
        lang_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lang_layout.addWidget(lang_label)

        lang_layout.addStretch()

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Русский", "English"])
        self.lang_combo.setCurrentIndex(0)
        self.lang_combo.setFixedWidth(200)
        self.lang_combo.setFixedHeight(40)
        self.lang_combo.setObjectName("settingsCombo")
        lang_layout.addWidget(self.lang_combo)

        general_layout.addLayout(lang_layout)

        # Уведомления
        self.notify_checkbox = QCheckBox("Показывать уведомления о завершении операций")
        self.notify_checkbox.setFont(QFont("Segoe UI", 12))
        self.notify_checkbox.setChecked(True)
        self.notify_checkbox.setObjectName("settingsCheckbox")
        general_layout.addWidget(self.notify_checkbox)

        # Автосохранение
        self.autosave_checkbox = QCheckBox("Автосохранение настроек при изменении")
        self.autosave_checkbox.setFont(QFont("Segoe UI", 12))
        self.autosave_checkbox.setChecked(True)
        self.autosave_checkbox.setObjectName("settingsCheckbox")
        general_layout.addWidget(self.autosave_checkbox)

        general_group.layout().addLayout(general_layout)
        content_layout.addWidget(general_group)

        # 4. Секция: Парсинг маркетплейсов
        parsing_group = self.create_settings_group(
            "Парсинг маркетплейсов",
            "Настройки поиска товаров на внешних площадках"
        )
        parsing_layout = QVBoxLayout()
        parsing_layout.setSpacing(15)

        # Таймаут между запросами
        timeout_layout = QHBoxLayout()
        timeout_layout.setSpacing(15)

        timeout_label = QLabel("Таймаут между запросами (секунды)")
        timeout_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        timeout_layout.addWidget(timeout_label)

        timeout_layout.addStretch()

        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 30)
        self.timeout_spin.setValue(5)
        self.timeout_spin.setFixedWidth(100)
        self.timeout_spin.setFixedHeight(40)
        self.timeout_spin.setObjectName("settingsSpin")
        timeout_layout.addWidget(self.timeout_spin)

        parsing_layout.addLayout(timeout_layout)

        # Максимум товаров
        max_items_layout = QHBoxLayout()
        max_items_layout.setSpacing(15)

        max_items_label = QLabel("Максимум товаров на запрос")
        max_items_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        max_items_layout.addWidget(max_items_label)

        max_items_layout.addStretch()

        self.max_items_spin = QSpinBox()
        self.max_items_spin.setRange(5, 100)
        self.max_items_spin.setValue(20)
        self.max_items_spin.setFixedWidth(100)
        self.max_items_spin.setFixedHeight(40)
        self.max_items_spin.setObjectName("settingsSpin")
        max_items_layout.addWidget(self.max_items_spin)

        parsing_layout.addLayout(max_items_layout)

        # Использовать прокси
        self.proxy_checkbox = QCheckBox("Использовать прокси-сервер для парсинга")
        self.proxy_checkbox.setFont(QFont("Segoe UI", 12))
        self.proxy_checkbox.setChecked(False)
        self.proxy_checkbox.setObjectName("settingsCheckbox")
        parsing_layout.addWidget(self.proxy_checkbox)

        parsing_group.layout().addLayout(parsing_layout)
        content_layout.addWidget(parsing_group)

        # 5. Секция: База данных
        database_group = self.create_settings_group(
            "База данных",
            "Управление локальной базой данных приложения"
        )
        database_layout = QVBoxLayout()
        database_layout.setSpacing(15)

        # Путь к базе данных
        db_path_layout = QHBoxLayout()
        db_path_layout.setSpacing(15)

        db_path_label = QLabel("Путь к базе данных")
        db_path_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        db_path_layout.addWidget(db_path_label)

        db_path_layout.addStretch()

        self.db_path_edit = QLineEdit()
        self.db_path_edit.setText(str(Path(__file__).parent.parent / "data" / "database.db"))
        self.db_path_edit.setReadOnly(True)
        self.db_path_edit.setFixedWidth(400)
        self.db_path_edit.setFixedHeight(40)
        self.db_path_edit.setObjectName("settingsInput")
        db_path_layout.addWidget(self.db_path_edit)

        browse_btn = QPushButton("Обзор")
        browse_btn.setFixedHeight(40)
        browse_btn.setFixedWidth(100)
        browse_btn.setObjectName("secondaryButton")
        browse_btn.clicked.connect(self.browse_database)
        db_path_layout.addWidget(browse_btn)

        database_layout.addLayout(db_path_layout)

        # Кнопки действий с БД
        db_buttons_layout = QHBoxLayout()
        db_buttons_layout.setSpacing(15)

        clear_cache_btn = QPushButton("🗑️ Очистить кэш")
        clear_cache_btn.setFixedHeight(40)
        clear_cache_btn.setObjectName("secondaryButton")
        clear_cache_btn.clicked.connect(self.clear_cache)

        reset_db_btn = QPushButton("🔄 Сбросить базу данных")
        reset_db_btn.setFixedHeight(40)
        reset_db_btn.setObjectName("dangerButton")
        reset_db_btn.clicked.connect(self.reset_database)

        db_buttons_layout.addWidget(clear_cache_btn)
        db_buttons_layout.addWidget(reset_db_btn)
        db_buttons_layout.addStretch()

        database_layout.addLayout(db_buttons_layout)

        database_group.layout().addLayout(database_layout)
        content_layout.addWidget(database_group)

        content_layout.addStretch()

        # 6. Кнопки сохранения
        save_buttons_layout = QHBoxLayout()
        save_buttons_layout.setSpacing(15)

        reset_btn = QPushButton("Сбросить по умолчанию")
        reset_btn.setFont(QFont("Segoe UI", 12))
        reset_btn.setFixedSize(200, 45)
        reset_btn.setObjectName("secondaryButton")
        reset_btn.clicked.connect(self.reset_to_default)

        save_btn = QPushButton("Сохранить настройки")
        save_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        save_btn.setFixedSize(200, 45)
        save_btn.setObjectName("saveButton")
        save_btn.clicked.connect(self.save_current_settings)

        save_buttons_layout.addStretch()
        save_buttons_layout.addWidget(reset_btn)
        save_buttons_layout.addWidget(save_btn)

        content_layout.addLayout(save_buttons_layout)

        # 7. Мини-карточка выхода в правом нижнем углу
        exit_layout = QHBoxLayout()
        exit_layout.addStretch()

        exit_card = self.create_exit_card()
        exit_layout.addWidget(exit_card)

        content_layout.addLayout(exit_layout)

        scroll_area.setWidget(scroll_widget)

        # Основной layout страницы
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)

    def create_settings_group(self, title, description):
        """Создание группы настроек (карточки)"""
        group = QFrame()
        group.setObjectName("settingsGroup")

        layout = QVBoxLayout(group)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        # Заголовок группы
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setObjectName("groupTitle")

        # Описание
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 11))
        desc_label.setObjectName("groupDescription")

        layout.addWidget(title_label)
        layout.addWidget(desc_label)

        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("groupSeparator")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        return group

    def on_theme_change(self, theme):
        """Обработчик смены темы"""
        if self.light_radio.isChecked():
            self.current_theme = "light"
        elif self.dark_radio.isChecked():
            self.current_theme = "dark"
        elif self.system_radio.isChecked():
            self.current_theme = "system"

        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        """Применение выбранной темы"""
        if theme == "dark":
            self.setStyleSheet(self.get_dark_styles())
        else:
            self.setStyleSheet(self.get_light_styles())

    def get_light_styles(self):
        """Стили светлой темы"""
        return """
            QWidget#scrollArea {
                background-color: #F9FAFB;
            }

            QLabel {
                selection-background-color: transparent;
                selection-color: transparent;
                background-color: transparent;
                color: #1F2937;
            }

            #mainTitle {
                color: #1F2937;
            }

            #subtitle {
                color: #6B7280;
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

            #settingsGroup {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }

            #groupTitle {
                color: #1F2937;
            }

            #groupDescription {
                color: #6B7280;
            }

            #groupSeparator {
                background-color: #E5E7EB;
            }

            QRadioButton#themeRadio {
                color: #374151;
                spacing: 8px;
            }

            QRadioButton#themeRadio::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #D1D5DB;
                background-color: #FFFFFF;
            }

            QRadioButton#themeRadio::indicator:checked {
                border: 2px solid #3B82F6;
                background-color: #3B82F6;
            }

            QCheckBox#settingsCheckbox {
                color: #374151;
                spacing: 8px;
            }

            QCheckBox#settingsCheckbox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #D1D5DB;
                background-color: #FFFFFF;
            }

            QCheckBox#settingsCheckbox::indicator:checked {
                background-color: #3B82F6;
                border: 2px solid #3B82F6;
            }

            QComboBox#settingsCombo {
                background-color: #FFFFFF;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 5px 10px;
                color: #1F2937;
            }

            QComboBox#settingsCombo:focus {
                border: 2px solid #3B82F6;
            }

            QComboBox#settingsCombo::drop-down {
                border: none;
                width: 30px;
            }

            QSpinBox#settingsSpin {
                background-color: #FFFFFF;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 5px 10px;
                color: #1F2937;
            }

            QSpinBox#settingsSpin:focus {
                border: 2px solid #3B82F6;
            }

            QLineEdit#settingsInput {
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 5px 10px;
                color: #1F2937;
            }

            QPushButton#saveButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 8px;
            }

            QPushButton#saveButton:hover {
                background-color: #2563EB;
            }

            QPushButton#secondaryButton {
                background-color: #FFFFFF;
                color: #374151;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
            }

            QPushButton#secondaryButton:hover {
                background-color: #F3F4F6;
            }

            QPushButton#dangerButton {
                background-color: #FFFFFF;
                color: #EF4444;
                border: 1px solid #FECACA;
                border-radius: 8px;
            }

            QPushButton#dangerButton:hover {
                background-color: #FEE2E2;
            }

            #exitCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }

            #exitCard:hover {
                border: 2px solid #EF4444;
            }
        """

    def get_dark_styles(self):
        """Стили темной темы"""
        return """
            QWidget#scrollArea {
                background-color: #111827;
            }

            QLabel {
                selection-background-color: transparent;
                selection-color: transparent;
                background-color: transparent;
                color: #F3F4F6;
            }

            #mainTitle {
                color: #F9FAFB;
            }

            #subtitle {
                color: #9CA3AF;
            }

            QToolTip {
                background-color: #1F2937;
                color: #F3F4F6;
                border: 1px solid #374151;
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

            #settingsGroup {
                background-color: #1F2937;
                border: 1px solid #374151;
                border-radius: 12px;
            }

            #groupTitle {
                color: #F9FAFB;
            }

            #groupDescription {
                color: #9CA3AF;
            }

            #groupSeparator {
                background-color: #374151;
            }

            QRadioButton#themeRadio {
                color: #D1D5DB;
                spacing: 8px;
            }

            QRadioButton#themeRadio::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #4B5563;
                background-color: #111827;
            }

            QRadioButton#themeRadio::indicator:checked {
                border: 2px solid #3B82F6;
                background-color: #3B82F6;
            }

            QCheckBox#settingsCheckbox {
                color: #D1D5DB;
                spacing: 8px;
            }

            QCheckBox#settingsCheckbox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #4B5563;
                background-color: #111827;
            }

            QCheckBox#settingsCheckbox::indicator:checked {
                background-color: #3B82F6;
                border: 2px solid #3B82F6;
            }

            QComboBox#settingsCombo {
                background-color: #111827;
                border: 1px solid #374151;
                border-radius: 8px;
                padding: 5px 10px;
                color: #F3F4F6;
            }

            QComboBox#settingsCombo:focus {
                border: 2px solid #3B82F6;
            }

            QComboBox#settingsCombo::drop-down {
                border: none;
                width: 30px;
            }

            QSpinBox#settingsSpin {
                background-color: #111827;
                border: 1px solid #374151;
                border-radius: 8px;
                padding: 5px 10px;
                color: #F3F4F6;
            }

            QSpinBox#settingsSpin:focus {
                border: 2px solid #3B82F6;
            }

            QLineEdit#settingsInput {
                background-color: #111827;
                border: 1px solid #374151;
                border-radius: 8px;
                padding: 5px 10px;
                color: #F3F4F6;
            }

            QPushButton#saveButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 8px;
            }

            QPushButton#saveButton:hover {
                background-color: #2563EB;
            }

            QPushButton#secondaryButton {
                background-color: #374151;
                color: #F3F4F6;
                border: 1px solid #4B5563;
                border-radius: 8px;
            }

            QPushButton#secondaryButton:hover {
                background-color: #4B5563;
            }

            QPushButton#dangerButton {
                background-color: #374151;
                color: #FCA5A5;
                border: 1px solid #7F1D1D;
                border-radius: 8px;
            }

            QPushButton#dangerButton:hover {
                background-color: #7F1D1D;
            }

            #exitCard {
                background-color: #1F2937;
                border: 1px solid #374151;
                border-radius: 10px;
            }

            #exitCard:hover {
                border: 2px solid #EF4444;
            }
        """

    def create_exit_card(self):
        """Создание мини-карточки выхода"""
        card = QFrame()
        card.setObjectName("exitCard")
        card.setFixedSize(180, 70)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(12)

        # Иконка с розовым фоном
        icon_container = QFrame()
        icon_container.setFixedSize(45, 45)
        icon_container.setStyleSheet("background-color: #FEE2E2; border-radius: 8px;")

        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(self.create_icon_label("door.png", size=25))

        # Текст
        title_label = QLabel("Выход")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1F2937;")

        layout.addWidget(icon_container)
        layout.addWidget(title_label)
        layout.addStretch()

        # Стрелка
        arrow = QLabel("→")
        arrow.setFont(QFont("Segoe UI", 16))
        arrow.setStyleSheet("color: #9CA3AF;")
        layout.addWidget(arrow)

        # При клике показываем подтверждение
        card.mousePressEvent = lambda event: self.show_exit_confirmation()

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
            print(f"️ Иконка не найдена: {icon_path}")

        label.setFixedSize(size, size)
        return label

    def navigate_to(self, page_name):
        """Переключение страницы через родительское окно (AppWindow)"""
        parent = self.parent()
        while parent is not None:
            if hasattr(parent, 'switch_page'):
                parent.switch_page(page_name)
                return
            parent = parent.parent()

    def browse_database(self):
        """Выбор пути к базе данных"""
        print("Открытие диалога выбора файла БД")

    def clear_cache(self):
        """Очистка кэша"""
        print("Кэш очищен")

    def reset_database(self):
        """Сброс базы данных"""
        print("База данных сброшена")

    def reset_to_default(self):
        """Сброс настроек к значениям по умолчанию"""
        self.light_radio.setChecked(True)
        self.current_theme = "light"
        self.font_size_combo.setCurrentIndex(1)
        self.lang_combo.setCurrentIndex(0)
        self.notify_checkbox.setChecked(True)
        self.autosave_checkbox.setChecked(True)
        self.timeout_spin.setValue(5)
        self.max_items_spin.setValue(20)
        self.proxy_checkbox.setChecked(False)
        self.apply_theme("light")
        print("Настройки сброшены по умолчанию")

    def save_current_settings(self):
        """Сохранение текущих настроек"""
        self.save_settings()
        print(f"Настройки сохранены. Тема: {self.current_theme}")

    def show_exit_confirmation(self):
        """Показать окно подтверждения выхода"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Выход из приложения")
        dialog.setFixedSize(450, 220)

        # Пытаемся взять иконку у главного окна
        parent = self.parent()
        while parent is not None:
            if hasattr(parent, 'windowIcon'):
                dialog.setWindowIcon(parent.windowIcon())
                break
            parent = parent.parent()

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

        subtitle_label = QLabel("Возможно, остались несохраненные дела")
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
        """Подтверждение выхода — закрытие всего приложения"""
        dialog.accept()
        QApplication.instance().quit()


# Блок для автономного тестирования этой страницы
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    # Для теста создаем временное окно, чтобы показать страницу
    from PyQt6.QtWidgets import QMainWindow

    window = QMainWindow()
    window.setWindowTitle("Тест: Настройки")
    window.setGeometry(100, 100, 1400, 900)

    icons_path = Path(__file__).parent / "icons"
    page = SettingsPage(icons_path)
    window.setCentralWidget(page)

    window.show()
    sys.exit(app.exec())