# import sys
# from pathlib import Path
# from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#                              QPushButton, QFrame, QSizePolicy, QApplication, QDialog,
#                              QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView,
#                              QLineEdit, QAbstractItemView)
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont, QPixmap, QIcon
#
#
# class CatalogWindow(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         # Путь к папке с иконками
#         self.icons_path = Path(__file__).parent / "icons"
#
#         # Настройки окна
#         self.setWindowTitle("Справочник товаров - Закупки ЦМИТ ЛЮКС")
#         self.setGeometry(100, 100, 1400, 900)
#         self.setMinimumSize(1200, 800)
#
#         # Иконка окна
#         icon_path = self.icons_path / "cmit_logo_parody.png"
#         if icon_path.exists():
#             self.setWindowIcon(QIcon(str(icon_path)))
#
#         # Создаем интерфейс
#         self.create_widgets()
#         self.apply_styles()
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
#             ("product.png", "Справочник товаров", True),  # ← Активная кнопка
#             ("light-bulb.png", "О предприятии", False),
#             ("settings.png", "Настройки", False),
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
#         # Основной контент
#         content_layout = QVBoxLayout()
#         content_layout.setContentsMargins(50, 40, 50, 40)
#         content_layout.setSpacing(20)
#
#         # Заголовок страницы
#         title = QLabel("Справочник товаров")
#         title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
#         title.setStyleSheet("color: #1F2937;")
#
#         subtitle = QLabel("Управляйте внутренним каталогом товаров для закупки")
#         subtitle.setFont(QFont("Segoe UI", 13))
#         subtitle.setStyleSheet("color: #6B7280;")
#
#         content_layout.addWidget(title)
#         content_layout.addWidget(subtitle)
#         content_layout.addSpacing(10)
#
#         # Панель инструментов: поиск + кнопки
#         toolbar = QHBoxLayout()
#         toolbar.setSpacing(15)
#
#         # # Поле поиска
#         # search_input = QLineEdit()
#         # search_input.setPlaceholderText("🔍 Поиск по названию товара...")
#         # search_input.setFont(QFont("Segoe UI", 12))
#         # search_input.setFixedHeight(45)
#         # search_input.setObjectName("searchInput")
#         # toolbar.addWidget(search_input, stretch=1)
#
#         # Поле поиска с иконкой
#         search_container = QFrame()
#         search_container.setObjectName("searchContainer")
#         search_container.setFixedHeight(45)
#
#         search_layout = QHBoxLayout(search_container)
#         search_layout.setContentsMargins(15, 0, 15, 0)
#         search_layout.setSpacing(10)
#
#         # Иконка лупы
#         search_icon = self.create_icon_label("magnifying-glass.png", size=20)
#         search_layout.addWidget(search_icon)
#
#         # Поле ввода
#         search_input = QLineEdit()
#         search_input.setPlaceholderText("Поиск по названию товара...")
#         search_input.setFont(QFont("Segoe UI", 12))
#         search_input.setObjectName("searchInput")
#         search_input.setStyleSheet("border: none; padding: 0; background-color: transparent;")
#         search_layout.addWidget(search_input)
#
#         toolbar.addWidget(search_container, stretch=1)
#
#         # Кнопка "Добавить товар"
#         add_btn = QPushButton("+ Добавить товар")
#         add_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
#         add_btn.setFixedHeight(45)
#         add_btn.setFixedWidth(180)
#         add_btn.setObjectName("addButton")
#         add_btn.clicked.connect(self.add_product)
#         toolbar.addWidget(add_btn)
#
#         # # Кнопка "Импорт из Excel"
#         # import_btn = QPushButton("📊 Импорт из Excel")
#         # import_btn.setFont(QFont("Segoe UI", 12))
#         # import_btn.setFixedHeight(45)
#         # import_btn.setFixedWidth(180)
#         # import_btn.setObjectName("importButton")
#         # import_btn.clicked.connect(self.import_excel)
#         # toolbar.addWidget(import_btn)
#
#         # Кнопка "Импорт из Excel" с иконкой
#         import_btn = QPushButton()
#         import_btn.setFixedHeight(45)
#         import_btn.setFixedWidth(180)
#         import_btn.setObjectName("importButton")
#         import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
#         import_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
#
#         # Layout внутри кнопки
#         import_layout = QHBoxLayout(import_btn)
#         import_layout.setContentsMargins(15, 10, 15, 10)
#         import_layout.setSpacing(10)
#
#         # Иконка
#         import_icon = self.create_icon_label("stats.png", size=20)
#
#         # Текст
#         import_text = QLabel("Импорт из Excel")
#         import_text.setFont(QFont("Segoe UI", 12))
#         import_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
#
#         import_layout.addWidget(import_icon)
#         import_layout.addWidget(import_text)
#         import_layout.addStretch()
#
#         import_btn.clicked.connect(self.import_excel)
#         toolbar.addWidget(import_btn)
#
#         # Кнопка "Экспорт в Excel"
#         export_btn = QPushButton(" Экспорт в Excel")
#         export_btn.setFont(QFont("Segoe UI", 12))
#         export_btn.setFixedHeight(45)
#         export_btn.setFixedWidth(180)
#         export_btn.setObjectName("exportButton")
#         export_btn.clicked.connect(self.export_excel)
#         toolbar.addWidget(export_btn)
#
#         content_layout.addLayout(toolbar)
#
#         # Таблица товаров
#         table = self.create_products_table()
#         content_layout.addWidget(table)
#
#         # Нижняя панель: пагинация
#         bottom_layout = QHBoxLayout()
#         bottom_layout.setSpacing(20)
#
#         pagination_info = QLabel("1–10 из 120 товаров")
#         pagination_info.setFont(QFont("Segoe UI", 11))
#         pagination_info.setStyleSheet("color: #6B7280;")
#         bottom_layout.addWidget(pagination_info)
#
#         bottom_layout.addStretch()
#
#         # Кнопки пагинации
#         pagination = self.create_pagination()
#         bottom_layout.addWidget(pagination)
#
#         content_layout.addLayout(bottom_layout)
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
#         main_layout.addLayout(content_layout)
#         self.setLayout(main_layout)
#
#     def create_products_table(self):
#         """Создание таблицы товаров"""
#         table = QTableWidget()
#         table.setObjectName("productsTable")
#         table.setRowCount(10)
#         table.setColumnCount(5)
#
#         # Заголовки столбцов
#         headers = ["Название", "Категория", "% поломки", "Ключевые слова", "Действия"]
#         table.setHorizontalHeaderLabels(headers)
#
#         # Настройка таблицы
#         table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
#         table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
#         table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
#         table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
#         table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
#
#         table.verticalHeader().setVisible(False)
#         table.setAlternatingRowColors(False)
#         table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
#         table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
#
#         # Мок-данные
#         products_data = [
#             ("Бумага офисная A4, 80 г/м²", "Канцелярские товары", "2.5%", "бумага, офисная, A4, 80 г/м2"),
#             ("Картридж HP LaserJet 12A", "Расходные материалы", "4.2%", "картридж, HP, 12A, принтер"),
#             ("Ручка шариковая синяя", "Канцелярские товары", "1.1%", "ручка, шариковая, синяя"),
#             ("Кабель витая пара UTP Cat.5e", "Кабельная продукция", "3.3%", "кабель, витая пара, UTP, Cat.5e"),
#             ("Светильник LED 36W", "Электрика", "2.8%", "светильник, LED, 36W, офисный"),
#             ("Степлер №24/6", "Канцелярские товары", "1.7%", "степлер, №24/6, канцелярский"),
#             ("Папка-регистратор A4, 75 мм", "Канцелярские товары", "2.0%", "папка, регистратор, A4, 75 мм"),
#             ("Мышь компьютерная USB", "Компьютерная периферия", "3.9%", "мышь, USB, компьютерная"),
#             ("Клавиатура проводная USB", "Компьютерная периферия", "3.6%", "клавиатура, USB, проводная"),
#             ("Батарейка AA (LR6)", "Электрика", "0.9%", "батарейка, AA, LR6, щелочная"),
#         ]
#
#         # Заполнение таблицы
#         for row, (name, category, damage, keywords) in enumerate(products_data):
#             # Название
#             name_item = QTableWidgetItem(name)
#             name_item.setFont(QFont("Segoe UI", 11))
#             table.setItem(row, 0, name_item)
#
#             # Категория
#             category_item = QTableWidgetItem(category)
#             category_item.setFont(QFont("Segoe UI", 11))
#             table.setItem(row, 1, category_item)
#
#             # % поломки
#             damage_item = QTableWidgetItem(damage)
#             damage_item.setFont(QFont("Segoe UI", 11))
#             damage_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             table.setItem(row, 2, damage_item)
#
#             # Ключевые слова
#             keywords_item = QTableWidgetItem(keywords)
#             keywords_item.setFont(QFont("Segoe UI", 11))
#             table.setItem(row, 3, keywords_item)
#
#             # Кнопка "Изменить"
#             edit_btn = QPushButton("✏️ Изменить")
#             edit_btn.setFont(QFont("Segoe UI", 10))
#             edit_btn.setFixedSize(120, 32)
#             edit_btn.setObjectName("editButton")
#             edit_btn.clicked.connect(lambda checked, r=row: self.edit_product(r))
#             table.setCellWidget(row, 4, edit_btn)
#
#         # Высота строк
#         for row in range(table.rowCount()):
#             table.setRowHeight(row, 50)
#
#         # Высота заголовков
#         table.horizontalHeader().setFixedHeight(45)
#
#         return table
#
#     def create_pagination(self):
#         """Создание блока пагинации"""
#         pagination = QFrame()
#         pagination.setObjectName("pagination")
#
#         layout = QHBoxLayout(pagination)
#         layout.setContentsMargins(10, 5, 10, 5)
#         layout.setSpacing(5)
#
#         pages = ["<", "1", "2", "3", "...", "12", ">"]
#
#         for page in pages:
#             btn = QPushButton(page)
#             btn.setFont(QFont("Segoe UI", 11))
#             btn.setFixedSize(35, 35)
#
#             if page == "1":
#                 btn.setObjectName("currentPage")
#             elif page in ["<", ">"]:
#                 btn.setObjectName("navButton")
#             else:
#                 btn.setObjectName("pageButton")
#
#             layout.addWidget(btn)
#
#         return pagination
#
#     def create_exit_card(self):
#         """Создание мини-карточки выхода (без надписи "Завершить работу")"""
#         card = QFrame()
#         card.setObjectName("exitCard")
#         card.setFixedSize(180, 70)  # Уменьшенный размер
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
#     def add_product(self):
#         """Добавить товар"""
#         print("Добавление нового товара")
#
#     def import_excel(self):
#         """Импорт из Excel"""
#         print("Импорт из Excel")
#
#     def export_excel(self):
#         """Экспорт в Excel"""
#         print("Экспорт в Excel")
#
#     def edit_product(self, row):
#         """Редактировать товар"""
#         print(f"Редактирование товара в строке {row}")
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
#         subtitle_label = QLabel("Возможно, остались незавершенные дела")
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
#     def apply_styles(self):
#         """Применение стилей"""
#         self.setStyleSheet("""
#             QWidget {
#                 background-color: #F9FAFB;
#             }
#
#             QLabel {
#                 selection-background-color: transparent;
#                 selection-color: transparent;
#                 background-color: transparent;
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
#             #searchInput {
#                 background-color: #FFFFFF;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 8px;
#                 padding: 10px 15px;
#                 color: #1F2937;
#             }
#
#             #searchInput:focus {
#                 border: 2px solid #3B82F6;
#             }
#
#             #addButton {
#                 background-color: #3B82F6;
#                 color: white;
#                 border: none;
#                 border-radius: 8px;
#             }
#
#             #addButton:hover {
#                 background-color: #2563EB;
#             }
#
#             #importButton {
#                 background-color: #FFFFFF;
#                 color: #374151;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 8px;
#             }
#
#             #importButton:hover {
#                 background-color: #F3F4F6;
#             }
#
#             #exportButton {
#                 background-color: #FFFFFF;
#                 color: #374151;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 8px;
#             }
#
#             #exportButton:hover {
#                 background-color: #F3F4F6;
#             }
#
#             #productsTable {
#                 background-color: #FFFFFF;
#                 border: 1px solid #E5E7EB;
#                 border-radius: 12px;
#                 gridline-color: #E5E7EB;
#             }
#
#             #productsTable QHeaderView::section {
#                 background-color: #F9FAFB;
#                 color: #6B7280;
#                 border: none;
#                 border-bottom: 1px solid #E5E7EB;
#                 padding: 10px;
#                 font-weight: bold;
#             }
#
#             #productsTable QTableCornerButton::section {
#                 background-color: #F9FAFB;
#                 border: none;
#                 border-bottom: 1px solid #E5E7EB;
#             }
#
#             #productsTable::item {
#                 padding: 8px;
#                 border-bottom: 1px solid #F3F4F6;
#             }
#
#             #editButton {
#                 background-color: #FFFFFF;
#                 color: #3B82F6;
#                 border: 1px solid #BFDBFE;
#                 border-radius: 6px;
#             }
#
#             #editButton:hover {
#                 background-color: #EFF6FF;
#             }
#
#             #currentPage {
#                 background-color: #3B82F6;
#                 color: white;
#                 border: none;
#                 border-radius: 6px;
#             }
#
#             #pageButton {
#                 background-color: #FFFFFF;
#                 color: #374151;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 6px;
#             }
#
#             #pageButton:hover {
#                 background-color: #F3F4F6;
#             }
#
#             #navButton {
#                 background-color: #FFFFFF;
#                 color: #6B7280;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 6px;
#             }
#
#             #navButton:hover {
#                 background-color: #F3F4F6;
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
#
#             #searchContainer {
#     background-color: #FFFFFF;
#     border: 1px solid #D1D5DB;
#     border-radius: 8px;
# }
#
# #searchContainer:focus-within {
#     border: 2px solid #3B82F6;
# }
#
# #searchInput {
#     background-color: transparent;
#     border: none;
#     padding: 0 5px;
#     color: #1F2937;
# }
#
# #searchInput:focus {
#     outline: none;
# }
#         """)
#
#
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     app.setStyle("Fusion")
# #     app.setFont(QFont("Segoe UI", 10))
# #
# #     window = CatalogWindow()
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
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QSizePolicy, QApplication, QDialog,
                             QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView,
                             QLineEdit, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon


class CatalogPage(QWidget):
    def __init__(self, icons_path, parent=None):
        super().__init__(parent)

        # Получаем путь к иконкам от родительского окна
        self.icons_path = icons_path

        # Создаем только контент этой страницы
        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        """Создание элементов интерфейса СТРАНИЦЫ справочника товаров"""
        # Основной вертикальный layout для контента страницы
        content_layout = QVBoxLayout(self)
        content_layout.setContentsMargins(50, 40, 50, 40)
        content_layout.setSpacing(20)

        # 1. Заголовок страницы
        title = QLabel("Справочник товаров")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")

        subtitle = QLabel("Управляйте внутренним каталогом товаров для закупки")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #6B7280;")

        content_layout.addWidget(title)
        content_layout.addWidget(subtitle)
        content_layout.addSpacing(10)

        # 2. Панель инструментов: поиск + кнопки
        toolbar = QHBoxLayout()
        toolbar.setSpacing(15)

        # Поле поиска с иконкой
        search_container = QFrame()
        search_container.setObjectName("searchContainer")
        search_container.setFixedHeight(45)

        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(15, 0, 15, 0)
        search_layout.setSpacing(10)

        # Иконка лупы
        search_icon = self.create_icon_label("magnifying-glass.png", size=20)
        search_layout.addWidget(search_icon)

        # Поле ввода
        search_input = QLineEdit()
        search_input.setPlaceholderText("Поиск по названию товара...")
        search_input.setFont(QFont("Segoe UI", 12))
        search_input.setObjectName("searchInput")
        search_input.setStyleSheet("border: none; padding: 0; background-color: transparent;")
        search_layout.addWidget(search_input)

        toolbar.addWidget(search_container, stretch=1)

        # Кнопка "Добавить товар"
        add_btn = QPushButton("+ Добавить товар")
        add_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        add_btn.setFixedHeight(45)
        add_btn.setFixedWidth(180)
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.add_product)
        toolbar.addWidget(add_btn)

        # Кнопка "Импорт из Excel" с иконкой
        import_btn = QPushButton()
        import_btn.setFixedHeight(45)
        import_btn.setFixedWidth(180)
        import_btn.setObjectName("importButton")
        import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        import_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        import_layout = QHBoxLayout(import_btn)
        import_layout.setContentsMargins(15, 10, 15, 10)
        import_layout.setSpacing(10)

        import_icon = self.create_icon_label("stats.png", size=20)
        import_text = QLabel("Импорт из Excel")
        import_text.setFont(QFont("Segoe UI", 12))
        import_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        import_layout.addWidget(import_icon)
        import_layout.addWidget(import_text)
        import_layout.addStretch()

        import_btn.clicked.connect(self.import_excel)
        toolbar.addWidget(import_btn)

        # Кнопка "Экспорт в Excel"
        export_btn = QPushButton("Экспорт в Excel")
        export_btn.setFont(QFont("Segoe UI", 12))
        export_btn.setFixedHeight(45)
        export_btn.setFixedWidth(180)
        export_btn.setObjectName("exportButton")
        export_btn.clicked.connect(self.export_excel)
        toolbar.addWidget(export_btn)

        content_layout.addLayout(toolbar)

        # 3. Таблица товаров
        table = self.create_products_table()
        content_layout.addWidget(table)

        # 4. Нижняя панель: пагинация
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        pagination_info = QLabel("1–10 из 120 товаров")
        pagination_info.setFont(QFont("Segoe UI", 11))
        pagination_info.setStyleSheet("color: #6B7280;")
        bottom_layout.addWidget(pagination_info)

        bottom_layout.addStretch()

        pagination = self.create_pagination()
        bottom_layout.addWidget(pagination)

        content_layout.addLayout(bottom_layout)

        # 5. Мини-карточка выхода в правом нижнем углу
        exit_layout = QHBoxLayout()
        exit_layout.addStretch()

        exit_card = self.create_exit_card()
        exit_layout.addWidget(exit_card)

        content_layout.addLayout(exit_layout)

    def create_products_table(self):
        """Создание таблицы товаров"""
        table = QTableWidget()
        table.setObjectName("productsTable")
        table.setRowCount(10)
        table.setColumnCount(5)

        # Заголовки столбцов
        headers = ["Название", "Категория", "% поломки", "Ключевые слова", "Действия"]
        table.setHorizontalHeaderLabels(headers)

        # Настройка таблицы
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Мок-данные
        products_data = [
            ("Бумага офисная A4, 80 г/м²", "Канцелярские товары", "2.5%", "бумага, офисная, A4, 80 г/м2"),
            ("Картридж HP LaserJet 12A", "Расходные материалы", "4.2%", "картридж, HP, 12A, принтер"),
            ("Ручка шариковая синяя", "Канцелярские товары", "1.1%", "ручка, шариковая, синяя"),
            ("Кабель витая пара UTP Cat.5e", "Кабельная продукция", "3.3%", "кабель, витая пара, UTP, Cat.5e"),
            ("Светильник LED 36W", "Электрика", "2.8%", "светильник, LED, 36W, офисный"),
            ("Степлер №24/6", "Канцелярские товары", "1.7%", "степлер, №24/6, канцелярский"),
            ("Папка-регистратор A4, 75 мм", "Канцелярские товары", "2.0%", "папка, регистратор, A4, 75 мм"),
            ("Мышь компьютерная USB", "Компьютерная периферия", "3.9%", "мышь, USB, компьютерная"),
            ("Клавиатура проводная USB", "Компьютерная периферия", "3.6%", "клавиатура, USB, проводная"),
            ("Батарейка AA (LR6)", "Электрика", "0.9%", "батарейка, AA, LR6, щелочная"),
        ]

        # Заполнение таблицы
        for row, (name, category, damage, keywords) in enumerate(products_data):
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("Segoe UI", 11))
            table.setItem(row, 0, name_item)

            category_item = QTableWidgetItem(category)
            category_item.setFont(QFont("Segoe UI", 11))
            table.setItem(row, 1, category_item)

            damage_item = QTableWidgetItem(damage)
            damage_item.setFont(QFont("Segoe UI", 11))
            damage_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 2, damage_item)

            keywords_item = QTableWidgetItem(keywords)
            keywords_item.setFont(QFont("Segoe UI", 11))
            table.setItem(row, 3, keywords_item)

            edit_btn = QPushButton("✏️ Изменить")
            edit_btn.setFont(QFont("Segoe UI", 10))
            edit_btn.setFixedSize(120, 32)
            edit_btn.setObjectName("editButton")
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_product(r))
            table.setCellWidget(row, 4, edit_btn)

        # Высота строк
        for row in range(table.rowCount()):
            table.setRowHeight(row, 50)

        # Высота заголовков
        table.horizontalHeader().setFixedHeight(45)

        return table

    def create_pagination(self):
        """Создание блока пагинации"""
        pagination = QFrame()
        pagination.setObjectName("pagination")

        layout = QHBoxLayout(pagination)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        pages = ["<", "1", "2", "3", "...", "12", ">"]

        for page in pages:
            btn = QPushButton(page)
            btn.setFont(QFont("Segoe UI", 11))
            btn.setFixedSize(35, 35)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            if page == "1":
                btn.setObjectName("currentPage")
            elif page in ["<", ">"]:
                btn.setObjectName("navButton")
            else:
                btn.setObjectName("pageButton")

            btn.clicked.connect(lambda checked, p=page: print(f"Переход на страницу {p}"))

            layout.addWidget(btn)

        return pagination

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
            print(f"⚠️ Иконка не найдена: {icon_path}")

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

    def add_product(self):
        """Добавить товар"""
        print("Добавление нового товара")

    def import_excel(self):
        """Импорт из Excel"""
        print("Импорт из Excel")

    def export_excel(self):
        """Экспорт в Excel"""
        print("Экспорт в Excel")

    def edit_product(self, row):
        """Редактировать товар"""
        print(f"Редактирование товара в строке {row}")

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
        """Подтверждение выхода — закрытие всего приложения"""
        dialog.accept()
        QApplication.instance().quit()

    def apply_styles(self):
        """Применение стилей ТОЛЬКО для этой страницы"""



        # self.setStyleSheet("""
        #     QWidget {
        #         background-color: #F9FAFB;
        #     }
        #
        #     QLabel {
        #         selection-background-color: transparent;
        #         selection-color: transparent;
        #         background-color: transparent;
        #     }
        #
        #     QToolTip {
        #         background-color: #F9FAFB;
        #         color: #334155;
        #         border: 1px solid #D1D5DB;
        #         border-radius: 8px;
        #         padding: 10px 14px;
        #         font-size: 12px;
        #         font-family: 'Segoe UI';
        #     }
        #
        #     QPushButton {
        #         selection-background-color: transparent;
        #         selection-color: transparent;
        #         outline: none;
        #     }
        #
        #     #searchContainer {
        #         background-color: #FFFFFF;
        #         border: 1px solid #D1D5DB;
        #         border-radius: 8px;
        #     }
        #
        #     #searchContainer:focus-within {
        #         border: 2px solid #3B82F6;
        #     }
        #
        #     #searchInput {
        #         background-color: transparent;
        #         border: none;
        #         padding: 0 5px;
        #         color: #1F2937;
        #     }
        #
        #     #searchInput:focus {
        #         outline: none;
        #     }
        #
        #     #addButton {
        #         background-color: #3B82F6;
        #         color: white;
        #         border: none;
        #         border-radius: 8px;
        #     }
        #
        #     #addButton:hover {
        #         background-color: #2563EB;
        #     }
        #
        #     #importButton {
        #         background-color: #FFFFFF;
        #         color: #374151;
        #         border: 1px solid #D1D5DB;
        #         border-radius: 8px;
        #     }
        #
        #     #importButton:hover {
        #         background-color: #F3F4F6;
        #     }
        #
        #     #exportButton {
        #         background-color: #FFFFFF;
        #         color: #374151;
        #         border: 1px solid #D1D5DB;
        #         border-radius: 8px;
        #     }
        #
        #     #exportButton:hover {
        #         background-color: #F3F4F6;
        #     }
        #
        #     #productsTable {
        #         background-color: #FFFFFF;
        #         border: 1px solid #E5E7EB;
        #         border-radius: 12px;
        #         gridline-color: #E5E7EB;
        #     }
        #
        #     #productsTable QHeaderView::section {
        #         background-color: #F9FAFB;
        #         color: #6B7280;
        #         border: none;
        #         border-bottom: 1px solid #E5E7EB;
        #         padding: 10px;
        #         font-weight: bold;
        #     }
        #
        #     #productsTable QTableCornerButton::section {
        #         background-color: #F9FAFB;
        #         border: none;
        #         border-bottom: 1px solid #E5E7EB;
        #     }
        #
        #     #productsTable::item {
        #         padding: 8px;
        #         border-bottom: 1px solid #F3F4F6;
        #     }
        #
        #     #editButton {
        #         background-color: #FFFFFF;
        #         color: #3B82F6;
        #         border: 1px solid #BFDBFE;
        #         border-radius: 6px;
        #     }
        #
        #     #editButton:hover {
        #         background-color: #EFF6FF;
        #     }
        #
        #     #currentPage {
        #         background-color: #3B82F6;
        #         color: white;
        #         border: none;
        #         border-radius: 6px;
        #     }
        #
        #     #pageButton {
        #         background-color: #FFFFFF;
        #         color: #374151;
        #         border: 1px solid #D1D5DB;
        #         border-radius: 6px;
        #     }
        #
        #     #pageButton:hover {
        #         background-color: #F3F4F6;
        #     }
        #
        #     #navButton {
        #         background-color: #FFFFFF;
        #         color: #6B7280;
        #         border: 1px solid #D1D5DB;
        #         border-radius: 6px;
        #     }
        #
        #     #navButton:hover {
        #         background-color: #F3F4F6;
        #     }
        #
        #     #exitCard {
        #         background-color: #FFFFFF;
        #         border: 1px solid #E5E7EB;
        #         border-radius: 10px;
        #     }
        #
        #     #exitCard:hover {
        #         border: 2px solid #EF4444;
        #     }
        # """)


# Блок для автономного тестирования этой страницы
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    # Для теста создаем временное окно, чтобы показать страницу
    from PyQt6.QtWidgets import QMainWindow

    window = QMainWindow()
    window.setWindowTitle("Тест: Справочник товаров")
    window.setGeometry(100, 100, 1400, 900)

    icons_path = Path(__file__).parent / "icons"
    page = CatalogPage(icons_path)
    window.setCentralWidget(page)

    window.show()
    sys.exit(app.exec())