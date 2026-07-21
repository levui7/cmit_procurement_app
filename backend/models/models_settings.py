"""
Модель глобальных настроек приложения
"""
from sqlalchemy import Column, Integer, String
from .models_base import Base


class AppSettings(Base):
    """Глобальные настройки приложения"""
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(String(500))
    description = Column(String(300))