import json
from nicegui import ui
from bs4 import BeautifulSoup
import os

location_list=[]

with open("utils/start_gg_countries.json", "r", encoding="utf-8") as file:
    countries = json.load(file)
with open("utils/states_hash.json", "r", encoding="utf-8") as file:
    states = json.load(file)
    
for country in countries:
    location_list.append(country["name"])
for state in states:
    location_list.append(state["name"])
    

with open("utils/location_list.json", "w", encoding="utf-8") as file:
    json.dump(location_list,file,indent=2, ensure_ascii=False)

with open("utils/location_list.json", "r", encoding='utf-8') as file:
    locations = json.load(file)

print(locations)
# with open("utils/location_list.txt", "r") as file:
#     new_list = file.read()

# print(new_list)
# print(type(new_list))
# json_list = json.loads(new_list)

# print(json_list)


# ui.select(label="test",options=location_list,on_change=lambda e: print(e.value),with_input=True).classes("w-40")

# ui.run()