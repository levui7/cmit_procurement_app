from playwright.sync_api import sync_playwright
import json
from pathlib import Path
from datetime import datetime

def save_wb_json(query: str):
    BASE_DIR = Path(__file__).parent.resolve()
    save_dir = BASE_DIR / "wb_raw"
    save_dir.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(locale="ru-RU")
        url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={query.replace(' ', '+')}"
        print(f"URL: {url}")
        
        try:
            with page.expect_response(
                lambda r: "__internal/u-search" in r.url and "resultset=catalog" in r.url,
                timeout=60000
            ) as response_info:
                page.goto(url, wait_until="domcontentloaded")
            
            response = response_info.value
            data = response.json()
            filename = f"{query.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            path = save_dir / filename
            
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"JSON сохранён: {path}")
            print(f"Товаров: {len(data.get('products', []))}")
        except Exception as e:
            print(f"Ошибка при парсинге WB: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    save_wb_json("Arduino Nano")