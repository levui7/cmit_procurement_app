"""
Сервис для получения отформатированных результатов парсинга для UI
Читает спаршенные данные из БД и возвращает их в формате,
"""
from backend.database import get_session
from backend.models import ProcurementItem, InternalProduct, MarketplaceProduct


def get_parsed_results_for_ui(request_id: int):
    """
    Читает спаршенные данные из БД и форматирует их в структуру, 
    которую ожидает интерфейс (search_results.py).
    
    Args:
        request_id: ID заявки, для которой нужно получить результаты
        
    Returns:
        Список словарей с данными о товарах и их вариантах на маркетплейсах
    """
    db = get_session()
    results = []
    
    try:
        # 1. Получаем все позиции конкретной заявки
        items = db.query(ProcurementItem).filter(
            ProcurementItem.request_id == request_id
        ).all()
        
        for item in items:
            # 2. Получаем внутреннее название товара (чтобы показать пользователю)
            internal_product = db.query(InternalProduct).filter(
                InternalProduct.id == item.internal_product_id
            ).first()
            
            if not internal_product:
                continue
            
            # 3. Получаем все спаршенные варианты для этого товара из БД
            # Сортируем по цене, чтобы самый дешевый был первым
            matches = db.query(MarketplaceProduct).filter(
                MarketplaceProduct.internal_product_id == item.internal_product_id
            ).order_by(MarketplaceProduct.price.asc()).all()
            
            if matches:
                variants = []
                for match in matches:
                    variants.append({
                        'marketplace': match.marketplace_name,
                        'name': match.name,
                        'price': float(match.price),
                        'rating': float(match.rating),
                        'url': match.url,
                        'reviews_count': 0  # Пока 0, так как в текущей модели БД этого поля нет
                    })
                
                # Формируем блок в точности как в _get_mock_results() интерфейса
                results.append({
                    'internal_product_id': item.internal_product_id,
                    'product_name': internal_product.name,
                    'variants': variants
                })
        
        return results
        
    except Exception as e:
        print(f"Ошибка получения результатов для UI: {e}")
        return []
    finally:
        db.close()