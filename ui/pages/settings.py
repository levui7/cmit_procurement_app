"""
Страница настроек приложения
"""
import json
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QRadioButton, QButtonGroup, QCheckBox, QComboBox,
                             QLineEdit, QSpinBox, QScrollArea, QDoubleSpinBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.utils.config import Colors, Fonts, Spacing, Sizes, DATA_DIR
from ui.utils.styles import get_settings_styles
from backend.crud.crud_settings import get_app_setting, set_app_setting

from backend.database import get_session

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Сохраняем настройки в папке data для лучшей архитектуры
        self.settings_path = DATA_DIR / "settings.json"
        self.current_theme = "light"

        self.load_settings()
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
        settings = {"theme": self.current_theme}
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        """Создание контента страницы настроек"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Скроллируемая область для контента
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("scrollArea")

        scroll_widget = QWidget()
        content_layout = QVBoxLayout(scroll_widget)
        content_layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
        content_layout.setSpacing(Spacing.LG)

        # Заголовок страницы
        title = QLabel("Настройки")
        title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_DISPLAY, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")

        subtitle = QLabel("Настройте приложение под свои предпочтения")
        subtitle.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")

        content_layout.addWidget(title)
        content_layout.addWidget(subtitle)
        content_layout.addSpacing(Spacing.SM)

        # --- Секция 1: Оформление ---
        appearance_group = self.create_settings_group(
            "Оформление",
            "Выберите тему и внешний вид приложения"
        )
        appearance_layout = QVBoxLayout()
        appearance_layout.setSpacing(Spacing.SM)

        theme_label = QLabel("Тема оформления")
        theme_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        appearance_layout.addWidget(theme_label)

        theme_options_layout = QHBoxLayout()
        theme_options_layout.setSpacing(Spacing.SM)

        self.theme_group = QButtonGroup()

        self.light_radio = QRadioButton("Светлая")
        self.light_radio.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        self.light_radio.setObjectName("themeRadio")
        self.light_radio.setChecked(self.current_theme == "light")
        self.light_radio.toggled.connect(lambda: self.on_theme_change("light"))

        self.dark_radio = QRadioButton("Темная")
        self.dark_radio.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        self.dark_radio.setObjectName("themeRadio")
        self.dark_radio.setChecked(self.current_theme == "dark")
        self.dark_radio.toggled.connect(lambda: self.on_theme_change("dark"))

        self.system_radio = QRadioButton("Системная")
        self.system_radio.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
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
        font_size_layout.setSpacing(Spacing.SM)

        font_size_label = QLabel("Размер шрифта интерфейса")
        font_size_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        font_size_layout.addWidget(font_size_label)
        font_size_layout.addStretch()

        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["Маленький (10)", "Обычный (12)", "Крупный (14)", "Очень крупный (16)"])
        self.font_size_combo.setCurrentIndex(1)
        self.font_size_combo.setFixedWidth(200)
        self.font_size_combo.setFixedHeight(Sizes.INPUT_HEIGHT)
        self.font_size_combo.setObjectName("settingsCombo")
        font_size_layout.addWidget(self.font_size_combo)
        appearance_layout.addLayout(font_size_layout)

        appearance_group.layout().addLayout(appearance_layout)
        content_layout.addWidget(appearance_group)

        # --- Секция: Параметры товаров ---
        products_group = self.create_settings_group(
            "Параметры товаров",
            "Глобальные настройки для всех товаров"
        )
        products_layout = QVBoxLayout()
        products_layout.setSpacing(Spacing.SM)

        damage_layout = QHBoxLayout()
        damage_layout.setSpacing(Spacing.SM)

        damage_label = QLabel("Процент поломки/амортизации")
        damage_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        damage_layout.addWidget(damage_label)
        damage_layout.addStretch()

        self.damage_spin = QDoubleSpinBox()
        self.damage_spin.setRange(0.0, 100.0)

        # Получаем значение из БД или 2.5 по умолчанию
        db = get_session()
        try:
            default_damage = float(get_app_setting(db, "default_damage_percent", "2.5"))
        finally:
            db.close()

        self.damage_spin.setValue(default_damage)
        self.damage_spin.setSuffix("%")
        self.damage_spin.setFixedWidth(100)
        self.damage_spin.setFixedHeight(Sizes.INPUT_HEIGHT)
        self.damage_spin.setObjectName("settingsSpin")
        damage_layout.addWidget(self.damage_spin)

        products_layout.addLayout(damage_layout)
        products_group.layout().addLayout(products_layout)
        content_layout.addWidget(products_group)

        # --- Секция 2: Общие настройки ---
        general_group = self.create_settings_group(
            "Общие",
            "Основные параметры работы приложения"
        )
        general_layout = QVBoxLayout()
        general_layout.setSpacing(Spacing.SM)

        lang_layout = QHBoxLayout()
        lang_layout.setSpacing(Spacing.SM)

        lang_label = QLabel("Язык интерфейса")
        lang_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        lang_layout.addWidget(lang_label)
        lang_layout.addStretch()

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Русский", "English"])
        self.lang_combo.setCurrentIndex(0)
        self.lang_combo.setFixedWidth(200)
        self.lang_combo.setFixedHeight(Sizes.INPUT_HEIGHT)
        self.lang_combo.setObjectName("settingsCombo")
        lang_layout.addWidget(self.lang_combo)
        general_layout.addLayout(lang_layout)

        self.notify_checkbox = QCheckBox("Показывать уведомления о завершении операций")
        self.notify_checkbox.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        self.notify_checkbox.setChecked(True)
        self.notify_checkbox.setObjectName("settingsCheckbox")
        general_layout.addWidget(self.notify_checkbox)

        self.autosave_checkbox = QCheckBox("Автосохранение настроек при изменении")
        self.autosave_checkbox.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        self.autosave_checkbox.setChecked(True)
        self.autosave_checkbox.setObjectName("settingsCheckbox")
        general_layout.addWidget(self.autosave_checkbox)

        general_group.layout().addLayout(general_layout)
        content_layout.addWidget(general_group)

        # --- Секция 3: Парсинг ---
        parsing_group = self.create_settings_group(
            "Парсинг маркетплейсов",
            "Настройки поиска товаров на внешних площадках"
        )
        parsing_layout = QVBoxLayout()
        parsing_layout.setSpacing(Spacing.SM)

        timeout_layout = QHBoxLayout()
        timeout_layout.setSpacing(Spacing.SM)

        timeout_label = QLabel("Таймаут между запросами (секунды)")
        timeout_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        timeout_layout.addWidget(timeout_label)
        timeout_layout.addStretch()

        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 30)
        self.timeout_spin.setValue(5)
        self.timeout_spin.setFixedWidth(100)
        self.timeout_spin.setFixedHeight(Sizes.INPUT_HEIGHT)
        self.timeout_spin.setObjectName("settingsSpin")
        timeout_layout.addWidget(self.timeout_spin)
        parsing_layout.addLayout(timeout_layout)

        max_items_layout = QHBoxLayout()
        max_items_layout.setSpacing(Spacing.SM)

        max_items_label = QLabel("Максимум товаров на запрос")
        max_items_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        max_items_layout.addWidget(max_items_label)
        max_items_layout.addStretch()

        self.max_items_spin = QSpinBox()
        self.max_items_spin.setRange(5, 100)
        self.max_items_spin.setValue(20)
        self.max_items_spin.setFixedWidth(100)
        self.max_items_spin.setFixedHeight(Sizes.INPUT_HEIGHT)
        self.max_items_spin.setObjectName("settingsSpin")
        max_items_layout.addWidget(self.max_items_spin)
        parsing_layout.addLayout(max_items_layout)

        self.proxy_checkbox = QCheckBox("Использовать прокси-сервер для парсинга")
        self.proxy_checkbox.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        self.proxy_checkbox.setChecked(False)
        self.proxy_checkbox.setObjectName("settingsCheckbox")
        parsing_layout.addWidget(self.proxy_checkbox)

        parsing_group.layout().addLayout(parsing_layout)
        content_layout.addWidget(parsing_group)

        # --- Секция 4: База данных ---
        database_group = self.create_settings_group(
            "База данных",
            "Управление локальной базой данных приложения"
        )
        database_layout = QVBoxLayout()
        database_layout.setSpacing(Spacing.SM)

        db_path_layout = QHBoxLayout()
        db_path_layout.setSpacing(Spacing.SM)

        db_path_label = QLabel("Путь к базе данных")
        db_path_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        db_path_layout.addWidget(db_path_label)
        db_path_layout.addStretch()

        from ui.utils.config import DATA_DIR  # Импортируем актуальный путь к БД
        self.db_path_edit = QLineEdit()
        self.db_path_edit.setText(str(DATA_DIR))
        self.db_path_edit.setReadOnly(True)
        self.db_path_edit.setFixedWidth(400)
        self.db_path_edit.setFixedHeight(Sizes.INPUT_HEIGHT)
        self.db_path_edit.setObjectName("settingsInput")
        db_path_layout.addWidget(self.db_path_edit)

        browse_btn = QPushButton("Обзор")
        browse_btn.setFixedHeight(Sizes.INPUT_HEIGHT)
        browse_btn.setFixedWidth(100)
        browse_btn.setObjectName("secondaryButton")
        browse_btn.clicked.connect(self.browse_database)
        db_path_layout.addWidget(browse_btn)
        database_layout.addLayout(db_path_layout)

        db_buttons_layout = QHBoxLayout()
        db_buttons_layout.setSpacing(Spacing.SM)

        clear_cache_btn = QPushButton("Очистить кэш")
        clear_cache_btn.setFixedHeight(Sizes.BUTTON_HEIGHT)
        clear_cache_btn.setObjectName("secondaryButton")
        clear_cache_btn.clicked.connect(self.clear_cache)

        reset_db_btn = QPushButton("Сбросить базу данных")
        reset_db_btn.setFixedHeight(Sizes.BUTTON_HEIGHT)
        reset_db_btn.setObjectName("dangerButton")
        reset_db_btn.clicked.connect(self.reset_database)

        db_buttons_layout.addWidget(clear_cache_btn)
        db_buttons_layout.addWidget(reset_db_btn)
        db_buttons_layout.addStretch()
        database_layout.addLayout(db_buttons_layout)

        database_group.layout().addLayout(database_layout)
        content_layout.addWidget(database_group)

        content_layout.addStretch()

        # Кнопки сохранения
        save_buttons_layout = QHBoxLayout()
        save_buttons_layout.setSpacing(Spacing.SM)

        reset_btn = QPushButton("Сбросить по умолчанию")
        reset_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        reset_btn.setFixedSize(200, Sizes.BUTTON_HEIGHT)
        reset_btn.setObjectName("secondaryButton")
        reset_btn.clicked.connect(self.reset_to_default)

        save_btn = QPushButton("Сохранить настройки")
        save_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL, QFont.Weight.Bold))
        save_btn.setFixedSize(200, Sizes.BUTTON_HEIGHT)
        save_btn.setObjectName("saveButton")
        save_btn.clicked.connect(self.save_current_settings)

        save_buttons_layout.addStretch()
        save_buttons_layout.addWidget(reset_btn)
        save_buttons_layout.addWidget(save_btn)
        content_layout.addLayout(save_buttons_layout)

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

    def create_settings_group(self, title, description):
        """Создание группы настроек (карточки)"""
        group = QFrame()
        group.setObjectName("settingsGroup")

        layout = QVBoxLayout(group)
        layout.setContentsMargins(Spacing.XL, Spacing.LG, Spacing.XL, Spacing.LG)
        layout.setSpacing(Spacing.SM)

        title_label = QLabel(title)
        title_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        title_label.setObjectName("groupTitle")

        desc_label = QLabel(description)
        desc_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        desc_label.setObjectName("groupDescription")

        layout.addWidget(title_label)
        layout.addWidget(desc_label)

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
        """Применение выбранной темы через централизованные стили"""
        self.setStyleSheet(get_settings_styles(theme))

    def browse_database(self):
        QMessageBox.information(self, "Информация", "Выбор файла БД будет реализован позже")

    def clear_cache(self):
        QMessageBox.information(self, "Информация", "Кэш очищен")

    def reset_database(self):
        reply = QMessageBox.warning(
            self, "Подтверждение",
            "Вы уверены? Это удалит все данные и создаст новую базу.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Информация", "База данных сброшена (требуется перезапуск)")

    def reset_to_default(self):
        """Сброс настроек к значениям по умолчанию"""
        db = get_session()
        try:
            self.light_radio.setChecked(True)
            self.current_theme = "light"
            self.font_size_combo.setCurrentIndex(1)
            self.lang_combo.setCurrentIndex(0)
            self.notify_checkbox.setChecked(True)
            self.autosave_checkbox.setChecked(True)
            self.timeout_spin.setValue(5)
            self.max_items_spin.setValue(20)
            self.proxy_checkbox.setChecked(False)

            # Сброс процента поломки
            default_damage = float(get_app_setting(db, "default_damage_percent", "2.5"))
            self.damage_spin.setValue(default_damage)
            set_app_setting(db, "default_damage_percent", str(default_damage))

            self.apply_theme("light")
            QMessageBox.information(self, "Успех", "Настройки сброшены по умолчанию")
        finally:
            db.close()

    def save_current_settings(self):
        """Сохранение текущих настроек"""
        db = get_session()
        try:
            # 1. Сохраняем тему в JSON
            self.save_settings()

            # 2. Сохраняем процент поломки в БД
            set_app_setting(db, "default_damage_percent", str(self.damage_spin.value()))

            QMessageBox.information(self, "Успех", f"Настройки сохранены!\nТема: {self.current_theme}")
        finally:
            db.close()
# import json
# from pathlib import Path
# from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#                              QPushButton, QFrame, QRadioButton, QButtonGroup, QCheckBox, QComboBox,
#                              QLineEdit, QSpinBox, QScrollArea, QDoubleSpinBox)
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont, QPixmap
#
# from ui.utils.styles import get_settings_styles
# from backend.database import get_app_setting
#
#
# class SettingsPage(QWidget):
#     def __init__(self, icons_path, parent=None):
#         super().__init__(parent)
#         self.icons_path = icons_path
#         self.settings_path = Path(__file__).parent / "settings.json"
#         self.current_theme = "light"
#
#         self.load_settings()
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
#         settings = {"theme": self.current_theme}
#         with open(self.settings_path, "w", encoding="utf-8") as f:
#             json.dump(settings, f, ensure_ascii=False, indent=2)
#
#     def create_widgets(self):
#         """Создание контента страницы настроек"""
#
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)
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
#         # --- Секция 1: Оформление ---
#         appearance_group = self.create_settings_group(
#             "Оформление",
#             "Выберите тему и внешний вид приложения"
#         )
#         appearance_layout = QVBoxLayout()
#         appearance_layout.setSpacing(15)
#
#         theme_label = QLabel("Тема оформления")
#         theme_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         appearance_layout.addWidget(theme_label)
#
#         theme_options_layout = QHBoxLayout()
#         theme_options_layout.setSpacing(15)
#
#         self.theme_group = QButtonGroup()
#
#         self.light_radio = QRadioButton("Светлая")
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
#         appearance_layout.addLayout(theme_options_layout)
#
#         # Размер шрифта
#         font_size_layout = QHBoxLayout()
#         font_size_layout.setSpacing(15)
#
#         font_size_label = QLabel("Размер шрифта интерфейса")
#         font_size_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         font_size_layout.addWidget(font_size_label)
#         font_size_layout.addStretch()
#
#         self.font_size_combo = QComboBox()
#         self.font_size_combo.addItems(["Маленький (10)", "Обычный (12)", "Крупный (14)", "Очень крупный (16)"])
#         self.font_size_combo.setCurrentIndex(1)
#         self.font_size_combo.setFixedWidth(200)
#         self.font_size_combo.setFixedHeight(40)
#         self.font_size_combo.setObjectName("settingsCombo")
#         font_size_layout.addWidget(self.font_size_combo)
#         appearance_layout.addLayout(font_size_layout)
#
#         appearance_group.layout().addLayout(appearance_layout)
#         content_layout.addWidget(appearance_group)
#
#         # Секция: Параметры товаров
#         products_group = self.create_settings_group(
#             "Параметры товаров",
#             "Глобальные настройки для всех товаров"
#         )
#         products_layout = QVBoxLayout()
#         products_layout.setSpacing(15)
#
#         # Процент поломки
#         damage_layout = QHBoxLayout()
#         damage_layout.setSpacing(15)
#
#         damage_label = QLabel("Процент поломки/амортизации")
#         damage_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         damage_layout.addWidget(damage_label)
#         damage_layout.addStretch()
#
#         self.damage_spin = QDoubleSpinBox()
#         self.damage_spin.setRange(0.0, 100.0)
#         self.damage_spin.setValue(float(get_app_setting("default_damage_percent", "2.5")))
#         self.damage_spin.setSuffix("%")
#         self.damage_spin.setFixedWidth(100)
#         self.damage_spin.setFixedHeight(40)
#         self.damage_spin.setObjectName("settingsSpin")
#         damage_layout.addWidget(self.damage_spin)
#
#         products_layout.addLayout(damage_layout)
#         products_group.layout().addLayout(products_layout)
#         content_layout.addWidget(products_group)
#
#         # --- Секция 2: Общие настройки ---
#         general_group = self.create_settings_group(
#             "Общие",
#             "Основные параметры работы приложения"
#         )
#         general_layout = QVBoxLayout()
#         general_layout.setSpacing(15)
#
#         lang_layout = QHBoxLayout()
#         lang_layout.setSpacing(15)
#
#         lang_label = QLabel("Язык интерфейса")
#         lang_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         lang_layout.addWidget(lang_label)
#         lang_layout.addStretch()
#
#         self.lang_combo = QComboBox()
#         self.lang_combo.addItems(["Русский", "English"])
#         self.lang_combo.setCurrentIndex(0)
#         self.lang_combo.setFixedWidth(200)
#         self.lang_combo.setFixedHeight(40)
#         self.lang_combo.setObjectName("settingsCombo")
#         lang_layout.addWidget(self.lang_combo)
#         general_layout.addLayout(lang_layout)
#
#         self.notify_checkbox = QCheckBox("Показывать уведомления о завершении операций")
#         self.notify_checkbox.setFont(QFont("Segoe UI", 12))
#         self.notify_checkbox.setChecked(True)
#         self.notify_checkbox.setObjectName("settingsCheckbox")
#         general_layout.addWidget(self.notify_checkbox)
#
#         self.autosave_checkbox = QCheckBox("Автосохранение настроек при изменении")
#         self.autosave_checkbox.setFont(QFont("Segoe UI", 12))
#         self.autosave_checkbox.setChecked(True)
#         self.autosave_checkbox.setObjectName("settingsCheckbox")
#         general_layout.addWidget(self.autosave_checkbox)
#
#         general_group.layout().addLayout(general_layout)
#         content_layout.addWidget(general_group)
#
#         # --- Секция 3: Парсинг ---
#         parsing_group = self.create_settings_group(
#             "Парсинг маркетплейсов",
#             "Настройки поиска товаров на внешних площадках"
#         )
#         parsing_layout = QVBoxLayout()
#         parsing_layout.setSpacing(15)
#
#         timeout_layout = QHBoxLayout()
#         timeout_layout.setSpacing(15)
#
#         timeout_label = QLabel("Таймаут между запросами (секунды)")
#         timeout_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         timeout_layout.addWidget(timeout_label)
#         timeout_layout.addStretch()
#
#         self.timeout_spin = QSpinBox()
#         self.timeout_spin.setRange(1, 30)
#         self.timeout_spin.setValue(5)
#         self.timeout_spin.setFixedWidth(100)
#         self.timeout_spin.setFixedHeight(40)
#         self.timeout_spin.setObjectName("settingsSpin")
#         timeout_layout.addWidget(self.timeout_spin)
#         parsing_layout.addLayout(timeout_layout)
#
#         max_items_layout = QHBoxLayout()
#         max_items_layout.setSpacing(15)
#
#         max_items_label = QLabel("Максимум товаров на запрос")
#         max_items_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         max_items_layout.addWidget(max_items_label)
#         max_items_layout.addStretch()
#
#         self.max_items_spin = QSpinBox()
#         self.max_items_spin.setRange(5, 100)
#         self.max_items_spin.setValue(20)
#         self.max_items_spin.setFixedWidth(100)
#         self.max_items_spin.setFixedHeight(40)
#         self.max_items_spin.setObjectName("settingsSpin")
#         max_items_layout.addWidget(self.max_items_spin)
#         parsing_layout.addLayout(max_items_layout)
#
#         self.proxy_checkbox = QCheckBox("Использовать прокси-сервер для парсинга")
#         self.proxy_checkbox.setFont(QFont("Segoe UI", 12))
#         self.proxy_checkbox.setChecked(False)
#         self.proxy_checkbox.setObjectName("settingsCheckbox")
#         parsing_layout.addWidget(self.proxy_checkbox)
#
#         parsing_group.layout().addLayout(parsing_layout)
#         content_layout.addWidget(parsing_group)
#
#         # --- Секция 4: База данных ---
#         database_group = self.create_settings_group(
#             "База данных",
#             "Управление локальной базой данных приложения"
#         )
#         database_layout = QVBoxLayout()
#         database_layout.setSpacing(15)
#
#         db_path_layout = QHBoxLayout()
#         db_path_layout.setSpacing(15)
#
#         db_path_label = QLabel("Путь к базе данных")
#         db_path_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         db_path_layout.addWidget(db_path_label)
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
#         database_layout.addLayout(db_path_layout)
#
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
#         content_layout.addLayout(save_buttons_layout)
#
#         scroll_area.setWidget(scroll_widget)
#         layout.addWidget(scroll_area)
#         # ✅ Layout уже привязан к self через QVBoxLayout(self)
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
#         title_label = QLabel(title)
#         title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
#         title_label.setObjectName("groupTitle")
#
#         desc_label = QLabel(description)
#         desc_label.setFont(QFont("Segoe UI", 11))
#         desc_label.setObjectName("groupDescription")
#
#         layout.addWidget(title_label)
#         layout.addWidget(desc_label)
#
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
#         self.apply_theme(self.current_theme)
#
#     def apply_theme(self, theme):
#         """Применение выбранной темы через централизованные стили"""
#         self.setStyleSheet(get_settings_styles(theme))
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
#         print("Открытие диалога выбора файла БД")
#
#     def clear_cache(self):
#         print("Кэш очищен")
#
#     def reset_database(self):
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
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     app.setStyle("Fusion")
# #     app.setFont(QFont("Segoe UI", 10))
# #
# #     # Для тестирования создаем временное окно
# #     from PyQt6.QtWidgets import QMainWindow
# #
# #     window = QMainWindow()
# #     window.setWindowTitle("Тест: Справочник товаров")
# #     window.setGeometry(100, 100, 1400, 900)
# #
# #     icons_path = Path(__file__).parent / "icons"
# #     page = SettingsPage(icons_path)
# #     window.setCentralWidget(page)
# #
# #     window.show()
# #     sys.exit(app.exec())