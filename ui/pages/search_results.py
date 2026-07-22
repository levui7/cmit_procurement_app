"""
Страница результатов поиска товаров на маркетплейсах
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QMessageBox,
                             QScrollArea, QRadioButton)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QDesktopServices

from backend.crud.crud_procurement import get_request_by_id, delete_procurement_request
from backend.database import get_session

from ui.utils.config import Colors, Fonts, Spacing, Sizes
from ui.utils.icons import create_icon_label, IconNames
from ui.utils.styles import get_catalog_styles
# from ui.dialogs.review_dialog import ReviewDialog


class SearchResultsPage(QWidget):
    """Страница отображения результатов поиска товаров"""

    def __init__(self, request_id=None, parent=None):
        super().__init__(parent)
        self.request_id = request_id
        self.request_data = None
        self.marketplace_products = []  # Результаты поиска

        self.create_widgets()
        self.apply_styles()

        if request_id:
            self.load_results()

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
        layout.setSpacing(Spacing.LG)

        # Заголовок
        title = QLabel("Результаты поиска товаров")
        title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_DISPLAY, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)

        self.subtitle = QLabel("")
        self.subtitle.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        self.subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(self.subtitle)

        # Скроллируемая область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(Spacing.LG)

        scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(scroll_area)

        # Итоговая панель
        summary_card = QFrame()
        summary_card.setObjectName("formCard")
        summary_layout = QHBoxLayout(summary_card)
        summary_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)

        # Сумма
        total_layout = QVBoxLayout()
        total_label = QLabel("Итоговая сумма:")
        total_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL, QFont.Weight.Bold))
        total_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        total_layout.addWidget(total_label)

        self.total_amount_label = QLabel("0 ₽")
        self.total_amount_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_HEADING, QFont.Weight.Bold))
        self.total_amount_label.setStyleSheet(f"color: {Colors.PRIMARY};")
        total_layout.addWidget(self.total_amount_label)

        summary_layout.addLayout(total_layout)
        summary_layout.addStretch()

        # Кнопка "Удалить заявку"
        delete_btn = QPushButton("Удалить заявку")
        delete_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        delete_btn.setFixedSize(200, Sizes.BUTTON_HEIGHT)
        delete_btn.setObjectName("deleteButton")  # Красный стиль
        delete_btn.clicked.connect(self.delete_request)
        summary_layout.addWidget(delete_btn)
        
        # Кнопка "Назад"
        back_btn = QPushButton("Назад")
        back_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        back_btn.setFixedSize(120, Sizes.BUTTON_HEIGHT)
        back_btn.setObjectName("clearButton")
        back_btn.clicked.connect(self.go_back)
        summary_layout.addWidget(back_btn)

        layout.addWidget(summary_card)

    def _clear_results(self):
        """Очистить старые результаты перед загрузкой новых"""
        while self.scroll_layout.count() > 0:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_results(self):
        """Загрузка результатов поиска"""
        if not self.request_id:
            return

        self._clear_results()
        self.marketplace_products = []

        db = get_session()
        try:
            # Получаем данные заявки
            self.request_data = get_request_by_id(db, self.request_id)

            if self.request_data:
                # Обновляем подзаголовок
                self.subtitle.setText(
                    f"Заявка #{self.request_data.number} • "
                    f"{self.request_data.students_count} студентов • "
                    f"Дата доставки: {self.request_data.delivery_date}"
                )

            # ==========================================================
            # ИЗМЕНЕНИЕ: Загружаем реальные результаты парсинга из БД
            # ==========================================================
            from backend.services.search_results_service import get_parsed_results_for_ui
            self.marketplace_products = get_parsed_results_for_ui(self.request_id)
            
            # Если база пуста (парсинг еще не прошел), используем заглушку для демо
            if not self.marketplace_products:
                self.marketplace_products = self._get_mock_results()

            # Отображаем результаты (Важно: этот блок должен быть ВНЕ условия if!)
            for product_data in self.marketplace_products:
                card = self.create_product_card(product_data)
                self.scroll_layout.addWidget(card)

            self.scroll_layout.addStretch()

            # Подсчитываем сумму
            self._calculate_total()
            
        finally:
            db.close()

    def _get_mock_results(self):
        """Заглушка для демонстрации (удалить при реализации парсинга)"""
        return [
            {
                'internal_product_id': 1,
                'product_name': 'Светодиоды 5мм красные',
                'variants': [
                    {
                        'marketplace': 'Ozon',
                        'name': 'Светодиоды красные 5мм (20шт)',
                        'price': 150.0,
                        'rating': 4.5,
                        'url': 'https://ozon.ru/product/123',
                        'reviews_count': 45
                    },
                    {
                        'marketplace': 'Wildberries',
                        'name': 'LED красные 5мм набор',
                        'price': 120.0,
                        'rating': 4.2,
                        'url': 'https://wb.ru/catalog/456',
                        'reviews_count': 32
                    },
                ]
            },
        ]

    def create_product_card(self, product_data):
        """Создание карточки товара с вариантами"""
        card = QFrame()
        card.setObjectName("formCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        card_layout.setSpacing(Spacing.SM)

        # Заголовок товара
        product_title = QLabel(product_data['product_name'])
        product_title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_LARGE, QFont.Weight.Bold))
        product_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        card_layout.addWidget(product_title)

        # Таблица вариантов
        variants_table = QTableWidget()
        variants_table.setColumnCount(6)
        variants_table.setHorizontalHeaderLabels([
            "Выбрать", "Маркетплейс", "Название", "Цена, ₽", "Рейтинг", "Действия"
        ])
        variants_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        variants_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        variants_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        variants_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        variants_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        variants_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        variants_table.verticalHeader().setVisible(False)
        variants_table.setFixedHeight(150)

        for i, variant in enumerate(product_data['variants']):
            row = variants_table.rowCount()
            variants_table.insertRow(row)

            # Радиокнопка выбора
            radio = QRadioButton()
            radio_widget = QWidget()
            radio_layout = QHBoxLayout(radio_widget)
            radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            radio_layout.setContentsMargins(0, 0, 0, 0)
            radio_layout.addWidget(radio)
            variants_table.setCellWidget(row, 0, radio_widget)

            # Маркетплейс
            marketplace_item = QTableWidgetItem(variant['marketplace'])
            variants_table.setItem(row, 1, marketplace_item)

            # Название
            name_item = QTableWidgetItem(variant['name'])
            variants_table.setItem(row, 2, name_item)

            # Цена
            price_item = QTableWidgetItem(f"{variant['price']:.0f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            variants_table.setItem(row, 3, price_item)

            # Рейтинг
            rating_item = QTableWidgetItem(f"⭐ {variant['rating']}")
            rating_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            variants_table.setItem(row, 4, rating_item)

            # Кнопки действий
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(5)

            # Кнопка "Перейти"
            link_btn = QPushButton("🔗")
            link_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_XSMALL))
            link_btn.setFixedHeight(25)
            link_btn.setFixedWidth(30)
            link_btn.setObjectName("editButton")
            link_btn.setToolTip("Открыть ссылку на товар")
            link_btn.clicked.connect(lambda checked, url=variant['url']: self.open_link(url))
            actions_layout.addWidget(link_btn)

            variants_table.setCellWidget(row, 5, actions_widget)

        card_layout.addWidget(variants_table)
        return card

    def delete_request(self):
        """Удалить текущую заявку"""
        print(f"🔍 Попытка удаления заявки #{self.request_id}")

        if not self.request_id:
            QMessageBox.warning(self, "Ошибка", "Не выбрана заявка для удаления!")
            return

        # Подтверждение удаления
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить заявку #{self.request_data.number if self.request_data else self.request_id}?\n\n"
            f"Это действие нельзя отменить!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            db = get_session()
            try:
                success = delete_procurement_request(db, self.request_id)

                if success:
                    QMessageBox.information(self, "Успех", "Заявка удалена!")
                    # Возвращаемся в историю заявок
                    self.go_back()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось удалить заявку!")
            finally:
                db.close()

    def open_link(self, url):
        """Открыть ссылку в браузере"""
        QDesktopServices.openUrl(QUrl(url))

    def _calculate_total(self):
        """Подсчитать итоговую сумму"""
        # TODO: Реальная логика подсчета
        total = 0
        self.total_amount_label.setText(f"{total} ₽")

    def go_back(self):
        """Вернуться в Историю заявок с обновлением"""
        parent = self.parent()
        while parent is not None:
            if hasattr(parent, 'switch_page'):
                # ✅ 1. Находим страницу истории
                history_page = parent.pages.get("История заявок")

                # ✅ 2. Принудительно обновляем данные истории
                if history_page and hasattr(history_page, 'load_history'):
                    history_page.load_history()

                # ✅ 3. Только после обновления переключаемся
                parent.switch_page("История заявок")
                return
            parent = parent.parent()

    def apply_styles(self):
        self.setStyleSheet(get_catalog_styles())