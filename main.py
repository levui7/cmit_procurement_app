"""
Точка входа в приложение
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui.app_window import AppWindow

from backend.database import init_db, seed_test_data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    # Инициализация БД
    init_db()
    seed_test_data()  # Заполняем тестовыми данными

    window = AppWindow()
    window.show()

    sys.exit(app.exec())