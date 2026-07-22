"""
CRUD-операции для заявок на закупку
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.models.models_procurement import ProcurementRequest, ProcurementItem
from typing import List, Optional, Dict, Tuple


# ========== ЗАЯВКИ (PROCUREMENT REQUESTS) ==========

def create_procurement_request(
        db: Session,
        description: str = "",
        students_count: int = 0,
        delivery_date: str = "",
        min_rating: str = "4.0",
        min_price: float = None,
        max_price: float = None,
        status: str = "new"
) -> ProcurementRequest:
    """
    Создать новую заявку на закупку

    Returns:
        Созданный объект ProcurementRequest
    """
    # Генерируем номер заявки
    number = generate_request_number(db)

    request = ProcurementRequest(
        number=number,
        description=description,
        students_count=students_count,
        delivery_date=delivery_date,
        min_rating=min_rating,
        min_price=min_price,
        max_price=max_price,
        status=status
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def get_all_requests(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: str = None
) -> List[ProcurementRequest]:
    """
    Получить все заявки

    Args:
        db: Сессия БД
        skip: Пропустить N записей (для пагинации)
        limit: Максимальное количество записей
        status: Фильтр по статусу (опционально)

    Returns:
        Список заявок, отсортированный по дате создания (новые сначала)
    """
    query = db.query(ProcurementRequest)

    if status:
        query = query.filter(ProcurementRequest.status == status)

    return query.order_by(desc(ProcurementRequest.created_at)).offset(skip).limit(limit).all()


def get_request_by_id(db: Session, request_id: int) -> Optional[ProcurementRequest]:
    """Получить заявку по ID"""
    return db.query(ProcurementRequest).filter(ProcurementRequest.id == request_id).first()


def get_request_by_number(db: Session, number: str) -> Optional[ProcurementRequest]:
    """Получить заявку по номеру"""
    return db.query(ProcurementRequest).filter(ProcurementRequest.number == number).first()


def update_request(
        db: Session,
        request_id: int,
        **kwargs
) -> bool:
    """
    Обновить заявку

    Args:
        db: Сессия БД
        request_id: ID заявки
        **kwargs: Поля для обновления

    Returns:
        True если успешно, False если заявка не найдена
    """
    request = get_request_by_id(db, request_id)
    if not request:
        return False

    for key, value in kwargs.items():
        if hasattr(request, key):
            setattr(request, key, value)

    db.commit()
    db.refresh(request)
    return True


def delete_request(db: Session, request_id: int) -> bool:
    """
    Удалить заявку (вместе со всеми позициями)

    Returns:
        True если успешно, False если заявка не найдена
    """
    request = get_request_by_id(db, request_id)
    if not request:
        return False

    db.delete(request)
    db.commit()
    return True


def update_request_status(
        db: Session,
        request_id: int,
        status: str
) -> bool:
    """
    Обновить статус заявки

    Args:
        status: new, in_progress, completed, cancelled
    """
    return update_request(db, request_id, status=status)


def calculate_total_amount(db: Session, request_id: int) -> float:
    """
    Подсчитать общую сумму заявки на основе выбранных товаров

    Returns:
        Общая сумма в рублях
    """
    items = get_items_by_request(db, request_id)
    total = 0.0

    for item in items:
        if item.selected_marketplace_id and item.best_price:
            total += item.best_price * item.quantity

    # Обновляем поле total_amount в заявке
    update_request(db, request_id, total_amount=total)

    return total


# ========== ПОЗИЦИИ ЗАЯВКИ (PROCUREMENT ITEMS) ==========

def add_item_to_request(
        db: Session,
        request_id: int,
        internal_product_id: int,
        quantity: int = 1,
        min_price: float = 0.0,
        max_price: float = 0.0
) -> ProcurementItem:
    """
    Добавить позицию товара в заявку

    Returns:
        Созданный объект ProcurementItem
    """
    item = ProcurementItem(
        request_id=request_id,
        internal_product_id=internal_product_id,
        quantity=quantity,
        min_price=min_price,
        max_price=max_price
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_items_by_request(db: Session, request_id: int) -> List[ProcurementItem]:
    """Получить все позиции заявки"""
    return db.query(ProcurementItem).filter(ProcurementItem.request_id == request_id).all()


def get_item_by_id(db: Session, item_id: int) -> Optional[ProcurementItem]:
    """Получить позицию по ID"""
    return db.query(ProcurementItem).filter(ProcurementItem.id == item_id).first()


def update_item(
        db: Session,
        item_id: int,
        **kwargs
) -> bool:
    """
    Обновить позицию товара в заявке

    Returns:
        True если успешно, False если позиция не найдена
    """
    item = get_item_by_id(db, item_id)
    if not item:
        return False

    for key, value in kwargs.items():
        if hasattr(item, key):
            setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return True


def delete_item(db: Session, item_id: int) -> bool:
    """
    Удалить позицию из заявки

    Returns:
        True если успешно, False если позиция не найдена
    """
    item = get_item_by_id(db, item_id)
    if not item:
        return False

    db.delete(item)
    db.commit()
    return True


def clear_request_items(db: Session, request_id: int) -> int:
    """
    Удалить все позиции из заявки

    Returns:
        Количество удаленных позиций
    """
    items = get_items_by_request(db, request_id)
    count = len(items)

    for item in items:
        db.delete(item)

    db.commit()
    return count


# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

def generate_request_number(db: Session) -> str:
    """
    Сгенерировать следующий номер заявки

    Формат: 001, 002, 003, ...
    """
    last_request = db.query(ProcurementRequest).order_by(desc(ProcurementRequest.id)).first()

    if last_request:
        try:
            last_number = int(last_request.number)
            new_number = f"{last_number + 1:03d}"
        except (ValueError, AttributeError):
            new_number = "001"
    else:
        new_number = "001"

    return new_number


def get_requests_count(db: Session, status: str = None) -> int:
    """Получить количество заявок"""
    query = db.query(ProcurementRequest)

    if status:
        query = query.filter(ProcurementRequest.status == status)

    return query.count()


def get_items_count_by_request(db: Session, request_id: int) -> int:
    """Получить количество позиций в заявке"""
    return db.query(ProcurementItem).filter(ProcurementItem.request_id == request_id).count()


def create_procurement_with_items(
        request_data: dict,
        items_data: list
) -> Tuple[Optional[int], Optional[str]]:
    """
    Создать заявку вместе с позициями товаров.

    Args:
        request_data: dict с полями:
            - description: str
            - delivery_date: str
            - min_rating: str
            - students_count: int
        items_data: список словарей вида:
            [
                {'internal_product_id': 1, 'quantity': 100, 'min_price': 10.0, 'max_price': 50.0},
                ...
            ]

    Returns:
        (request_id, request_number) или (None, None) при ошибке
    """
    from backend.database import get_session

    db = get_session()
    try:
        # Генерируем номер заявки
        last_request = db.query(ProcurementRequest).order_by(
            desc(ProcurementRequest.id)
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
        print(f" Ошибка создания заявки: {e}")
        return None, None
    finally:
        db.close()


def delete_procurement_request(db: Session, request_id: int) -> bool:
    """
    Удалить заявку и все связанные позиции
    """
    try:
        # Находим заявку
        request = db.query(ProcurementRequest).filter(ProcurementRequest.id == request_id).first()

        if not request:
            return False

        # Удаляем заявку (каскадное удаление позиций благодаря cascade="all, delete-orphan")
        db.delete(request)
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка удаления заявки: {e}")
        return False