import json
import shutil
from constants import MATCH_JSON_PATH
from utils.image_rounder import add_border_and_round_corners, resize_image
from writer import scoreboard_writer
from constants import *


async def change_text(input, path):
    with open(path, "w", encoding="utf-8") as file:
        file.write(str(input))
    return


def swap_players():
    with open(MATCH_JSON_PATH, "r", encoding="utf-8") as file:

        bracket_json = json.load(file)
        bracket_json["players"][0], bracket_json["players"][1] = (
            bracket_json["players"][1],
            bracket_json["players"][0],
        )

    with open(MATCH_JSON_PATH, "w") as file:
        file.write(json.dumps(bracket_json))
        scoreboard_writer(bracket_json)
        return bracket_json


def swap_files(file1_path, file2_path):
    temp_file_path = file1_path + ".tmp"
    shutil.move(file1_path, temp_file_path)
    shutil.move(file2_path, file1_path)
    shutil.move(temp_file_path, file2_path)


def swap_player_files():

    try:
        swap_files(
            P1_GAMERTAG_PATH,
            P2_GAMERTAG_PATH,
        )
    except Exception as e:
        print(f"failed to swap gamertag files: {e}")
    try:
        swap_files(
            P1_SCORE_PATH,
            P2_SCORE_PATH,
        )
    except Exception as e:
        print(f"failed to swap score files: {e}")
    try:
        swap_files(
            P1_ID_PATH,
            P2_ID_PATH,
        )
    except Exception as e:
        print(f"failed to swap id files: {e}")
    try:
        swap_files(
            P1_FLAG_PATH,
            P2_FLAG_PATH,
        )
    except Exception as e:
        print(f"failed to swap flag files: {e}")


def swap_player_files():

    try:
        swap_files(
            P1_GAMERTAG_PATH,
            P2_GAMERTAG_PATH,
        )
    except Exception as e:
        print(f"failed to swap gamertag files: {e}")
    try:
        swap_files(
            P1_SCORE_PATH,
            P2_SCORE_PATH,
        )
    except Exception as e:
        print(f"failed to swap score files: {e}")
    try:
        swap_files(
            P1_ID_PATH,
            P2_ID_PATH,
        )
    except Exception as e:
        print(f"failed to swap id files: {e}")
    try:
        swap_files(
            P1_FLAG_PATH,
            P2_FLAG_PATH,
        )
    except Exception as e:
        print(f"failed to swap flag files: {e}")


def upload_flag(image, flag_name, border_size, corner_radius):
    path = f"{FLAG_PATH}/{flag_name}.png"

    with open(path, "wb") as f:
        f.write(image.content.read())

    resize_image(path, path, 500)
    add_border_and_round_corners(path, path, border_size, corner_radius)
    return


def remove_all_extensions(filename):
    while "." in filename:
        filename = filename.rsplit(".", 1)[0]
    return filename


def append_unique_item(my_list, item):
    # Check if the item is already in the list
    if item not in my_list:
        my_list.append(item)
        my_list.sort()
        
    #  This exists so that the Upload Custom Flag is always on top
        try:
            my_list.remove("Upload Custom Flag")
        except:
            print("")
        my_list.insert(0, "Upload Custom Flag")
        with open(LOCATION_LIST_PATH, "w", encoding="utf-8") as file:
            json.dump(my_list, file, indent=2, ensure_ascii= False)
        print(f"Item {item} added.")
    else:
        print(f"Item {item} already exists.")
