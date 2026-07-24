from playwright.sync_api import sync_playwright
import json
from pathlib import Path
from datetime import datetime

# Импорт следующих этапов парсинга
from .extract_wb import extract_wb_products
from .normalize_products_wb import normalize_wb_products


def save_wb_json(query):
    save_dir = Path("wb_raw")
    save_dir.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(locale="ru-RU")

        url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={query.replace(' ', '+')}"
        print(url)

        with page.expect_response(
            lambda r:
                "__internal/u-search" in r.url
                and "resultset=catalog" in r.url,
            timeout=60000
        ) as response_info:
            page.goto(url, wait_until="domcontentloaded")

        response = response_info.value
        data = response.json()

        filename = f"{query.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = save_dir / filename

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("JSON сохранён:", path)
        
        # Универсальная проверка структуры JSON Wildberries
        products = data.get("data", {}).get("products", []) or data.get("products", [])
        print("Товаров:", len(products))

        browser.close()


def run_wb_parser(query: str):
    """Запуск полного цикла парсинга WB"""
    print(f"=== [WB] Этап 1: сбор JSON для '{query}' ===")
    save_wb_json(query)
    
    print("=== [WB] Этап 2: извлечение товаров ===")
    extract_wb_products()
    
    print("=== [WB] Этап 3: нормализация ===")
    normalize_wb_products()
    
    print("=== [WB] ГОТОВО ===")
    return True


if __name__ == "__main__":
    run_wb_parser("Arduino Nano")