"""
Нормализация данных Wildberries
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
INPUT_FILE = BASE_DIR / "wb_extracted" / "products_clean_wb.json"
OUTPUT_DIR = BASE_DIR / "normalized"
OUTPUT_FILE = OUTPUT_DIR / "products_wb.json"

OUTPUT_DIR.mkdir(exist_ok=True)


def normalize_wb_product(product):
    # ГЛАВНОЕ: WB отдает цену в копейках. Делим на 100.
    price_kopecks = product.get("price_kopecks", 0)
    try:
        price_rub = float(price_kopecks) / 100.0
    except (ValueError, TypeError):
        price_rub = 0.0
        
    rating = product.get("rating", 0)
    try:
        rating = float(rating)
    except (ValueError, TypeError):
        rating = 0.0
        
    return {
        "id": product.get("id"),
        "name": product.get("name"),
        "price": round(price_rub, 2),
        "old_price": None,
        "discount": None,
        "rating": rating,
        "reviews_count": int(product.get("reviews", 0)),
        "delivery": {"text": "Доставка WB", "days": 2},
        "stock": None,
        "link": product.get("link")
    }


def normalize_wb_products():
    if not INPUT_FILE.exists():
        print("[WB] Файл для нормализации не найден!")
        return
        
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    normalized = {}
    for product in products:
        pid = product.get("id")
        if not pid:
            continue
        normalized[pid] = normalize_wb_product(product)
    
    result = list(normalized.values())
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"[WB] Готово: {OUTPUT_FILE}")
    print(f"[WB] Нормализовано товаров: {len(result)}")


if __name__ == "__main__":
    normalize_wb_products()