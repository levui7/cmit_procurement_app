"""
Диалог прогресса парсинга маркетплейсов
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QProgressBar,
                             QPushButton, QFrame, QHBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont

from ui.utils.config import Colors, Fonts, Spacing, Sizes
from ui.utils.icons import create_icon_label, IconNames
from ui.utils.styles import get_dialog_styles


class ParsingWorker(QThread):
    """Поток для парсинга (заглушка для демонстрации)"""
    progress_updated = pyqtSignal(int, str)  # (процент, статус)
    parsing_finished = pyqtSignal(bool, str)  # (успех, сообщение)

    def __init__(self, request_id, items_count, parent=None):
        super().__init__(parent)
        self.request_id = request_id
        self.items_count = items_count
        self.is_cancelled = False

    def run(self):
        """Симуляция парсинга (заменить на реальный парсер)"""
        try:
            total_steps = self.items_count * 3  # 3 маркетплейса на товар
            for i in range(total_steps):
                if self.is_cancelled:
                    self.parsing_finished.emit(False, "Парсинг отменён пользователем")
                    return

                percent = int((i + 1) / total_steps * 100)
                status = f"Обработка товара {i // 3 + 1} из {self.items_count}..."
                self.progress_updated.emit(percent, status)

                # Симуляция задержки парсинга
                self.msleep(500)  # 0.5 секунды на шаг

            self.parsing_finished.emit(True, f"Найдено товаров: {self.items_count * 5}")
        except Exception as e:
            self.parsing_finished.emit(False, f"Ошибка парсинга: {str(e)}")

    def cancel(self):
        self.is_cancelled = True


class ParsingProgressDialog(QDialog):
    """Диалог отображения прогресса парсинга"""

    def __init__(self, request_id, items_count, parent=None):
        super().__init__(parent)
        self.request_id = request_id
        self.items_count = items_count
        self.worker = None

        self.setWindowTitle("Обработка заявки")
        self.setFixedSize(600, 350)
        self.setModal(True)

        self.create_widgets()
        self.apply_styles()
        self.start_parsing()

    def create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.XXL, Spacing.XL, Spacing.XXL, Spacing.XL)
        layout.setSpacing(Spacing.LG)

        # Иконка и заголовок
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

        # Описание
        description = QLabel(f"Заявка #{self.request_id} • {self.items_count} товаров • Ozon, Wildberries, Яндекс.Маркет")
        description.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_NORMAL))
        description.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(description)

        layout.addSpacing(Spacing.LG)

        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setObjectName("progressBar")
        layout.addWidget(self.progress_bar)

        # Статус
        self.status_label = QLabel("Инициализация парсинга...")
        self.status_label.setFont(QFont(Fonts.FAMILY, Fonts.SIZE_SMALL))
        self.status_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addStretch()

        # Кнопка отмены
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
        """Запуск парсинга в отдельном потоке"""
        self.worker = ParsingWorker(self.request_id, self.items_count)
        self.worker.progress_updated.connect(self.on_progress_updated)
        self.worker.parsing_finished.connect(self.on_parsing_finished)
        self.worker.start()

    def on_progress_updated(self, percent, status):
        """Обновление прогресса"""
        self.progress_bar.setValue(percent)
        self.status_label.setText(status)

    def on_parsing_finished(self, success, message):
        """Завершение парсинга"""
        self.cancel_btn.setEnabled(False)

        if success:
            self.status_icon = create_icon_label(IconNames.SAVE, size=48)
            self.status_label.setText(f"✅ {message}")
            self.status_label.setStyleSheet(f"color: {Colors.SUCCESS};")
            self.accept()  # Закрываем диалог с успехом
        else:
            self.status_label.setText(f" {message}")
            self.status_label.setStyleSheet(f"color: {Colors.DANGER};")
            self.cancel_btn.setText("Закрыть")
            self.cancel_btn.setEnabled(True)

    def cancel_parsing(self):
        """Отмена парсинга"""
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