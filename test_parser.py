from parser.parser_service import search_and_save_to_db

print("Запускаем тест парсера Ozon...")
result = search_and_save_to_db(
    query="Arduino Nano", 
    internal_product_id=1, 
    marketplace="ozon"
)

if result:
    print("Парсинг успешен, данные сохранены в БД")
else:
    print("Парсинг завершился с ошибкой")