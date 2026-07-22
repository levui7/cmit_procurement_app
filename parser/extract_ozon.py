import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
INPUT_DIR = BASE_DIR / "ozon_raw"
OUTPUT_DIR = BASE_DIR / "extracted"
OUTPUT_FILE = OUTPUT_DIR / "products_clean.json"

OUTPUT_DIR.mkdir(exist_ok=True)

def extract_rating(main_state):
    for block in main_state:
        if block.get("type") == "labelListV2":
            texts = []
            for item in block["labelListV2"].get("items", []):
                if item.get("type") == "text":
                    texts.append(item["text"]["text"])
            for text in texts:
                clean = text.replace(",", ".")
                if "." in clean and clean.replace(".", "").isdigit():
                    return text
    return None

def extract_reviews(main_state):
    for block in main_state:
        if block.get("type") == "labelListV2":
            for item in block["labelListV2"].get("items", []):
                if item.get("type") == "text":
                    text = item["text"]["text"]
                    if "отзыв" in text:
                        return text
    return None

def extract_price(main_state):
    for block in main_state:
        if block.get("type") == "priceV2":
            prices = block["priceV2"].get("price", [])
            result = {}
            if len(prices) > 0:
                result["price"] = prices[0]["text"]
            if len(prices) > 1:
                result["oldPrice"] = prices[1]["text"]
            result["discount"] = block["priceV2"].get("discount")
            return result
    return {}

def extract_stock(main_state):
    for block in main_state:
        if block.get("type") == "textDS":
            test = block["textDS"].get("testInfo", {})
            if test.get("automatizationId") == "tile-blackFridayStockbar":
                return block["textDS"].get("text")
    return None

def extract_name(main_state):
    for block in main_state:
        if block.get("id") == "name":
            return block["textDS"].get("text")
    return None

def extract_delivery(item):
    try:
        return item["multiButton"]["ozonButton"]["addToCart"]["actionButton"]["title"]
    except Exception:
        return None

def parse_product(item):
    main_state = item.get("mainState", [])
    price = extract_price(main_state)
    return {
        "id": item.get("id"),
        "name": extract_name(main_state),
        "price": price.get("price"),
        "oldPrice": price.get("oldPrice"),
        "discount": price.get("discount"),
        "rating": extract_rating(main_state),
        "reviews": extract_reviews(main_state),
        "delivery": extract_delivery(item),
        "stock": extract_stock(main_state),
        "link": item.get("action", {}).get("link")
    }

def extract_products():
    products = {}
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")]
    print(f"Найдено файлов: {len(files)}")
    
    for filename in files:
        path = INPUT_DIR / filename
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            widgets = data.get("widgetStates", {})
            for key, value in widgets.items():
                if not key.startswith("tileGridDesktop"):
                    continue
                try:
                    widget = json.loads(value)
                except Exception:
                    continue
                for item in widget.get("items", []):
                    product = parse_product(item)
                    pid = product.get("id")
                    if pid:
                        products[pid] = product
            print(f"{filename} OK")
        except Exception as e:
            print(f"{filename} ERROR {e}")
    
    result = list(products.values())
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("====================")
    print(f"Уникальных товаров: {len(result)}")
    print(f"Сохранено: {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_products()