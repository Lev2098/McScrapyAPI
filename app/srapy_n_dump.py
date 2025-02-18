import os

path = r"/mcdonalds_scraper/menu.json"
if os.path.exists(path):
    print(f"File exists at path: {path}")
else:
    print(f"File not found at path: {path}")
