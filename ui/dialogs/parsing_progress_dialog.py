"""
Диалог прогресса парсинга маркетплейсов
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QProgressBar,
                             QPushButton, QFrame, QHBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QEvent
from PyQt6.QtGui import QFont

from ui.utils.config import Colors, Fonts, Spacing, Sizes
from ui.utils.icons import create_icon_label, IconNames
from ui.utils.styles import get_dialog_styles


class ParsingWorker(QThread):
    """Поток для парсинга"""
    progress_updated = pyqtSignal(int, str)
    parsing_finished = pyqtSignal(bool, str)

    def __init__(self, request_number, items_count, parent=None):
        super().__init__(parent)
        self.request_number = request_number
        self.items_count = items_count
        self.is_cancelled = False

    def run(self):
        try:
            total_steps = max(1, self.items_count * 3)
            for i in range(total_steps):
                if self.is_cancelled:
                    self.parsing_finished.emit(False, "Парсинг отменён пользователем")
                    return

                percent = int((i + 1) / total_steps * 100)
                status = f"Обработка товара {i // 3 + 1} из {self.items_count}..."
                self.progress_updated.emit(percent, status)
                self.msleep(300)

            self.parsing_finished.emit(True, f"Найдено товаров: {self.items_count * 5}")
        except Exception as e:
            self.parsing_finished.emit(False, f"Ошибка парсинга: {str(e)}")

    def cancel(self):
        self.is_cancelled = True


class ParsingProgressDialog(QDialog):
    """Диалог отображения прогресса парсинга"""

    def __init__(self, request_number, items_count, request_date, parent=None):
        super().__init__(parent)
        self.request_number = str(request_number)
        self.items_count = int(items_count)
        self.request_date = str(request_date)
        self.worker = None

        self.setWindowTitle("Обработка заявки")
        self.setFixedSize(600, 350)
        self.setModal(True)

        self.create_widgets()
        self.apply_styles()
        # ❌ ВАЖНО: НЕ вызываем self.start_parsing() здесь!

    def showEvent(self, event):
        """Запускаем поток ТОЛЬКО после полной отрисовки окна"""
        super().showEvent(event)
        if event.type() == QEvent.Type.Show and self.worker is None:
            self.start_parsing()

    def closeEvent(self, event):
        """Безопасно останавливаем поток при закрытии окна"""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait(1000)  # Ждем завершения потока
        super().closeEvent(event)

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
        layout.setSpacing(Spacing.LG)

        header = QHBoxLayout()
        header.setSpacing(Spacing.SM)

        self.status_icon = create_icon_label(IconNames.STATS, size=48)
        header.addWidget(self.status_icon)

        title = QLabel("Поиск товаров на маркетплейсах")
        title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_HEADING, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        formatted_number = self.request_number.zfill(3)
        description = QLabel(f"Заявка №{formatted_number} от {self.request_date}")
        description.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        description.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(description)

        layout.addSpacing(Spacing.LG)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setObjectName("progressBar")
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Инициализация парсинга...")
        self.status_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        self.status_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addStretch()

        self.cancel_btn = QPushButton("Отменить")
        self.cancel_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        self.cancel_btn.setFixedSize(150, Sizes.BUTTON_HEIGHT)
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.clicked.connect(self.cancel_parsing)

        cancel_layout = QHBoxLayout()
        cancel_layout.addStretch()
        cancel_layout.addWidget(self.cancel_btn)
        cancel_layout.addStretch()
        layout.addLayout(cancel_layout)

    def start_parsing(self):
        self.worker = ParsingWorker(self.request_number, self.items_count)
        self.worker.progress_updated.connect(self.on_progress_updated)
        self.worker.parsing_finished.connect(self.on_parsing_finished)
        self.worker.start()

    def on_progress_updated(self, percent, status):
        self.progress_bar.setValue(percent)
        self.status_label.setText(status)

    def on_parsing_finished(self, success, message):
        if self.worker and self.worker.isRunning():
            self.worker.wait(500)

        self.cancel_btn.setEnabled(False)
        if success:
            self.status_icon = create_icon_label(IconNames.SAVE, size=48)
            self.status_label.setText(f"✅ {message}")
            self.status_label.setStyleSheet(f"color: {Colors.SUCCESS};")
            self.accept()
        else:
            self.status_label.setText(f"❌ {message}")
            self.status_label.setStyleSheet(f"color: {Colors.DANGER};")
            self.cancel_btn.setText("Закрыть")
            self.cancel_btn.setEnabled(True)

    def cancel_parsing(self):
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.status_label.setText("Отмена парсинга...")

    def apply_styles(self):
        styles = get_dialog_styles() + """
            QProgressBar {
                background-color: #E5E7EB;
                border: 1px solid #D1D5DB;
                border-radius: 15px;
                text-align: center;
                color: #1F2937;
            }
            QProgressBar::chunk {
                background-color: #3B82F6;
                border-radius: 15px;
            }
        """
        self.setStyleSheet(styles)

# """
# Диалог прогресса парсинга маркетплейсов
# """
# from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QProgressBar,
#                              QPushButton, QFrame, QHBoxLayout)
# from PyQt6.QtCore import Qt, pyqtSignal, QThread, QEvent
# from PyQt6.QtGui import QFont
#
# from ui.utils.config import Colors, Fonts, Spacing, Sizes
# from ui.utils.icons import create_icon_label, IconNames
# from ui.utils.styles import get_dialog_styles
#
#
# class ParsingWorker(QThread):
#     """Поток для парсинга (заглушка для демонстрации)"""
#     progress_updated = pyqtSignal(int, str)
#     parsing_finished = pyqtSignal(bool, str)
#
#     def __init__(self, request_number, items_count, parent=None):
#         super().__init__(parent)
#         self.request_number = request_number
#         self.items_count = items_count
#         self.is_cancelled = False
#
#     def run(self):
#         try:
#             total_steps = self.items_count * 3 if self.items_count > 0 else 1
#             for i in range(total_steps):
#                 if self.is_cancelled:
#                     self.parsing_finished.emit(False, "Парсинг отменён пользователем")
#                     return
#
#                 percent = int((i + 1) / total_steps * 100)
#                 status = f"Обработка товара {i // 3 + 1} из {self.items_count}..."
#                 self.progress_updated.emit(percent, status)
#                 self.msleep(300)  # Немного уменьшил задержку для плавности
#
#             self.parsing_finished.emit(True, f"Найдено товаров: {self.items_count * 5}")
#         except Exception as e:
#             self.parsing_finished.emit(False, f"Ошибка парсинга: {str(e)}")
#
#     def cancel(self):
#         self.is_cancelled = True
#
#
# class ParsingProgressDialog(QDialog):
#     """Диалог отображения прогресса парсинга"""
#
#     def __init__(self, request_number, items_count, request_date, parent=None):
#         super().__init__(parent)
#         self.request_number = str(request_number)  # ✅ Гарантируем, что это строка
#         self.items_count = int(items_count)        # ✅ Гарантируем, что это число
#         self.request_date = str(request_date)      # ✅ Гарантируем, что это строка
#         self.worker = None
#
#         self.setWindowTitle("Обработка заявки")
#         self.setFixedSize(600, 350)
#         self.setModal(True)
#
#         self.create_widgets()
#         self.apply_styles()
#         # ❌ УДАЛИТЕ self.start_parsing() отсюда!
#
#     def showEvent(self, event):
#         """Запускаем парсинг только после того, как окно полностью отображено"""
#         super().showEvent(event)
#         if event.type() == QEvent.Type.Show and self.worker is None:
#             self.start_parsing()
#
#     def create_widgets(self):
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
#         layout.setSpacing(Spacing.LG)
#
#         header = QHBoxLayout()
#         header.setSpacing(Spacing.SM)
#
#         self.status_icon = create_icon_label(IconNames.STATS, size=48)
#         header.addWidget(self.status_icon)
#
#         title = QLabel("Поиск товаров на маркетплейсах")
#         title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_HEADING, QFont.Weight.Bold))
#         title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
#         header.addWidget(title)
#         header.addStretch()
#         layout.addLayout(header)
#
#         # ✅ Безопасное форматирование номера
#         formatted_number = self.request_number.zfill(3)
#         description = QLabel(f"Заявка №{formatted_number} от {self.request_date}")
#         description.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
#         description.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
#         layout.addWidget(description)
#
#         layout.addSpacing(Spacing.LG)
#
#         self.progress_bar = QProgressBar()
#         self.progress_bar.setRange(0, 100)
#         self.progress_bar.setValue(0)
#         self.progress_bar.setFixedHeight(30)
#         self.progress_bar.setTextVisible(True)
#         self.progress_bar.setObjectName("progressBar")
#         layout.addWidget(self.progress_bar)
#
#         self.status_label = QLabel("Инициализация парсинга...")
#         self.status_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
#         self.status_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
#         self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.status_label)
#
#         layout.addStretch()
#
#         self.cancel_btn = QPushButton("Отменить")
#         self.cancel_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
#         self.cancel_btn.setFixedSize(150, Sizes.BUTTON_HEIGHT)
#         self.cancel_btn.setObjectName("cancelButton")
#         self.cancel_btn.clicked.connect(self.cancel_parsing)
#
#         cancel_layout = QHBoxLayout()
#         cancel_layout.addStretch()
#         cancel_layout.addWidget(self.cancel_btn)
#         cancel_layout.addStretch()
#         layout.addLayout(cancel_layout)
#
#     def start_parsing(self):
#         self.worker = ParsingWorker(self.request_number, self.items_count)
#         self.worker.progress_updated.connect(self.on_progress_updated)
#         self.worker.parsing_finished.connect(self.on_parsing_finished)
#         self.worker.start()
#
#     def on_progress_updated(self, percent, status):
#         self.progress_bar.setValue(percent)
#         self.status_label.setText(status)
#
#     def on_parsing_finished(self, success, message):
#         """Завершение парсинга"""
#         # ✅ 1. Ждем полного завершения потока перед закрытием
#         if self.worker and self.worker.isRunning():
#             self.worker.wait(1000)  # Ждем до 1 секунды
#
#         self.cancel_btn.setEnabled(False)
#
#         if success:
#             self.status_icon = create_icon_label(IconNames.SAVE, size=48)
#             self.status_label.setText(f"✅ {message}")
#             self.status_label.setStyleSheet(f"color: {Colors.SUCCESS};")
#             self.accept()
#         else:
#             self.status_label.setText(f"❌ {message}")
#             self.status_label.setStyleSheet(f"color: {Colors.DANGER};")
#             self.cancel_btn.setText("Закрыть")
#             self.cancel_btn.setEnabled(True)
#
#     def cancel_parsing(self):
#         if self.worker and self.worker.isRunning():
#             self.worker.cancel()
#             self.status_label.setText("Отмена парсинга...")
#
#     def closeEvent(self, event):
#         """Гарантированная очистка потока при закрытии окна"""
#         if self.worker and self.worker.isRunning():
#             self.worker.cancel()
#             self.worker.wait(1000)  # Принудительно ждем завершения
#         super().closeEvent(event)
#
#     def apply_styles(self):
#         styles = get_dialog_styles() + """
#             QProgressBar {
#                 background-color: #E5E7EB;
#                 border: 1px solid #D1D5DB;
#                 border-radius: 15px;
#                 text-align: center;
#                 color: #1F2937;
#             }
#             QProgressBar::chunk {
#                 background-color: #3B82F6;
#                 border-radius: 15px;
#             }
#         """
#         self.setStyleSheet(styles)
#
# # """
# # Диалог прогресса парсинга маркетплейсов
# # """
# # from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QProgressBar,
# #                              QPushButton, QFrame, QHBoxLayout)
# # from PyQt6.QtCore import Qt, pyqtSignal, QThread
# # from PyQt6.QtGui import QFont
# #
# # from ui.utils.config import Colors, Fonts, Spacing, Sizes
# # from ui.utils.icons import create_icon_label, IconNames
# # from ui.utils.styles import get_dialog_styles
# #
# #
# # class ParsingWorker(QThread):
# #     """Поток для парсинга (заглушка для демонстрации)"""
# #     progress_updated = pyqtSignal(int, str)  # (процент, статус)
# #     parsing_finished = pyqtSignal(bool, str)  # (успех, сообщение)
# #
# #     def __init__(self, request_number, items_count, parent=None):
# #         super().__init__(parent)
# #         self.request_number = request_number
# #         self.items_count = items_count
# #         self.is_cancelled = False
# #
# #     def run(self):
# #         """Симуляция парсинга (заменить на реальный парсер)"""
# #         try:
# #             total_steps = self.items_count * 3  # 3 маркетплейса на товар
# #             for i in range(total_steps):
# #                 if self.is_cancelled:
# #                     self.parsing_finished.emit(False, "Парсинг отменён пользователем")
# #                     return
# #
# #                 percent = int((i + 1) / total_steps * 100)
# #                 status = f"Обработка товара {i // 3 + 1} из {self.items_count}..."
# #                 self.progress_updated.emit(percent, status)
# #
# #                 # Симуляция задержки парсинга
# #                 self.msleep(500)  # 0.5 секунды на шаг
# #
# #             self.parsing_finished.emit(True, f"Найдено товаров: {self.items_count * 5}")
# #         except Exception as e:
# #             self.parsing_finished.emit(False, f"Ошибка парсинга: {str(e)}")
# #
# #     def cancel(self):
# #         self.is_cancelled = True
# #
# #
# # class ParsingProgressDialog(QDialog):
# #     """Диалог отображения прогресса парсинга"""
# #
# #     # ✅ ИСПРАВЛЕНО: первый аргумент теперь request_number
# #     def __init__(self, request_number, items_count, request_date, parent=None):
# #         super().__init__(parent)
# #         self.request_number = request_number  # ✅ ИСПРАВЛЕНО: сохраняем как request_number
# #         self.items_count = items_count
# #         self.request_date = request_date
# #         self.worker = None
# #
# #         self.setWindowTitle("Обработка заявки")
# #         self.setFixedSize(600, 350)
# #         self.setModal(True)
# #
# #         self.create_widgets()
# #         self.apply_styles()
# #         self.start_parsing()
# #
# #     def create_widgets(self):
# #         layout = QVBoxLayout(self)
# #         layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
# #         layout.setSpacing(Spacing.LG)
# #
# #         # Иконка и заголовок
# #         header = QHBoxLayout()
# #         header.setSpacing(Spacing.SM)
# #
# #         self.status_icon = create_icon_label(IconNames.STATS, size=48)
# #         header.addWidget(self.status_icon)
# #
# #         title = QLabel("Поиск товаров на маркетплейсах")
# #         title.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_HEADING, QFont.Weight.Bold))
# #         title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
# #         header.addWidget(title)
# #         header.addStretch()
# #
# #         layout.addLayout(header)
# #
# #         # ✅ Теперь self.request_number существует и работает корректно
# #         formatted_number = f"{self.request_number:03d}" if isinstance(self.request_number, int) else str(self.request_number).zfill(3)
# #
# #         # Описание с датой из БД
# #         description = QLabel(f"Заявка №{formatted_number} от {self.request_date}")
# #         description.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
# #         description.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
# #         layout.addWidget(description)
# #
# #         layout.addSpacing(Spacing.LG)
# #
# #         # Прогресс-бар
# #         self.progress_bar = QProgressBar()
# #         self.progress_bar.setRange(0, 100)
# #         self.progress_bar.setValue(0)
# #         self.progress_bar.setFixedHeight(30)
# #         self.progress_bar.setTextVisible(True)
# #         self.progress_bar.setObjectName("progressBar")
# #         layout.addWidget(self.progress_bar)
# #
# #         # Статус
# #         self.status_label = QLabel("Инициализация парсинга...")
# #         self.status_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
# #         self.status_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
# #         self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
# #         layout.addWidget(self.status_label)
# #
# #         layout.addStretch()
# #
# #         # Кнопка отмены
# #         self.cancel_btn = QPushButton("Отменить")
# #         self.cancel_btn.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
# #         self.cancel_btn.setFixedSize(150, Sizes.BUTTON_HEIGHT)
# #         self.cancel_btn.setObjectName("cancelButton")
# #         self.cancel_btn.clicked.connect(self.cancel_parsing)
# #
# #         cancel_layout = QHBoxLayout()
# #         cancel_layout.addStretch()
# #         cancel_layout.addWidget(self.cancel_btn)
# #         cancel_layout.addStretch()
# #
# #         layout.addLayout(cancel_layout)
# #
# #     def start_parsing(self):
# #         """Запуск парсинга в отдельном потоке"""
# #         self.worker = ParsingWorker(self.request_number, self.items_count)
# #         self.worker.progress_updated.connect(self.on_progress_updated)
# #         self.worker.parsing_finished.connect(self.on_parsing_finished)
# #         self.worker.start()
# #
# #     def on_progress_updated(self, percent, status):
# #         """Обновление прогресса"""
# #         self.progress_bar.setValue(percent)
# #         self.status_label.setText(status)
# #
# #     def on_parsing_finished(self, success, message):
# #         """Завершение парсинга"""
# #         self.cancel_btn.setEnabled(False)
# #
# #         if success:
# #             self.status_icon = create_icon_label(IconNames.SAVE, size=48)
# #             self.status_label.setText(f"✅ {message}")
# #             self.status_label.setStyleSheet(f"color: {Colors.SUCCESS};")
# #             self.accept()  # Закрываем диалог с успехом
# #         else:
# #             self.status_label.setText(f"❌ {message}")
# #             self.status_label.setStyleSheet(f"color: {Colors.DANGER};")
# #             self.cancel_btn.setText("Закрыть")
# #             self.cancel_btn.setEnabled(True)
# #
# #     def cancel_parsing(self):
# #         """Отмена парсинга"""
# #         if self.worker and self.worker.isRunning():
# #             self.worker.cancel()
# #             self.status_label.setText("Отмена парсинга...")
# #
# #     def apply_styles(self):
# #         styles = get_dialog_styles() + """
# #             QProgressBar {
# #                 background-color: #E5E7EB;
# #                 border: 1px solid #D1D5DB;
# #                 border-radius: 15px;
# #                 text-align: center;
# #                 color: #1F2937;
# #             }
# #             QProgressBar::chunk {
# #                 background-color: #3B82F6;
# #                 border-radius: 15px;
# #             }
# #         """
# #         self.setStyleSheet(styles)