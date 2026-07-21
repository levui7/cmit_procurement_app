"""
Реестр всех моделей базы данных.
Импорт этого модуля регистрирует все модели в SQLAlchemy.
"""
from .models_base import Base

# Импортируем все модели (порядок важен для зависимостей)
from .models_internal_product import InternalProduct
from .models_procurement import ProcurementRequest, ProcurementItem, procurement_item_matches
from .models_marketplace_product import MarketplaceProduct
from .models_settings import AppSettings  # ✅ ДОБАВЛЕНО

# Экспортируем всё для удобства
__all__ = [
    'Base',
    'InternalProduct',
    'MarketplaceProduct',
    'ProcurementRequest',
    'ProcurementItem',
    'procurement_item_matches',
    'AppSettings',
]