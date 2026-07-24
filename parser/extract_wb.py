import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
INPUT_DIR = BASE_DIR / "wb_raw"
OUTPUT_DIR = BASE_DIR / "wb_extracted"
OUTPUT_FILE = OUTPUT_DIR / "products_clean_wb.json"

OUTPUT_DIR.mkdir(exist_ok=True)


def parse_wb_product(item):
    product_id = item.get("id")
    name = item.get("name", "Без названия")
    
    # Получаем данные о цене из sizes[0].price
    sizes_price_data = item.get("sizes", [{}])[0].get("price") if item.get("sizes") else None
    
    price_kopecks = 0
    
    # Если price - это словарь (новая структура WB), извлекаем значение из ключа 'product' или 'basic'
    if isinstance(sizes_price_data, dict):
        price_kopecks = sizes_price_data.get("product") or sizes_price_data.get("basic") or 0
    elif sizes_price_data is not None:
        # Если price - это число (старая структура)
        price_kopecks = sizes_price_data
    
    # Если не нашли в sizes, пробуем другие поля на всякий случай
    if price_kopecks == 0:
        price_kopecks = (
            item.get("salePriceU") or 
            item.get("priceU") or 
            item.get("salePrice") or 
            item.get("price") or
            0
        )
    
    # Рейтинг
    rating = (
        item.get("rating") or 
        item.get("reviewRating") or 
        item.get("feedbackRating") or
        0
    )
    
    reviews = item.get("feedbacks") or item.get("reviews") or 0
    
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
            
            # Универсальная проверка структуры JSON Wildberries
            items = data.get("data", {}).get("products", [])
            if not items:
                items = data.get("products", [])
            
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