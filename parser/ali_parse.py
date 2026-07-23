import json
import os
import time
from datetime import datetime
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

# Безопасный импорт (работает и при прямом запуске, и при импорте из пакета)
try:
    from .extract_ali import process_products
    from .ali_normalized import normalize_process
except ImportError:
    from extract_ali import process_products
    from ali_normalized import normalize_process

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "aliexpress_raw")
os.makedirs(RAW_DIR, exist_ok=True)

def clear_raw():
    for file in os.listdir(RAW_DIR):
        if file.endswith(".json"):
            os.remove(os.path.join(RAW_DIR, file))

def save_json(data):
    filename = os.path.join(
        RAW_DIR,
        "ali_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".json"
    )
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Сохранено:", filename)

def click_page(page, number):
    print("Переход на страницу:", number)
    links = page.locator("a")
    for i in range(links.count()):
        try:
            text = links.nth(i).inner_text().strip()
            if text == str(number):
                print("Нажимаем страницу:", number)
                with page.expect_response(
                    lambda r: "aer-webapi/v2/recommend" in r.url and r.status == 200
                ) as response_info:
                    links.nth(i).click()
                response = response_info.value
                return response
        except Exception:
            pass
    print("Страница не найдена:", number)
    return None

def collect_pages(search_text="Arduino uno r3"):
    clear_raw()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        try:
            context = browser.new_context(
                locale="ru-RU",
                viewport={"width": 1600, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            url = f"https://aliexpress.ru/wholesale?SearchText={quote_plus(search_text)}"
            print("Открываем:", url)
            
            with page.expect_response(
                lambda r: "aer-webapi/v2/recommend" in r.url and r.status == 200
            ) as response_info:
                page.goto(url, wait_until="domcontentloaded")
            
            response = response_info.value
            try:
                data = response.json()
                count = len(data.get("data", {}).get("snippetsV2", []))
                if count:
                    print("Получено товаров:", count)
                    save_json(data)
            except Exception:
                print("Не удалось получить JSON первой страницы.")
            
            print("Первая страница загружена")
            max_pages = 5 # Уменьшил с 10 до 5 для более быстрого теста
            for number in range(2, max_pages + 1):
                response = click_page(page, number)
                if response is None:
                    break
                try:
                    data = response.json()
                    count = len(data.get("data", {}).get("snippetsV2", []))
                    if count:
                        print("Получено товаров:", count)
                        save_json(data)
                    time.sleep(2) # Небольшая пауза между страницами
                except Exception:
                    print(f"Не удалось обработать страницу {number}")
            
            context.storage_state(path=os.path.join(BASE_DIR, "aliexpress_state.json"))
        finally:
            browser.close()

def run_ali_parser(query: str):
    """Главная функция для запуска полного цикла парсинга AliExpress"""
    print(f"=== [Ali] Этап 1: сбор JSON для '{query}' ===")
    collect_pages(query)
    
    print("=== [Ali] Этап 2: извлечение товаров ===")
    process_products(query)
    
    print("=== [Ali] Этап 3: нормализация ===")
    normalize_process()
    
    print("=== [Ali] ГОТОВО ===")
    return True

if __name__ == "__main__":
    run_ali_parser("Arduino Nano")