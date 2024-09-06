# *Scoreboard Stuff
from event_listner import extract_slug, write_players_json
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

        # self.grab_match_button.on_click(self.handle_grab_match_click, slug )

    async def handle_grab_match_click(self, e, slug):
        # print(e.sender)
        await self.get_scoreboard_data(e.sender, slug)

    async def get_scoreboard_data(self, sender, slug):

        if self.stream_select.value == [] or self.stream_select.value == 0:
            ui.notify("No Matches Available 1")
            return

        # try:
        scoreboard = get_scoreboard(self.stream_select.value, slug)

        await write_players_json(
            scoreboard,
            self.round_input,
            self.player_1_input,
            self.player_1_score,
            self.player_2_input,
            self.player_2_score,
        )

        self.grab_match_button.disable()
        self.round_input.disable()
        self.player_1_input.disable()
        self.player_2_input.disable()
        self.report_score_button.enable()
        # except:
        #     ui.notify("No Matches Available")
        #     return


def get_scoreboard(stream_name, slug_value):

    tourney_slug = extract_slug(slug_value)
    stream_vars = {"tourneySlug": tourney_slug}
    stream_payload = {"query": STREAM_QUERY, "variables": stream_vars}

    stream_response = requests.post(url=API_URL, json=stream_payload, headers=HEADER)
    stream_data = stream_parse(stream_response)
    for stream in stream_data:
        if stream["stream"]["streamName"] == stream_name:
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
