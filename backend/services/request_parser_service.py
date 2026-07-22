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
        # 1. Получаем все товары, добавленные в эту заявку
        items = db.query(ProcurementItem).filter(
            ProcurementItem.request_id == request_id
        ).all()
        
        if not items:
            print(f" Заявка #{request_id} пуста. Парсинг не требуется.")
            return False
            
        print(f" Запуск парсинга для {len(items)} позиций заявки #{request_id}")
        
        # 2. Для каждого товара находим его название/ключевые слова и парсим
        for item in items:
            product = db.query(InternalProduct).filter(
                InternalProduct.id == item.internal_product_id
            ).first()
            
            if product:
                # Используем ключевые слова, если есть, иначе берем название
                query = product.keywords if product.keywords else product.name
                print(f"Ищем: '{query}' (Внутренний ID: {product.id})")
                
                # Вызываем твой работающий парсер!
                search_and_save_to_db(
                    query=query,
                    internal_product_id=product.id,
                    marketplace="ozon"
                )
                
        print(f"Парсинг для заявки #{request_id} успешно завершен")
        return True
        
    except Exception as e:
        print(f"Критическая ошибка при парсинге заявки #{request_id}: {e}")
        return False
    finally:
        db.close()