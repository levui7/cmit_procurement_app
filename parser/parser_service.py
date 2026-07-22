import json
import sys
from pathlib import Path

# Добавляем корень проекта в путь, чтобы работали импорты из backend
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.database import get_session, add_marketplace_match
from .ozon_parse import run_ozon_parser

def search_and_save_to_db(query: str, internal_product_id: int, marketplace: str = "ozon"):
    """
    Выполняет парсинг по запросу и сохраняет результаты в БД.
    """
    if marketplace == "ozon":
        success = run_ozon_parser(query)
        if not success:
            return False
        
        BASE_DIR = Path(__file__).parent.resolve()
        normalized_file = BASE_DIR / "normalized" / "products_ozon.json"
        
        if not normalized_file.exists():
            print(" Файл с нормализованными данными не найден.")
            return False
        
        # Теперь json определен, так как мы добавили import json в начало файла
        with open(normalized_file, "r", encoding="utf-8") as f:
            products = json.load(f)
        
        db = get_session()
        try:
            count = 0
            # Ограничиваем 10 топ результатами для скорости интерфейса
            for product in products[:10]: 
                add_marketplace_match(
                    internal_product_id=internal_product_id,
                    marketplace_name="Ozon",
                    name=product.get("name", "Без названия"),
                    url=product.get("link", ""),
                    price=float(product.get("price", 0) or 0),
                    rating=float(product.get("rating", 0) or 0)
                )
                count += 1
            
            print(f"Успешно сохранено {count} товаров в БД для запроса '{query}'")
            return True
        except Exception as e:
            print(f"Ошибка сохранения в БД: {e}")
            return False
        finally:
            db.close()
    else:
        print(f" Маркетплейс {marketplace} пока не поддерживается.")
        return False