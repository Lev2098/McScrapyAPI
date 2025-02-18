import json


with open("mcdonalds_scraper/menu.json", "r", encoding="utf-8") as file1:

    all_items = json.load(file1)
    all_ids = {str(item["id"]) for item in all_items}

with open(
        "mcdonalds_scraper/macdonalds_menu_old.json", "r", encoding="utf-8"
) as file2:

    scraped_items = json.load(file2)
    scraped_ids = {str(item["id_item"]) for item in scraped_items}

missing_ids = all_ids - scraped_ids
extra_ids = scraped_ids - all_ids

print("Порівняння ID:")
print(f"- Відсутні ID у розпарсених даних: {missing_ids}")
print(f"- Зайві ID у розпарсених даних (не в списку): {extra_ids}")
