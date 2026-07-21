"""
Модель внутреннего каталога товаров
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .models_base import Base


class InternalProduct(Base):
    """Внутренний каталог ВолгГТУ (наименования внутри поликека)"""
    __tablename__ = "internal_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    internal_code = Column(String(50), unique=True, nullable=True)  # Код внутри поликека/1С
    name = Column(String(200), nullable=False)
    # category = Column(String(100), nullable=False)
    damage_percent = Column(Float, default=0.0)  # Процент поломки/амортизации
    keywords = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)

    # Связь: один внутренний товар может иметь много аналогов на маркетплейсах
    marketplace_matches = relationship("MarketplaceProduct",
                                    back_populates="internal_product",
                                    cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InternalProduct(id={self.id}, name='{self.name}')>"