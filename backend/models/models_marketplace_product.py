"""
Модель товаров, найденных на маркетплейсах
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .models_base import Base

# ✅ Импортируем уже существующую таблицу вместо создания новой
from .models_procurement import procurement_item_matches


class MarketplaceProduct(Base):
    """Товар, найденный на маркетплейсе (Ozon, Wildberries, Яндекс.Маркет и т.д.)"""
    __tablename__ = "marketplace_products"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Связь с внутренним каталогом
    internal_product_id = Column(
        Integer,
        ForeignKey("internal_products.id", ondelete="CASCADE"),
        nullable=False
    )

    # Информация о маркетплейсе
    marketplace_name = Column(String(50), nullable=False)
    marketplace_url = Column(String(500))

    # Информация о товаре
    name = Column(String(300), nullable=False)
    description = Column(Text)
    url = Column(String(500), nullable=False)
    image_url = Column(String(500))

    # Цена и рейтинг
    price = Column(Float, nullable=False)
    old_price = Column(Float)
    discount_percent = Column(Float)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)

    # Доставка
    delivery_days = Column(Integer)
    delivery_cost = Column(Float, default=0.0)
    is_free_delivery = Column(Boolean, default=False)

    # Продавец
    seller_name = Column(String(200))
    seller_rating = Column(Float)

    # Метаданные парсинга
    parsed_at = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    parse_error = Column(String(500))

    # Связи
    internal_product = relationship(
        "InternalProduct",
        back_populates="marketplace_matches"
    )

    # ✅ Связь с ProcurementItem через импортированную таблицу
    procurement_items = relationship(
        "ProcurementItem",
        secondary=procurement_item_matches,  # Используем импортированную таблицу
        back_populates="marketplace_matches"
    )

    def __repr__(self):
        return f"<MarketplaceProduct(marketplace='{self.marketplace_name}', price={self.price})>"

    def to_dict(self):
        """Конвертация в словарь"""
        return {
            'id': self.id,
            'internal_product_id': self.internal_product_id,
            'marketplace_name': self.marketplace_name,
            'name': self.name,
            'url': self.url,
            'price': self.price,
            'rating': self.rating,
            'parsed_at': self.parsed_at.isoformat() if self.parsed_at else None,
        }

    @property
    def final_price(self) -> float:
        """Итоговая цена с учетом доставки"""
        return self.price + (self.delivery_cost or 0.0)

    @property
    def has_discount(self) -> bool:
        """Есть ли скидка"""
        return self.old_price is not None and self.old_price > self.price