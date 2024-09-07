# *Scoreboard Stuff
from event_listner import extract_slug, send_mutation
from queries import *
from query_parser import *
from writer import *
from nicegui import ui
from constants import *


class Scoreboard_Components:
    def __init__(self):

        self.stream_select = ui.select(
            label="Select Stream",
            options=["Insert Slug"],
            on_change=lambda e: print(e.value),
            value=[],
        ).classes("w-60")

        self.round_input = ui.input(
            label="Round",
            on_change=lambda e: change_text(e.value, path="match_info\match_round.txt"),
        )

        self.player_1_input = ui.input(
            label="Player 1",
            on_change=lambda e: change_text(
                e.value, path="match_info\player_1_gamertag.txt"
            ),
        )

        self.player_1_score = ui.number(
            "P1 Score",
            min=0,
            precision=0,
            value=0,
        )

        self.player_2_input = ui.input(
            label="Player 2",
            on_change=lambda e: change_text(
                e.value, path="match_info\player_2_gamertag.txt"
            ),
        )

        self.player_2_score = ui.number(
            "P2 Score",
            min=0,
            precision=0,
            value=0,
        )
        self.grab_match_button = ui.button(
            "Grab Matches",
        )
        self.swap_button = ui.button(
            "Swap Players",
        )

        self.report_score_button = ui.button("Report Score")

        self.swap_button.on_click(self.handle_swap_player_ui)

    async def handle_grab_match_click(self, e, slug):
        await self.get_scoreboard_data(e.sender, slug)

    async def handle_swap_player_ui(self, e):
        await self.swap_player_ui(e.sender)

    async def handle_mutate_score(self, e, player, path, slug):
        await self.mutate_score(e.sender, player, path, slug)

    async def get_scoreboard_data(self, sender, slug):

        if self.stream_select.value == [] or self.stream_select.value == 0:
            ui.notify("No Matches Available")
            return

        try:
            scoreboard = self.get_scoreboard(slug)

            await self.write_players_json(scoreboard)

            self.grab_match_button.disable()
            self.round_input.disable()
            self.player_1_input.disable()
            self.player_2_input.disable()
            self.report_score_button.enable()
        except:
            ui.notify("No Matches Available")
            return

    async def swap_player_ui(self, sender):
        print(self.grab_match_button.enabled)
        if self.grab_match_button.enabled == False:
            scoreboard = swap_players()
            await self.write_players_json(scoreboard)
            return

        else:
            swap_player_files()

            self.player_1_input.value, self.player_2_input.value = (
                self.player_2_input.value,
                self.player_1_input.value,
            )

            self.player_1_score.value, self.player_2_score.value = (
                self.player_2_score.value,
                self.player_1_score.value,
            )

            self.player_1_score.update()
            self.player_1_input.update()
            self.player_2_score.update()
            self.player_2_input.update()

    async def mutate_score(self, sender, player, path, slug):

        p1_score = int(self.player_1_score.value)
        p2_score = int(self.player_2_score.value)

        player_1 = self.player_1_input.value
        player_2 = self.player_2_input.value

        print(self.grab_match_button.enabled)
        if self.grab_match_button.enabled == True:
            input = p1_score if player == 1 else p2_score
            await change_text(input, path)
            return

        else:
            mutation_vars, numId = await mutation_writer(
                p1_score, p2_score, player_1, player_2
            )
            await send_mutation(mutation_vars)

            await score_writer(p1_score, p2_score, player_1, player_2)
            return

    # Will write the score locally because it conflicts with the swap players function

    async def write_players_json(self, scoreboard):

        player_1 = scoreboard["players"][0]
        player_2 = scoreboard["players"][1]
        self.round_input.value = scoreboard["round"]
        self.player_1_input.value = player_1["gamertag"]
        self.player_1_score.value = player_1["score"]
        self.player_2_input.value = player_2["gamertag"]
        self.player_2_score.value = player_2["score"]

        self.round_input.update()
        self.player_1_input.update()
        self.player_1_score.update()
        self.player_2_input.update()
        self.player_2_score.update()

    def get_scoreboard(self, slug_value):

        tourney_slug = extract_slug(slug_value)
        stream_vars = {"tourneySlug": tourney_slug}
        stream_payload = {"query": STREAM_QUERY, "variables": stream_vars}

        stream_response = requests.post(
            url=API_URL, json=stream_payload, headers=HEADER
        )
        stream_data = stream_parse(stream_response)
        for stream in stream_data:
            if stream["stream"]["streamName"] == self.stream_select.value:
                for set in stream["sets"]:
                    if set["state"] == ONGOING:
                        scoreboard = scoreboard_json_writer(get_set(set["id"]))
                        scoreboard_writer(scoreboard)
                        return scoreboard
        print("no streamed matches")


async def change_text(input, path):
    with open(path, "w") as file:
        file.write(str(input))
    return


def swap_players():
    with open(MATCH_JSON_PATH, "r") as file:

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
    swap_files("match_info/player_1_gamertag.txt", "match_info/player_2_gamertag.txt")
    swap_files("match_info/player_1_score.txt", "match_info/player_2_score.txt")
    swap_files("match_info/player_1_id.txt", "match_info/player_2_id.txt")
    swap_files("match_info/player_1_state.png", "match_info/player_2_state.png")
    swap_files("match_info/player_1_country.png", "match_info/player_2_country.png")
