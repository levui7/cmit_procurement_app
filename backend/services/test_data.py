"""
Сервис для заполнения тестовыми данными
"""
from sqlalchemy.orm import Session
from backend.models.models_internal_product import InternalProduct
from backend.models.models_settings import AppSettings

from backend.crud import (
    crud_internal_product as internal_product,
    crud_settings as settings
)

from typing import List


def seed_test_data(db: Session):
    """Заполнить БД тестовыми данными"""
    # 1. Добавляем глобальные настройки
    if not settings.get_app_setting(db, "default_damage_percent"):
        settings.set_app_setting(
            db,
            "default_damage_percent",
            "2.5",
            "Процент поломки/амортизации"
        )
        settings.set_app_setting(
            db,
            "default_min_rating",
            "4.0",
            "Минимальный рейтинг товара"
        )
        print("✅ Добавлены глобальные настройки приложения")

    # 2. Добавляем тестовые товары
    test_products = [
                ("INT-001", "Светодиоды 5мм красные (20 шт)", "Электроника", 1.0, "светодиоды, LED, 5мм, красные"),
                ("INT-002", "Светодиоды 5мм синие (20 шт)", "Электроника", 1.0, "светодиоды, LED, 5мм, синие"),
                ("INT-003", "L298N Driver Controller", "Электроника", 4.2, "драйвер, L298N, контроллер, мотор"),
                ("INT-004", "Сервопривод MG995 360°", "Робототехника", 3.3, "сервопривод, MG995, серво, мотор"),
                ("INT-005", "Метизы M4 потай (набор)", "Крепеж", 1.5, "метизы, винты, M4, крепеж"),
                ("INT-006", "Пластик PLA для 3D печати 1.75мм", "Расходные материалы", 2.0,
                 "3D печать, пластик, PLA, филамент"),
                ("INT-007", "Лак токопроводящий", "Электроника", 5.0, "лак, токопроводящий, электроника"),
                ("INT-008", "Графитовая токопроводящая краска", "Электроника", 4.5, "краска, графит, токопроводящая"),
                ("INT-009", "Батарейки AA Trofi (40 шт)", "Расходные материалы", 1.2, "батарейки, AA, питание, Trofi"),
                ("INT-010", "Arduino Uno R3", "Электроника", 6.0, "Arduino, Uno, контроллер, плата, микроконтроллер"),
                ("INT-011", "TSOP1738 ИК приемник", "Электроника", 2.5, "ИК приемник, TSOP1738, инфракрасный, датчик"),
                ("INT-012", "Резисторы 220 Ом (набор 100 шт)", "Электроника", 1.0, "резисторы, 220 Ом, электроника"),
                ("INT-013", "Провода Dupont папа-папа (40 шт)", "Электроника", 2.0, "провода, Dupont, соединители"),
                ("INT-014", "Провода Dupont мама-папа (40 шт)", "Электроника", 2.0, "провода, Dupont, соединители"),
                ("INT-015", "Макетная плата 830 контактов", "Электроника", 3.0, "макетная плата, breadboard, 830"),
            ]

    added_count = 0
    for code, name, category, damage, keywords in test_products:
        if not internal_product.get_internal_product_by_code(db, code):
            internal_product.create_internal_product(
                db,
                internal_code=code,
                name=name,
                # category=category,
                damage_percent=damage,
                keywords=keywords
            )
            added_count += 1

    if added_count > 0:
        db.commit()
        print(f"✅ Добавлено {added_count} новых тестовых товаров")
    else:
        print("ℹ️ Тестовые товары уже существуют, пропуск")