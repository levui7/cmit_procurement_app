"""
Модуль работы с базой данных
"""
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Путь к файлу БД
DB_DIR = Path(__file__).parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "procurement.db"

# Создание движка БД
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Базовый класс для моделей
Base = declarative_base()

# Сессия для работы с БД
SessionLocal = sessionmaker(bind=engine)


# ========== МОДЕЛИ ДАННЫХ ==========

class InternalProduct(Base):
    """Внутренний каталог ВолгГТУ (наименования внутри поликека)"""
    __tablename__ = "internal_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    internal_code = Column(String(50), unique=True, nullable=True)  # Код внутри поликека/1С
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    damage_percent = Column(Float, default=0.0)  # Процент поломки/амортизации
    keywords = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)

    # Связь: один внутренний товар может иметь много аналогов на маркетплейсах
    marketplace_matches = relationship("MarketplaceProduct", back_populates="internal_product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InternalProduct(id={self.id}, name='{self.name}')>"


class MarketplaceProduct(Base):
    """Товары на маркетплейсах (Ozon, WB и т.д.)"""
    __tablename__ = "marketplace_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    internal_product_id = Column(Integer, ForeignKey("internal_products.id"), nullable=False)

    marketplace_name = Column(String(50), nullable=False)  # Например: "Ozon", "Wildberries"
    name = Column(String(300), nullable=False)
    url = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, default=0.0)
    parsed_at = Column(DateTime, default=datetime.now)

    # Обратная связь
    internal_product = relationship("InternalProduct", back_populates="marketplace_matches")

    def __repr__(self):
        return f"<MarketplaceProduct(id={self.id}, marketplace='{self.marketplace_name}', price={self.price})>"


class ProcurementRequest(Base):
    """Прогнозы и заявки на закупку"""
    __tablename__ = "procurement_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(20), unique=True, nullable=False)
    description = Column(String(500))

    # Поля из плана: дата, кол-во студентов
    students_count = Column(Integer, default=0)
    forecast_date = Column(DateTime, default=datetime.now)  # Дата прогноза/создания
    delivery_date = Column(String(20))  # Желаемая дата поставки

    min_price = Column(Float)
    max_price = Column(Float)
    min_rating = Column(String(20))
    status = Column(String(20), default="new")  # new, in_progress, completed
    total_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)

    # Связь с товарами заявки
    items = relationship("ProcurementItem", back_populates="request", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProcurementRequest(number='{self.number}', students={self.students_count})>"


class ProcurementItem(Base):
    """Конкретные товары внутри одной заявки"""
    __tablename__ = "procurement_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(Integer, ForeignKey("procurement_requests.id"), nullable=False)
    internal_product_id = Column(Integer, ForeignKey("internal_products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    estimated_price = Column(Float)

    request = relationship("ProcurementRequest", back_populates="items")
    product = relationship("InternalProduct")


class Supplier(Base):
    """Поставщики (опционально, для будущего расширения)"""
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(100))
    phone = Column(String(50))
    email = Column(String(100))
    rating = Column(Float, default=0.0)


# ========== ФУНКЦИИ ДЛЯ РАБОТЫ С БД ==========

def init_db():
    """Инициализация БД: создание таблиц"""
    Base.metadata.create_all(engine)
    print(f"✅ База данных инициализирована: {DB_PATH}")


def get_session():
    """Получить сессию БД"""
    return SessionLocal()


# ========== CRUD ДЛЯ ВНУТРЕННЕГО КАТАЛОГА ==========

def add_internal_product(internal_code, name, category, damage_percent=0.0, keywords=""):
    """Добавить товар во внутренний каталог"""
    session = get_session()
    try:
        product = InternalProduct(
            internal_code=internal_code,
            name=name,
            category=category,
            damage_percent=damage_percent,
            keywords=keywords
        )
        session.add(product)
        session.commit()
        return product.id
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка добавления товара: {e}")
        return None
    finally:
        session.close()


def get_all_internal_products():
    """Получить все товары внутреннего каталога"""
    session = get_session()
    try:
        products = session.query(InternalProduct).all()
        return products
    finally:
        session.close()


def search_internal_products(query):
    """Поиск товаров по названию, коду или ключевым словам"""
    session = get_session()
    try:
        search_term = f"%{query}%"
        products = session.query(InternalProduct).filter(
            (InternalProduct.name.like(search_term)) |
            (InternalProduct.internal_code.like(search_term)) |
            (InternalProduct.keywords.like(search_term))
        ).all()
        return products
    finally:
        session.close()


def update_internal_product(product_id, **kwargs):
    """Обновить товар внутреннего каталога"""
    session = get_session()
    try:
        product = session.query(InternalProduct).filter_by(id=product_id).first()
        if product:
            for key, value in kwargs.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка обновления товара: {e}")
        return False
    finally:
        session.close()


def delete_internal_product(product_id):
    """Удалить товар из внутреннего каталога"""
    session = get_session()
    try:
        product = session.query(InternalProduct).filter_by(id=product_id).first()
        if product:
            session.delete(product)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка удаления товара: {e}")
        return False
    finally:
        session.close()


# ========== CRUD ДЛЯ ТОВАРОВ НА МАРКЕТПЛЕЙСАХ ==========

def add_marketplace_match(internal_product_id, marketplace_name, name, url, price, rating=0.0):
    """Добавить найденный товар на маркетплейсе, привязанный к внутреннему"""
    session = get_session()
    try:
        match = MarketplaceProduct(
            internal_product_id=internal_product_id,
            marketplace_name=marketplace_name,
            name=name,
            url=url,
            price=price,
            rating=rating
        )
        session.add(match)
        session.commit()
        return match.id
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка добавления товара маркетплейса: {e}")
        return None
    finally:
        session.close()


def get_marketplace_matches(internal_product_id):
    """Получить все варианты товара на маркетплейсах для конкретного внутреннего товара"""
    session = get_session()
    try:
        matches = session.query(MarketplaceProduct).filter_by(
            internal_product_id=internal_product_id
        ).order_by(MarketplaceProduct.price.asc()).all()  # Сортируем по цене
        return matches
    finally:
        session.close()


# ========== CRUD ДЛЯ ЗАЯВОК ==========

def create_procurement_request(data):
    """Создать новую заявку/прогноз"""
    session = get_session()
    try:
        last_request = session.query(ProcurementRequest).order_by(
            ProcurementRequest.id.desc()
        ).first()

        new_number = f"{int(last_request.number) + 1:03d}" if last_request else "001"

        request = ProcurementRequest(
            number=new_number,
            description=data.get("description", ""),
            students_count=data.get("students_count", 0),
            min_price=data.get("min_price", 0),
            max_price=data.get("max_price", 0),
            delivery_date=data.get("delivery_date", ""),
            min_rating=data.get("min_rating", ""),
            status="new"
        )
        session.add(request)
        session.commit()
        return request.id, new_number
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка создания заявки: {e}")
        return None, None
    finally:
        session.close()


def get_all_requests():
    """Получить все заявки"""
    session = get_session()
    try:
        requests = session.query(ProcurementRequest).order_by(
            ProcurementRequest.created_at.desc()
        ).all()
        return requests
    finally:
        session.close()

# НАСТРОЙКИ ПРИЛОЖЕНИЯ
class AppSettings(Base):
    """Глобальные настройки приложения"""
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(String(500))
    description = Column(String(300))


def seed_test_data():
    """Заполнить БД тестовыми данными"""
    session = get_session()
    try:
        # 1. Добавляем глобальные настройки, если их нет
        if session.query(AppSettings).filter_by(key="default_damage_percent").first() is None:
            settings = [
                AppSettings(key="default_damage_percent", value="2.5", description="Процент поломки/амортизации"),
                AppSettings(key="default_min_rating", value="4.0", description="Минимальный рейтинг товара"),
            ]
            session.add_all(settings)
            session.commit()
            print("✅ Добавлены глобальные настройки приложения")

        # 2. Добавляем тестовые товары, проверяя уникальность кода
        # 2. Добавляем тестовые товары, проверяя уникальность кода
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
            # Проверяем, есть ли уже товар с таким кодом
            existing = session.query(InternalProduct).filter_by(internal_code=code).first()
            if not existing:
                product = InternalProduct(
                    internal_code=code,
                    name=name,
                    category=category,
                    damage_percent=damage,
                    keywords=keywords
                )
                session.add(product)
                added_count += 1

        if added_count > 0:
            session.commit()
            print(f"✅ Добавлено {added_count} новых тестовых товаров")
        else:
            print("ℹ️ Тестовые товары уже существуют, пропуск")

    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка заполнения тестовых данных: {e}")
    finally:
        session.close()


def get_next_internal_code():
    """Получить следующий доступный внутренний код"""
    session = get_session()
    try:
        # Получаем все коды, которые начинаются с "INT-"
        products = session.query(InternalProduct).filter(
            InternalProduct.internal_code.like('INT-%')
        ).all()

        if not products:
            return "INT-001"

        # Извлекаем числовые части
        numbers = []
        for product in products:
            try:
                # Извлекаем число после "INT-"
                code_num = int(product.internal_code.replace("INT-", ""))
                numbers.append(code_num)
            except (ValueError, AttributeError):
                continue

        # Если есть числа, берем максимальное + 1
        if numbers:
            next_num = max(numbers) + 1
            return f"INT-{next_num:03d}"  # Форматируем как INT-001, INT-002 и т.д.
        else:
            return "INT-001"

    except Exception as e:
        print(f"❌ Ошибка получения следующего кода: {e}")
        return "INT-001"
    finally:
        session.close()

# ========== ФУНКЦИИ ДЛЯ РАБОТЫ С НАСТРОЙКАМИ ==========

def get_app_setting(key, default_value=None):
    """Получить значение настройки"""
    session = get_session()
    try:
        setting = session.query(AppSettings).filter_by(key=key).first()
        return setting.value if setting else default_value
    finally:
        session.close()


def set_app_setting(key, value, description=""):
    """Установить значение настройки"""
    session = get_session()
    try:
        setting = session.query(AppSettings).filter_by(key=key).first()
        if setting:
            setting.value = value
            if description:
                setting.description = description
        else:
            setting = AppSettings(key=key, value=value, description=description)
            session.add(setting)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка сохранения настройки: {e}")
        return False
    finally:
        session.close()


def get_all_app_settings():
    """Получить все настройки"""
    session = get_session()
    try:
        settings = session.query(AppSettings).all()
        return {s.key: s.value for s in settings}
    finally:
        session.close()