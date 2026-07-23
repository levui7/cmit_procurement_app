"""
Извлечение полей из сырого JSON Wildberries
"""
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
INPUT_DIR = BASE_DIR / "wb_raw"
OUTPUT_DIR = BASE_DIR / "wb_extracted"
OUTPUT_FILE = OUTPUT_DIR / "products_clean_wb.json"

OUTPUT_DIR.mkdir(exist_ok=True)


def parse_wb_product(item):
    """Извлечение данных из одного товара WB"""
    product_id = item.get("id")
    name = item.get("name", "Без названия")
    
    # Цена в копейках (salePriceU) или обычная (priceU)
    price_kopecks = item.get("salePriceU") or item.get("priceU") or 0
    
    rating = item.get("rating", 0)
    reviews = item.get("feedbacks", 0)
    
    # Формируем прямую ссылку на товар
    link = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"
    
    return {
        "id": product_id,
        "name": name,
        "price_kopecks": price_kopecks,
        "rating": rating,
        "reviews": reviews,
        "link": link
    }


def extract_wb_products():
    products = {}
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")]
    print(f"[WB] Найдено файлов: {len(files)}")
    
    for filename in files:
        path = INPUT_DIR / filename
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # WB API обычно кладет товары в data.products
            items = data.get("data", {}).get("products", [])
            
            for item in items:
                product = parse_wb_product(item)
                pid = product.get("id")
                if pid:
                    products[pid] = product
                    
            print(f"[WB] {filename} OK (найдено {len(items)} товаров)")
        except Exception as e:
            print(f"[WB] {filename} ERROR: {e}")
    
    result = list(products.values())
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"[WB] Уникальных товаров: {len(result)}")
    print(f"[WB] Сохранено: {OUTPUT_FILE}")


if __name__ == "__main__":
    extract_wb_products()