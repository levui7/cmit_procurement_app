import json
import time
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from datetime import datetime

# Абсолютные пути относительно текущего файла
BASE_DIR = Path(__file__).parent.resolve()
RAW_DIR = BASE_DIR / "ozon_raw"
RAW_DIR.mkdir(exist_ok=True)

# Импорт функций из соседних файлов
from .extract_ozon import extract_products
from .normalize_products_ozon import normalize_products

saved_files = set()

def log_response(response, raw_dir):
    if "page/json/v2" not in response.url:
        return
    if response.status != 200:
        return
    try:
        data = response.json()
        widgets = data.get("widgetStates", {})
        has_products = False
        for key in widgets:
            if key.startswith("tileGridDesktop"):
                has_products = True
                break
        if not has_products:
            return
        
        filename = raw_dir / f"ozon_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Сохранено: {filename}")
    except Exception as e:
        print(f"Ошибка: {e}")

def clear_raw(raw_dir):
    if not raw_dir.exists():
        return
    for file in raw_dir.glob("*.json"):
        file.unlink()

def collect_pages(query: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            locale="ru-RU",
            viewport={"width": 1600, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        page.on("response", lambda r: log_response(r, RAW_DIR))
        
        clear_raw(RAW_DIR)
        
        search_url = f"https://www.ozon.ru/search/?text={query.replace(' ', '+')}"
        page.goto(search_url, wait_until="domcontentloaded")
        
        # Проверка на antibot challenge page
        if "challenge" in page.url.lower() or "captcha" in page.title().lower():
            print("ОШИБКА: Обнаружена страница антибота (antibot challenge page) на Ozon.")
            browser.close()
            return False

        page.wait_for_timeout(5000)
        print("Начинаем скролл")
        for i in range(30):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1000)
            print(f"Скролл {i + 1}")
        
        context.storage_state(path=BASE_DIR / "ozon_state.json")
        browser.close()
        return True

def run_ozon_parser(query: str):
    print("=== Этап 1: сбор JSON ===")
    success = collect_pages(query)
    if not success:
        print("Парсинг прерван из-за антибота.")
        return False
    
    print("=== Этап 2: извлечение товаров ===")
    extract_products()
    print("=== Этап 3: нормализация ===")
    normalize_products()
    print("=== ГОТОВО ===")
    return True

if __name__ == "__main__":
    run_ozon_parser("Arduino Nano")