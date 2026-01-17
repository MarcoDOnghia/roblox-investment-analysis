import requests

url = "https://www.rolimons.com/itemapi/itemdetails"

print("Knocking on Rolimons' door...")
print("URL:", url)

response = requests.get(url)

print("\n Did they answer?")
print( "Status Code:" , response.status_code)

if response.status_code == 200:
    print("Success")
else: 
    print ("Failure")

data = response.json()

print("\n" + "="*50)
print("What kind of data did we get?")
print(type(data))

print("\nWhat categories are available?")
print(data.keys())

items_dict = data['items']

print("\nHow many items did they send us?")
print(len(items_dict))

first_item_id = list(items_dict.keys())[0]
first_item_data = items_dict[first_item_id]

print("\nExample item:")
print("Item ID:", first_item_id)
print("Item Details:", first_item_data)
print("Item Name:", first_item_data[0])
print("Item RAP (Robux):", first_item_data[2])