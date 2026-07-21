"""
Модель товаров, найденных на маркетплейсах
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from models.models_base import Base


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
    marketplace_name = Column(String(50), nullable=False)  # Ozon, Wildberries, Яндекс.Маркет
    marketplace_url = Column(String(500))  # Ссылка на страницу маркетплейса

    # Информация о товаре
    name = Column(String(300), nullable=False)  # Название товара на маркетплейсе
    description = Column(Text)  # Описание товара
    url = Column(String(500), nullable=False)  # Прямая ссылка на товар
    image_url = Column(String(500))  # Ссылка на изображение товара

    # Цена и рейтинг
    price = Column(Float, nullable=False)  # Цена в рублях
    old_price = Column(Float)  # Старая цена (если есть скидка)
    discount_percent = Column(Float)  # Процент скидки
    rating = Column(Float, default=0.0)  # Рейтинг товара
    review_count = Column(Integer, default=0)  # Количество отзывов

    # Доставка
    delivery_days = Column(Integer)  # Дней до доставки
    delivery_cost = Column(Float, default=0.0)  # Стоимость доставки
    is_free_delivery = Column(Boolean, default=False)  # Бесплатная доставка

    # Продавец
    seller_name = Column(String(200))  # Название продавца
    seller_rating = Column(Float)  # Рейтинг продавца

    # Метаданные парсинга
    parsed_at = Column(DateTime, default=datetime.now)  # Дата парсинга
    last_updated = Column(DateTime, onupdate=datetime.now)  # Дата последнего обновления
    is_active = Column(Boolean, default=True)  # Активен ли товар (не удален с маркетплейса)
    parse_error = Column(String(500))  # Ошибка при парсинге (если была)

    # Связи
    internal_product = relationship(
        "InternalProduct",
        back_populates="marketplace_matches"
    )

    def __repr__(self):
        return f"<MarketplaceProduct(marketplace='{self.marketplace_name}', price={self.price}, name='{self.name[:30]}...')>"

    def to_dict(self):
        """Конвертация в словарь"""
        return {
            'id': self.id,
            'internal_product_id': self.internal_product_id,
            'marketplace_name': self.marketplace_name,
            'marketplace_url': self.marketplace_url,
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'image_url': self.image_url,
            'price': self.price,
            'old_price': self.old_price,
            'discount_percent': self.discount_percent,
            'rating': self.rating,
            'review_count': self.review_count,
            'delivery_days': self.delivery_days,
            'delivery_cost': self.delivery_cost,
            'is_free_delivery': self.is_free_delivery,
            'seller_name': self.seller_name,
            'seller_rating': self.seller_rating,
            'parsed_at': self.parsed_at.isoformat() if self.parsed_at else None,
            'is_active': self.is_active,
        }

    @property
    def final_price(self) -> float:
        """Итоговая цена с учетом доставки"""
        return self.price + (self.delivery_cost or 0.0)

    @property
    def has_discount(self) -> bool:
        """Есть ли скидка"""
        return self.old_price is not None and self.old_price > self.price

    @property
    def discount_amount(self) -> float:
        """Размер скидки в рублях"""
        if self.has_discount:
            return self.old_price - self.price
        return 0.0