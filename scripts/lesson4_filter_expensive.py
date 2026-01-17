import requests

url = "https://www.rolimons.com/itemapi/itemdetails"
response = requests.get(url)
data = response.json()
items_dict = data['items']

print("Total items in the catalog:" , len(items_dict))

expensive_items = []

for item_id, item_details in items_dict.items():
    item_name = item_details[0]
    RAP = item_details [2]

    if RAP > 100000:
        expensive_items.append((item_name, RAP))

print(f"\nExpensive items (RAP > 100k): {len(expensive_items)}")

expensive_items.sort(key=lambda x:x[1] , reverse= True)

print("\n🏆 TOP 10 MOST EXPENSIVE ROBLOX LIMITED ITEMS:")

for i, (name, rap) in enumerate(expensive_items[:10], 1):
    print(f"{i}. {name:<40} {rap:>12,} Robux")



