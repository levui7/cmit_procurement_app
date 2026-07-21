"""
Сервис для создания заявок с позициями
"""
from sqlalchemy.orm import Session
from backend.models.models_procurement import ProcurementRequest, ProcurementItem
from backend.crud import crud_internal_product, crud_procurement
from typing import List, Dict, Tuple, Optional


def create_procurement_with_items(
        db: Session,
        request_data: Dict,
        items_data: List[Dict]
) -> Tuple[Optional[int], Optional[str]]:
    """
    Создать заявку вместе с позициями товаров.

    Args:
        db: Сессия БД
        request_data: dict с общими полями
        items_data: список словарей с данными о позициях

    Returns:
        (request_id, request_number) или (None, None) при ошибке
    """
    try:
        # Генерируем номер заявки
        last_request = db.query(ProcurementRequest).order_by(
            ProcurementRequest.id.desc()
        ).first()
        new_number = f"{int(last_request.number) + 1:03d}" if last_request else "001"

        # Создаём заявку
        request = ProcurementRequest(
            number=new_number,
            description=request_data.get("description", ""),
            students_count=request_data.get("students_count", 0),
            delivery_date=request_data.get("delivery_date", ""),
            min_rating=request_data.get("min_rating", "4.0"),
            status="new"
        )
        db.add(request)
        db.flush()  # Чтобы получить request.id до commit

        # Создаём позиции
        for item in items_data:
            proc_item = ProcurementItem(
                request_id=request.id,
                internal_product_id=item['internal_product_id'],
                quantity=item.get('quantity', 1),
                min_price=item.get('min_price', 0.0),
                max_price=item.get('max_price', 0.0)
            )
            db.add(proc_item)

        db.commit()
        return request.id, new_number
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка создания заявки: {e}")
        return None, None