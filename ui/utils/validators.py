"""
Валидация данных
"""
from typing import Optional, Tuple


def validate_product_name(name: str) -> Tuple[bool, str]:
    """
    Проверить название товара

    Returns:
        (успех, сообщение)
    """
    if not name or not name.strip():
        return False, "Название товара обязательно"

    if len(name.strip()) < 3:
        return False, "Название должно содержать минимум 3 символа"

    if len(name.strip()) > 200:
        return False, "Название слишком длинное (макс. 200 символов)"

    return True, ""


def validate_price(price: float, min_price: float = 0) -> Tuple[bool, str]:
    """Проверить цену"""
    if price < min_price:
        return False, f"Цена не может быть меньше {min_price}"

    if price > 10_000_000:
        return False, "Цена слишком большая"

    return True, ""


def validate_quantity(qty: int) -> Tuple[bool, str]:
    """Проверить количество"""
    if qty < 1:
        return False, "Количество должно быть больше 0"

    if qty > 100000:
        return False, "Количество слишком большое"

    return True, ""