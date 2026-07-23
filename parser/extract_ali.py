import json
import os
import csv
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DIR = os.path.join(
    BASE_DIR,
    "aliexpress_raw"
)


OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "aliexpress_extracted"
)


OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "extracted_products.json"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

def extract_price(product):

    try:
        return (
            product["finalPrice"]
            ["element"][0]
            ["text"]
        )

    except Exception:
        return None

def extract_rating(product):

    try:

        for tag in product.get(
            "snippetTags",
            []
        ):

            if tag.get("type") == "review":

                return (
                    tag["element"][0]
                    ["text"]
                )

    except Exception:
        pass

    return None

def extract_orders(product):

    try:

        for tag in product.get(
            "snippetTags",
            []
        ):

            if tag.get("type") == "orders":

                return (
                    tag["element"][0]
                    ["text"]
                )

    except Exception:
        pass

    return None

def extract_delivery(product):

    try:

        event = (
            product["trackInfo"]
            ["aerEvent"]
        )

        return {
            "free": event.get(
                "snippetDeliveryFree"
            ),

            "next_day": event.get(
                "snippetDeliveryNextDay"
            ),

            "choice": event.get(
                "snippetDeliveryChoice"
            )
        }

    except Exception:

        return None

def title_matches_search(title, search_text):
    if not title:
        return False
    title = title.lower()
    # Очищаем поисковый запрос от знаков препинания (запятых и т.д.)
    search_text = re.sub(r'[^\w\s]', '', search_text).lower()
    
    words = [word for word in search_text.split() if len(word) > 2]
    matches = 0
    for word in words:
        if word in title:
            matches += 1
            
    # минимум половина слов запроса должна быть в названии
    return matches >= max(1, len(words) // 2)

def parse_files(search_text):

    products = {}

    total_products = 0

    for file in os.listdir(RAW_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(
            RAW_DIR,
            file
        )

        print(
            "Обрабатываем:",
            file
        )


        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)



        items = (
            data
            .get("data", {})
            .get("snippetsV2", [])
        )

        total_products += len(items)

        for item in items:

            if not title_matches_search(
                item.get("productTitle"),
                search_text
            ):

                print(
                    "Удален по названию:",
                    item.get("productTitle")
                )

                continue

            product = {

                "id": item.get(
                    "id"
                ),

                "title": item.get(
                    "productTitle"
                ),

                "url": item.get(
                    "productUrl"
                ),

                "price": extract_price(
                    item
                ),

                "rating": extract_rating(
                    item
                ),

                "orders": extract_orders(
                    item
                ),

                "delivery": extract_delivery(
                    item
                )
            }


            product_id = product.get("id")

            if product_id:

                products[product_id] = product


    print("Всего найдено товаров:",total_products)

    print("Удалено дублей:",total_products - len(products))

    return list(
        products.values()
    )


def save_products(products):

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            products,
            f,
            ensure_ascii=False,
            indent=2
        )


    print(
        "Уникальных товаров:",
        len(products)
    )


    print(
        "Сохранено:",
        OUTPUT_FILE
    )

def process_products(search_text="Arduino uno r3"):

    products = parse_files(search_text)

    save_products(
        products
    )

if __name__ == "__main__":

    process_products()