import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "aliexpress_extracted")
INPUT_FILE = os.path.join(INPUT_DIR, "extracted_products.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "ali_normalized")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "products_normalized.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def normalize_id(value):
    if not value:
        return None
    try:
        return int(value)
    except Exception:
        return None

def normalize_price(value):
    if not value:
        return None
    try:
        value = str(value).replace("₽", "").replace("\u00A0", "").replace(" ", "")
        return int(float(value.replace(",", ".")))
    except Exception:
        return None

def normalize_rating(value):
    if not value:
        return None
    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return None

def normalize_orders(value):
    if not value:
        return None
    try:
        text = str(value).lower()
        number = re.search(r"[\d,.]+", text)
        if not number:
            return None
        result = float(number.group().replace(",", "."))
        if "тыс" in text:
            result *= 1000
        elif "млн" in text:
            result *= 1000000
        return int(result)
    except Exception:
        return None

def normalize_product(product):
    normalized = product.copy()
    normalized["id"] = normalize_id(product.get("id"))
    normalized["price"] = normalize_price(product.get("price"))
    normalized["rating"] = normalize_rating(product.get("rating"))
    normalized["orders"] = normalize_orders(product.get("orders"))
    return normalized

def normalize_process():
    if not os.path.exists(INPUT_FILE):
        print("Не найден файл:", INPUT_FILE)
        return
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)
    normalized_products = []
    for product in products:
        normalized_products.append(normalize_product(product))
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(normalized_products, f, ensure_ascii=False, indent=2)
    print("Обработано товаров:", len(products))
    print("Сохранено:", OUTPUT_FILE)

if __name__ == "__main__":
    print("=== Нормализация AliExpress товаров ===")
    normalize_process()
    print("=== ГОТОВО ===")