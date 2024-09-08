import json
from nicegui import ui
from bs4 import BeautifulSoup
import os
import shutil
# TODO:  Get Serbian Flag
with open("utils/start_gg_countries.json", "r", encoding="utf-8") as file:
    countries = json.load(file)

with open("utils/states_hash.json", "r", encoding="utf-8") as file:
    states = json.load(file)

for country in countries:
    try:
        shutil.copy(f"country_flags_rounded/{country['code']}.png",f"utils/flags/{country['name']}.png")
    except Exception as e:
        print(f"Failed to grab {country['name']}")

for state in states:
    try:
        shutil.copy(f"state_flags_rounded/{state['code']}.png",f"utils/flags/{state['name']}.png")
    except Exception as e:
        print(f"Failed to grab {state['name']}")

# with open("utils/location_list.txt", "r") as file:
#     new_list = file.read()

# print(new_list)
# print(type(new_list))
# json_list = json.loads(new_list)

# print(json_list)


# ui.select(label="test",options=location_list,on_change=lambda e: print(e.value),with_input=True).classes("w-40")

# ui.run()