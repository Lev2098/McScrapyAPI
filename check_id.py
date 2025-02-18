import json

# Завантаження JSON даних із файлів
with open('mcdonalds_scraper/menu.json', 'r', encoding='utf-8') as file1:
    # Всі ID перетворюємо в рядки
    all_items = json.load(file1)
    all_ids = {str(item["id"]) for item in all_items}  # Витягаємо множину ID як рядки

with open('mcdonalds_scraper/macdonalds_menu_old.json', 'r', encoding='utf-8') as file2:
    # Всі ID перетворюємо в рядки
    scraped_items = json.load(file2)
    scraped_ids = {str(item["id_item"]) for item in scraped_items}

# Порівнюємо множини
missing_ids = all_ids - scraped_ids
extra_ids = scraped_ids - all_ids

# Виводимо результати
print("Порівняння ID:")
print(f"- Відсутні ID у розпарсених даних: {missing_ids}")
print(f"- Зайві ID у розпарсених даних (не в списку): {extra_ids}")