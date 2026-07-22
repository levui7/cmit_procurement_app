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
    """Поток для реального парсинга"""
    progress_updated = pyqtSignal(int, str)
    parsing_finished = pyqtSignal(bool, str)

    def __init__(self, request_id, request_number, items_count, parent=None):
        super().__init__(parent)
        self.request_id = request_id          # ID заявки для парсера
        self.request_number = request_number
        self.items_count = items_count
        self.is_cancelled = False

    def run(self):
        try:
            self.progress_updated.emit(10, "Подключение к маркетплейсам...")
            
            # Импортируем сервис внутри потока, чтобы не блокировать основной интерфейс при старте
            from backend.services.request_parser_service import run_parsing_for_request
            
            self.progress_updated.emit(30, "Запуск поиска товаров (это может занять время)...")
            
            # Вызываем реальный парсер, который сам пройдет по всем товарам заявки
            success = run_parsing_for_request(self.request_id)
            
            # Проверяем, не отменил ли пользователь процесс во время парсинга
            if self.is_cancelled:
                self.parsing_finished.emit(False, "Парсинг отменён пользователем")
                return

            if success:
                self.progress_updated.emit(100, "Обработка завершена!")
                self.parsing_finished.emit(True, "Товары успешно найдены и сохранены в базу данных")
            else:
                self.parsing_finished.emit(False, "Ошибка при парсинге или заявка пуста")
                
        except Exception as e:
            self.parsing_finished.emit(False, f"Критическая ошибка парсинга: {str(e)}")

    def cancel(self):
        self.is_cancelled = True


class ParsingProgressDialog(QDialog):
    """Диалог отображения прогресса парсинга"""

    def __init__(self, request_id, request_number, items_count, request_date, parent=None):
        super().__init__(parent)
        self.request_id = request_id          # <-- ДОБАВЛЕНО: сохраняем ID заявки
        self.request_number = str(request_number)
        self.items_count = int(items_count)
        self.request_date = str(request_date)
        self.worker = None

        self.setWindowTitle("Обработка заявки")
        self.setFixedSize(600, 350)
        self.setModal(True)

        self.create_widgets()
        self.apply_styles()

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
        # Передаем request_id первым аргументом в рабочий поток
        self.worker = ParsingWorker(self.request_id, self.request_number, self.items_count)
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