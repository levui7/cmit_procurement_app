# """
# Точка входа в приложение
# """
# import sys
# from PyQt6.QtWidgets import QApplication
# from PyQt6.QtGui import QFont
# from ui.utils.app_window import AppWindow
#
# from backend.database import init_db, seed_test_data
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     app.setFont(QFont("Segoe UI", 10))
#
#     # Инициализация БД
#     init_db()
#     seed_test_data()  # Заполняем тестовыми данными
#
#     window = AppWindow()
#     window.show()
#
#     sys.exit(app.exec())

"""
Точка входа в приложение
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

# Импорты из твоего проекта (проверь пути, если ты перемещал файлы)
from ui.utils.app_window import AppWindow  # Или from ui.utils.app_window import AppWindow
from backend.database import init_db, get_session
from backend.services.test_data import seed_test_data  # Укажи правильный путь к твоему файлу с seed_test_data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    from backend.models import (
        InternalProduct,
        MarketplaceProduct,
        ProcurementRequest,
        ProcurementItem,
        AppSettings
    )

    # 1. Инициализация БД (создаст таблицы, если их нет)
    init_db()

    # 2. Заполнение тестовыми данными (если база пустая)
    db = get_session()
    try:
        seed_test_data(db)
    finally:
        db.close()

    # 3. Запуск главного окна
    window = AppWindow()
    window.show()

    sys.exit(app.exec())