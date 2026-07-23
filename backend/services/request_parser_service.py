"""
Сервис для запуска пакетного парсинга по всем товарам в заявке
"""
from backend.database import get_session
from backend.models import ProcurementItem, InternalProduct
from parser.parser_service import search_and_save_to_db


def run_parsing_for_request(request_id: int):
    """
    Проходит по всем позициям заявки и запускает для них парсинг.
    Возвращает True при успехе, False при ошибке.
    """
    db = get_session()
    try:
        items = db.query(ProcurementItem).filter(
            ProcurementItem.request_id == request_id
        ).all()
        
        if not items:
            print(f"Заявка #{request_id} пуста.")
            return False
            
        print(f"Запуск парсинга для {len(items)} позиций заявки #{request_id}")
        
        for item in items:
            product = db.query(InternalProduct).filter(
                InternalProduct.id == item.internal_product_id
            ).first()
            
            if product:
                query = product.keywords if product.keywords else product.name
                print(f"Ищем: '{query}' (ID: {product.id})")
                
                # OZON
                print("   -> Ozon...")
                search_and_save_to_db(query=query, internal_product_id=product.id, marketplace="ozon")
                
                # WILDBERRIES
                print("   -> Wildberries...")
                search_and_save_to_db(query=query, internal_product_id=product.id, marketplace="wb")
                
                # ALIEXPRESS
                print("   -> AliExpress...")
                search_and_save_to_db(query=query, internal_product_id=product.id, marketplace="ali")
                
        print(f"Парсинг для заявки #{request_id} завершен")
        return True
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    finally:
        db.close()