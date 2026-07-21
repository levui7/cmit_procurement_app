"""
CRUD-операции для внутреннего каталога товаров
"""
from sqlalchemy.orm import Session
from backend.models.models_internal_product import InternalProduct
from typing import List, Optional


def create_internal_product(
        db: Session,
        internal_code: str,
        name: str,
        # category: str,
        damage_percent: float = 0.0,
        keywords: str = ""
) -> InternalProduct:
    """Добавить товар во внутренний каталог"""
    product = InternalProduct(
        internal_code=internal_code,
        name=name,
        # category=category,
        damage_percent=damage_percent,
        keywords=keywords
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_all_internal_products(db: Session) -> List[InternalProduct]:
    """Получить все товары внутреннего каталога"""
    return db.query(InternalProduct).all()


def search_internal_products(
        db: Session,
        query: str
) -> List[InternalProduct]:
    """Поиск товаров по названию, коду или ключевым словам"""
    search_term = f"%{query}%"
    return db.query(InternalProduct).filter(
        (InternalProduct.name.like(search_term)) |
        (InternalProduct.internal_code.like(search_term)) |
        (InternalProduct.keywords.like(search_term))
    ).all()


def get_internal_product(
        db: Session,
        product_id: int
) -> Optional[InternalProduct]:
    """Получить товар по ID"""
    return db.query(InternalProduct).filter(InternalProduct.id == product_id).first()

def get_internal_product_by_code(db: Session, code: str) -> Optional[InternalProduct]:
    """
    Получить товар по внутреннему коду (internal_code)
    """
    return db.query(InternalProduct).filter(InternalProduct.internal_code == code).first()

def update_internal_product(
        db: Session,
        product_id: int,
        **kwargs
) -> bool:
    """Обновить товар внутреннего каталога"""
    product = db.query(InternalProduct).filter(InternalProduct.id == product_id).first()
    if not product:
        return False

    for key, value in kwargs.items():
        if hasattr(product, key):
            setattr(product, key, value)

    db.commit()
    return True


def delete_internal_product(
        db: Session,
        product_id: int
) -> bool:
    """Удалить товар из внутреннего каталога"""
    product = db.query(InternalProduct).filter(InternalProduct.id == product_id).first()
    if not product:
        return False

    db.delete(product)
    db.commit()
    return True


def get_next_internal_code(db: Session) -> str:
    """
    Получить следующий доступный внутренний код.
    Автоматически определяет максимальный номер INT-XXX и возвращает следующий.
    """
    # Получаем все товары, у которых есть internal_code, начинающийся с "INT-"
    products = db.query(InternalProduct).filter(
        InternalProduct.internal_code.like('INT-%')
    ).all()

    if not products:
        return "INT-001"

    # Извлекаем числовые части из кодов
    numbers = []
    for product in products:
        try:
            # Убираем "INT-" и преобразуем в число
            code_num = int(product.internal_code.replace("INT-", ""))
            numbers.append(code_num)
        except (ValueError, AttributeError):
            continue

    # Если нашли числа, берём максимальное + 1
    if numbers:
        next_num = max(numbers) + 1
        return f"INT-{next_num:03d}"  # Формат: INT-001, INT-016, INT-100 и т.д.
    else:
        return "INT-001"