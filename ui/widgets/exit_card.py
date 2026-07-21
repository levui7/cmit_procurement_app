"""
Мини-карточка выхода из приложения
"""
from pathlib import Path
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QDialog, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

from ui.utils.icons import create_icon_label, IconNames
from ui.utils.styles import get_dialog_styles


class ExitCard(QFrame):
    """
    Мини-карточка выхода в правом нижнем углу

    Сигналы:
        exit_requested: Вызывается при подтверждении выхода
    """

    exit_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._apply_styles()
        self._setup_signals()

    def _setup_ui(self):
        """Создание интерфейса карточки"""
        self.setObjectName("exitCard")
        self.setFixedSize(220, 90)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Нажмите для выхода из приложения")

        # Главный layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Иконка с розовым фоном
        icon_container = QFrame()
        icon_container.setFixedSize(50, 50)
        icon_container.setStyleSheet("""
            background-color: #FEE2E2;
            border-radius: 10px;
        """)

        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        # Иконка двери
        icon_label = create_icon_label(IconNames.DOOR, size=30)
        icon_layout.addWidget(icon_label)

        layout.addWidget(icon_container)

        # Текст
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)

        title_label = QLabel("Выход")
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1F2937;")

        text_layout.addWidget(title_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        # Стрелка
        arrow = QLabel("→")
        arrow.setFont(QFont("Segoe UI", 18))
        arrow.setStyleSheet("color: #9CA3AF;")
        layout.addWidget(arrow)

    def _apply_styles(self):
        """Применение стилей"""
        # Стили применяются через главный файл styles.py
        # Здесь только дополнительные стили для самой карточки
        self.setStyleSheet("""
            #exitCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }

            #exitCard:hover {
                border: 2px solid #EF4444;
                background-color: #FFFFFF;
            }
        """)

    def _setup_signals(self):
        """Настройка обработчиков событий"""
        # Обработка клика по карточке
        self.mousePressEvent = self._on_click

    def _on_click(self, event):
        """Обработчик клика по карточке"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._show_exit_confirmation()

    def _show_exit_confirmation(self):
        """Показать диалог подтверждения выхода"""
        dialog = ExitConfirmationDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.exit_requested.emit()
            QApplication.instance().quit()


class ExitConfirmationDialog(QDialog):
    """
    Диалог подтверждения выхода из приложения
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Создание интерфейса диалога"""
        self.setWindowTitle("Выход из приложения")
        self.setFixedSize(450, 220)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        # Иконка предупреждения
        icon_label = create_icon_label(IconNames.WARNING, size=50)
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Заголовок
        title_label = QLabel("Вы точно хотите уйти?")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Подтекст
        subtitle_label = QLabel("Возможно, остались незавершенные дела")
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setStyleSheet("color: #6B7280;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)

        layout.addSpacing(10)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setFont(QFont("Segoe UI", 12))
        cancel_btn.setFixedSize(150, 45)
        cancel_btn.setObjectName("cancelButton")
        cancel_btn.clicked.connect(self.reject)

        exit_btn = QPushButton("Выйти")
        exit_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        exit_btn.setFixedSize(150, 45)
        exit_btn.setObjectName("dangerButton")
        exit_btn.clicked.connect(self.accept)

        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(exit_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

    def _apply_styles(self):
        """Применение стилей диалога"""
        self.setStyleSheet(get_dialog_styles(theme="light"))

# """
# Общая кнопка выхода для всех страниц
# """
# from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QDialog, QPushButton
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont, QPixmap, QIcon
# from PyQt6.QtWidgets import QApplication
#
#
# class ExitCard(QFrame):
#     """Мини-карточка выхода"""
#
#     def __init__(self, icons_path, parent=None):
#         super().__init__(parent)
#         self.icons_path = icons_path
#
#         self.setObjectName("exitCard")
#         self.setFixedSize(180, 70)
#         self.setCursor(Qt.CursorShape.PointingHandCursor)
#
#         self._create_ui()
#         self._connect_signals()
#
#     def _create_ui(self):
#         layout = QHBoxLayout(self)
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
#         icon_layout.addWidget(self._create_icon_label("door.png", size=25))
#
#         # Текст
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
#     def _create_icon_label(self, filename, size=24):
#         label = QLabel()
#         icon_path = self.icons_path / filename
#
#         if icon_path.exists():
#             pixmap = QPixmap(str(icon_path))
#             scaled_pixmap = pixmap.scaled(size, size,
#                                           Qt.AspectRatioMode.KeepAspectRatio,
#                                           Qt.TransformationMode.SmoothTransformation)
#             label.setPixmap(scaled_pixmap)
#
#         label.setFixedSize(size, size)
#         return label
#
#     def _connect_signals(self):
#         self.mousePressEvent = lambda event: self._show_exit_confirmation()
#
#     def _show_exit_confirmation(self):
#         """Показать окно подтверждения выхода"""
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Выход из приложения")
#         dialog.setFixedSize(450, 220)
#
#         # Пытаемся взять иконку у главного окна
#         parent = self.parent()
#         while parent is not None:
#             if hasattr(parent, 'windowIcon'):
#                 dialog.setWindowIcon(parent.windowIcon())
#                 break
#             parent = parent.parent()
#
#         layout = QVBoxLayout(dialog)
#         layout.setContentsMargins(40, 30, 40, 30)
#         layout.setSpacing(15)
#
#         icon_label = self._create_icon_label("warning.png", size=50)
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
#         exit_btn.clicked.connect(lambda: self._confirm_exit(dialog))
#
#         buttons_layout.addStretch()
#         buttons_layout.addWidget(cancel_btn)
#         buttons_layout.addWidget(exit_btn)
#         buttons_layout.addStretch()
#
#         layout.addLayout(buttons_layout)
#         dialog.exec()
#
#     def _confirm_exit(self, dialog):
#         """Подтверждение выхода"""
#         dialog.accept()
#         QApplication.instance().quit()