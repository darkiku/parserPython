import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

all_restaurants = []
seen_ids = set()

queries = [
    "ресторан", "кафе", "бар", "столовая", "кофейня",
    "пиццерия", "суши", "шашлык", "плов", "бургер"
]

for query in queries:
    print(f"\nпоиск: {query}")

    for page in range(1, 50):
        try:
            response = requests.get("https://catalog.api.2gis.com/3.0/items", params={
                "q": query,
                "point": "71.4491,51.1694",
                "radius": "20000",
                "page": page,
                "page_size": 10,
                "key": API_KEY
            })

            data = response.json()

            if "result" not in data:
                break

            items = data["result"].get("items", [])

            if not items:
                break

            for item in items:
                item_id = item.get("id")
                if item_id and item_id not in seen_ids:
                    seen_ids.add(item_id)
                    all_restaurants.append({
                        "id": item_id,
                        "name": item.get("name", ""),
                        "address": item.get("address_name", ""),
                        "type": item.get("purpose_name", "")
                    })

            if len(all_restaurants) >= 1000:
                break

            time.sleep(0.3)
        except:
            break

    print(f"всего: {len(all_restaurants)}")

    if len(all_restaurants) >= 1000:
        break

with open('restaurants_2gis.json', 'w', encoding='utf-8') as f:
    json.dump(all_restaurants[:1000], f, ensure_ascii=False, indent=2)

print(f"готово: {len(all_restaurants[:1000])}")
