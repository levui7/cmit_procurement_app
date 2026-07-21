"""
Модели для заявок на закупку
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .models_base import Base


class ProcurementRequest(Base):
    """Заявка на закупку (прогноз потребности)"""
    __tablename__ = "procurement_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(20), unique=True, nullable=False)  # Номер заявки (001, 002, ...)
    description = Column(String(500))  # Описание/назначение закупки

    # Параметры закупки
    students_count = Column(Integer, default=0)  # Количество студентов
    forecast_date = Column(DateTime, default=datetime.now)  # Дата создания прогноза
    delivery_date = Column(String(20))  # Желаемая дата поставки

    # Фильтры для поиска
    min_price = Column(Float)  # Минимальная цена (общая)
    max_price = Column(Float)  # Максимальная цена (общая)
    min_rating = Column(String(20))  # Минимальный рейтинг товара

    # Статус и сумма
    status = Column(String(20), default="new")  # new, in_progress, completed, cancelled
    total_amount = Column(Float, default=0.0)  # Общая сумма заявки

    # Метаданные
    created_at = Column(DateTime, default=datetime.now)  # Дата создания
    updated_at = Column(DateTime, onupdate=datetime.now)  # Дата обновления

    # Связь с позициями товаров
    items = relationship(
        "ProcurementItem",
        back_populates="request",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ProcurementRequest(number='{self.number}', status='{self.status}')>"

    def to_dict(self):
        """Конвертация в словарь"""
        return {
            'id': self.id,
            'number': self.number,
            'description': self.description,
            'students_count': self.students_count,
            'forecast_date': self.forecast_date.isoformat() if self.forecast_date else None,
            'delivery_date': self.delivery_date,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'min_rating': self.min_rating,
            'status': self.status,
            'total_amount': self.total_amount,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ProcurementItem(Base):
    """Позиция товара внутри заявки на закупку"""
    __tablename__ = "procurement_items"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Внешние ключи
    request_id = Column(
        Integer,
        ForeignKey("procurement_requests.id", ondelete="CASCADE"),
        nullable=False
    )
    internal_product_id = Column(
        Integer,
        ForeignKey("internal_products.id"),
        nullable=False
    )

    # Параметры позиции
    quantity = Column(Integer, default=1)  # Количество единиц товара
    min_price = Column(Float, default=0.0)  # Мин. цена для этого товара
    max_price = Column(Float, default=0.0)  # Макс. цена для этого товара

    # Результаты поиска (заполняются после парсинга)
    found_count = Column(Integer, default=0)  # Сколько найдено вариантов
    best_price = Column(Float)  # Лучшая найденная цена
    selected_marketplace_id = Column(Integer)  # ID выбранного товара на маркетплейсе

    # Связи
    request = relationship("ProcurementRequest", back_populates="items")
    product = relationship("InternalProduct")
    marketplace_matches = relationship(
        "MarketplaceProduct",
        secondary="procurement_item_matches",  # Промежуточная таблица
        back_populates="procurement_items"
    )

    def __repr__(self):
        return f"<ProcurementItem(request_id={self.request_id}, product_id={self.internal_product_id})>"

    def to_dict(self):
        """Конвертация в словарь"""
        return {
            'id': self.id,
            'request_id': self.request_id,
            'internal_product_id': self.internal_product_id,
            'quantity': self.quantity,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'found_count': self.found_count,
            'best_price': self.best_price,
            'product_name': self.product.name if self.product else None,
        }


# Промежуточная таблица для связи многие-ко-многим
# между позициями заявки и найденными товарами на маркетплейсах
procurement_item_matches = Table(
    'procurement_item_matches',
    Base.metadata,
    Column('procurement_item_id', Integer, ForeignKey('procurement_items.id')),
    Column('marketplace_product_id', Integer, ForeignKey('marketplace_products.id')),
    Column('is_selected', Boolean, default=False),  # Выбран ли этот вариант
    Column('parsed_at', DateTime, default=datetime.now)
)