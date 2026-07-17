from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from ui.utils.styles import get_about_styles


class AboutCompanyPage(QWidget):
    def __init__(self, icons_path, parent=None):
        super().__init__(parent)
        self.icons_path = icons_path
        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        """Создание элементов интерфейса"""

        # Основной контент (справа от sidebar)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(30)

        # Заголовок страницы
        title = QLabel("О предприятии ЦМИТ ЛЮКС")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #1F2937;")

        subtitle = QLabel("Малое инновационное предприятие "
                          "\nЦентр Молодежного Инновационного Творчества "
                          "\nЛаборатория Юных Конструкторов")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #6B7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)

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

        layout.addWidget(info_card)
        layout.addStretch()


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

    def apply_styles(self):
        self.setStyleSheet(get_about_styles())


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     app.setFont(QFont("Segoe UI", 10))
#
#     from PyQt6.QtWidgets import QMainWindow
#
#     window = QMainWindow()
#     window.setWindowTitle("Тест: О предприятии")
#     window.setGeometry(100, 100, 1400, 900)
#
#     icons_path = Path(__file__).parent.parent / "icons"
#     page = AboutCompanyPage(icons_path)
#     window.setCentralWidget(page)
#
#     window.show()
#     sys.exit(app.exec())