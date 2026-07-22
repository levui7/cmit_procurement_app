import json
import re
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
INPUT_FILE = BASE_DIR / "extracted" / "products_clean.json"
OUTPUT_DIR = BASE_DIR / "normalized"
OUTPUT_FILE = OUTPUT_DIR / "products_ozon.json"

OUTPUT_DIR.mkdir(exist_ok=True)

def clean_number(text):
    if not text:
        return None
    text = str(text).replace("\u2009", "").replace("\xa0", "").replace(" ", "")
    numbers = re.findall(r"\d+", text)
    if not numbers:
        return None
    return int("".join(numbers))

def normalize_price(value):
    return clean_number(value)

def normalize_rating(value):
    if not value:
        return None
    value = value.replace(",", ".").strip()
    try:
        return float(value)
    except Exception:
        return None

def normalize_reviews(value):
    return clean_number(value)

def normalize_stock(value):
    return clean_number(value)

def normalize_discount(value):
    if not value:
        return None
    return clean_number(value)

def normalize_delivery(value):
    if not value:
        return {"text": None, "days": None}
    value_lower = value.lower()
    if "сегодня" in value_lower:
        days = 0
    elif "завтра" in value_lower:
        days = 1
    elif "послезавтра" in value_lower:
        days = 2
    else:
        match = re.search(r"(\d+)\s+июля", value_lower)
        if match:
            days = None
        else:
            days = None
    return {"text": value, "days": days}

def normalize_link(value):
    if not value:
        return None
    if value.startswith("http"):
        return value
    return "https://www.ozon.ru" + value

def normalize_product(product):
    return {
        "id": product.get("id"),
        "name": product.get("name"),
        "price": normalize_price(product.get("price")),
        "old_price": normalize_price(product.get("oldPrice")),
        "discount": normalize_discount(product.get("discount")),
        "rating": normalize_rating(product.get("rating")),
        "reviews_count": normalize_reviews(product.get("reviews")),
        "delivery": normalize_delivery(product.get("delivery")),
        "stock": normalize_stock(product.get("stock")),
        "link": normalize_link(product.get("link"))
    }

def normalize_products():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    normalized = {}
    for product in products:
        pid = product.get("id")
        if not pid:
            continue
        normalized[pid] = normalize_product(product)
    
    result = list(normalized.values())
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Готово: {OUTPUT_FILE}")
    print(f"Товаров: {len(result)}")

if __name__ == "__main__":
    normalize_products()