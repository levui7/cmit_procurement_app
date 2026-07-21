"""
CRUD-операции для глобальных настроек
"""
from sqlalchemy.orm import Session
from typing import Optional

from backend.models.models_settings import AppSettings


def get_app_setting(
        db: Session,
        key: str,
        default_value: str = None
) -> Optional[str]:
    """Получить значение настройки"""
    setting = db.query(AppSettings).filter(AppSettings.key == key).first()
    return setting.value if setting else default_value


def set_app_setting(
        db: Session,
        key: str,
        value: str,
        description: str = ""
) -> bool:
    """Установить значение настройки"""
    setting = db.query(AppSettings).filter(AppSettings.key == key).first()
    if setting:
        setting.value = value
        if description:
            setting.description = description
    else:
        setting = AppSettings(key=key, value=value, description=description)
        db.add(setting)

    db.commit()
    return True