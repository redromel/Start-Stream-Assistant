# *Scoreboard Stuff
from collections import Counter
from event_listner import extract_slug, send_mutation
from queries import *
from query_parser import *
from scoreboard_utils import append_unique_item, change_text, swap_player_files, swap_players, upload_flag, remove_all_extensions
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
            on_change=lambda e: change_text(e.value, path=ROUND_PATH),
        )

        self.player_1_input = ui.input(
            label="Player 1",
            on_change=lambda e: change_text(e.value, path=P1_GAMERTAG_PATH),
        )

        self.player_1_score = ui.number(
            "P1 Score",
            min=0,
            precision=0,
            value=0,
        )

        with open(LOCATION_LIST_PATH, "r", encoding="utf-8") as file:
            self.flag_options = json.load(file)

        self.player_1_flag = ui.select(
            label="P1 Flag", options=self.flag_options, with_input=True, value=None
        ).classes("w-40")

        self.player_2_flag = ui.select(
            label="P2 Flag", options=self.flag_options, with_input=True, value=None
        ).classes("w-40")

        self.player_2_input = ui.input(
            label="Player 2",
            on_change=lambda e: change_text(e.value, path=P2_GAMERTAG_PATH),
        )

        self.player_2_score = ui.number(
            "P2 Score",
            min=0,
            precision=0,
            value=0,
        )
        self.grab_match_switch = ui.switch(
            "Streamed Match Listener",
        )
        self.swap_button = ui.button(
            "Swap Players",
        )

        self.reset_button = ui.button("Reset")

        self.report_score_button = ui.button("Report Score")

        self.player_1_score.on_value_change(
            lambda e: self.handle_mutate_score(e, player=1, path=P1_SCORE_PATH)
        )
        self.player_2_score.on_value_change(
            lambda e: self.handle_mutate_score(e, player=2, path=P2_SCORE_PATH)
        )

        self.report_score_button.on_click(self.get_confirm_dialog)
        self.swap_button.on_click(self.handle_swap_player_ui)
        self.reset_button.on_click(self.reset_scoreboard)

        # self.report_score_button.disable()

        self.player_1_flag.on_value_change(lambda e: self.handle_set_flag(e, player=1))
        self.player_2_flag.on_value_change(lambda e: self.handle_set_flag(e, player=2))

    async def get_set(self, sender):

        self.player_1_input.update()
        self.player_2_input.update()
        self.player_1_score.update()
        self.player_2_score.update()

        set_count = f"{self.player_1_input.value} | {self.player_1_score.value} - {self.player_2_score.value} | {self.player_2_input.value}"

        with ui.dialog() as confirm, ui.card(align_items="center").classes("w-40"):
            ui.label(
                "Pressing Confirm will Report the Entire Set.  Do you want to report this set?"
            ).classes("text-wrap")
            ui.label(set_count)

            with ui.grid(columns=2):
                confirm_button = (
                    ui.button("Confirm").props("color=green").classes("w-full")
                )
                exit_button = (
                    ui.button("Exit", on_click=confirm.close)
                    .props("color=red")
                    .classes("w-full")
                )
                confirm_button.on_click(
                    lambda e: self.handle_report_match(e, dialog=confirm)
                )
        confirm.open()

    async def get_confirm_dialog(self, e):
        await self.get_set(e.sender)

    async def handle_report_match(self, e, dialog: ui.dialog):
        await self.report_match(e.sender, dialog)

    async def handle_grab_match_click(self, e, slug):
        await self.get_scoreboard_data(e.sender, slug)

    async def handle_swap_player_ui(self, e):
        await self.swap_player_ui(e.sender)

    async def handle_mutate_score(self, e, player, path):
        await self.mutate_score(e.sender, player, path)

    async def handle_set_flag(self, e, player):
        await self.set_flag(e.sender, player)

    async def get_scoreboard_data(self, sender, slug):

        print(self.grab_match_switch.value)
        if self.grab_match_switch.value == False:
            await self.unlock_scoreboard()
            return

        if self.stream_select.value == [] or self.stream_select.value == 0:
            ui.notify("No Matches Available")
            self.grab_match_switch.set_value(False)
            return
        try:
            scoreboard = self.get_scoreboard(slug)

            await self.write_players_json(scoreboard)

            await self.lock_scoreboard()

        except:
            self.grab_match_switch.value = False
            ui.notify("No Matches Available")
            return

    async def swap_player_ui(self, sender):

        p1_flag = self.player_1_flag.value
        p2_flag = self.player_2_flag.value

        print(f"BEFORE  P1:  {p1_flag} | P2: {p2_flag}")

        if self.grab_match_switch.value == True:
            scoreboard = swap_players()
            await self.write_players_json(scoreboard)

            self.player_1_flag.value = p2_flag
            self.player_2_flag.value = p1_flag

            self.player_1_flag.update()
            self.player_2_flag.update()
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

            self.player_1_flag.value = p2_flag
            self.player_2_flag.value = p1_flag

            self.player_1_score.update()
            self.player_1_input.update()
            self.player_2_score.update()
            self.player_2_input.update()
            self.player_1_flag.update()
            self.player_2_flag.update()

    async def lock_scoreboard(self):
        self.round_input.disable()
        self.player_1_input.disable()
        self.player_2_input.disable()
        self.report_score_button.enable()

    async def unlock_scoreboard(self):
        self.round_input.enable()
        self.player_1_input.enable()
        self.player_2_input.enable()
        self.report_score_button.disable()
        self.grab_match_switch.value = False

    async def reset_scoreboard(self):

        if self.grab_match_switch.value == False:
            self.round_input.value = ""
            self.player_1_input.value = ""
            self.player_2_input.value = ""
        self.player_1_score.value = 0
        self.player_2_score.value = 0

    async def mutate_score(self, sender, player, path):

        try:
            p1_score = int(self.player_1_score.value)
            p2_score = int(self.player_2_score.value)

            player_1 = self.player_1_input.value
            player_2 = self.player_2_input.value

            if self.grab_match_switch.value == False:
                input = p1_score if player == 1 else p2_score
                await change_text(input, path)
                return

            else:
                mutation_vars = await mutation_writer(p1_score, p2_score)
                await send_mutation(mutation_vars)

                await score_writer(p1_score, p2_score, player_1, player_2)
                return
        except Exception as e:
            print(e)
            return

    async def write_players_json(self, scoreboard):

        player_1 = scoreboard["players"][0]
        player_2 = scoreboard["players"][1]
        self.round_input.value = scoreboard["round"]
        self.player_1_input.value = player_1["gamertag"]
        self.player_1_score.value = player_1["score"]
        self.player_2_input.value = player_2["gamertag"]
        self.player_2_score.value = player_2["score"]

        if player_1["state"] is not None:
            self.player_1_flag.value = player_1["state"]
        elif player_1["country"] is not None:
            self.player_1_flag.value = player_1["country"]
        else:
            self.player_1_flag.value = None

        if player_2["state"] is not None:
            self.player_2_flag.value = player_2["state"]
        elif player_2["country"] is not None:
            self.player_1_flag.value = player_2["country"]
        else:
            self.player_2_flag.value = None

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

    async def report_match(self, sender, dialog):
        with open(MATCH_MUTATION_PATH, "r", encoding="utf-8") as file:
            mutation_json = json.load(file)

        if int(self.player_1_score.value) == 0 and int(self.player_2_score.value) == 0:
            ui.notify("There is no Winner")
            dialog.close()
            return

        winnerIds = [players["winnerId"] for players in mutation_json["gameData"]]
        winnerId_count = Counter(winnerIds)

        print(winnerId_count)
        print(winnerId_count.keys())
        print(winnerId_count.values())

        key_count = list(winnerId_count.keys())
        value_count = list(winnerId_count.values())

        if len(value_count) == 1:
            mutation_json["winnerId"] = key_count[0]
        elif value_count[0] > value_count[1]:
            mutation_json["winnerId"] = key_count[0]
        elif value_count[0] < value_count[1]:
            mutation_json["winnerId"] = key_count[1]
        else:
            ui.notify("There is no Winner")
            dialog.close()
            return

        try:
            await send_mutation(mutation_json)
            ui.notify("Set Data Reported")
            await self.unlock_scoreboard()
            await self.reset_scoreboard()
            dialog.close()
            return
        except:
            ui.notify("Set Data Failed to report")
            dialog.close()
            return

    async def set_flag(self, sender, player):

        print(f"Player {player}:  {sender.value}")

        destination_path = f"match_info/player_{player}_info/player_{player}_flag.png"
        flag_path = f"utils/flags/{sender.value}.png"

        if sender.value == None:
            transparent_image = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
            transparent_image.save(destination_path)
            return
        if sender.value == "Upload Custom Flag":
            await self.upload_custom_flag_popup(player)
            return

        try:
            shutil.copy(flag_path, destination_path)
        except:
            ui.notify("Flag not Found")

    async def upload_custom_flag_popup(self, player):
        with ui.dialog() as dialog, ui.card(align_items="center").style(
            "height: 600px; width: 386px;"
        ):

            with ui.card_section().classes("gap-y-10"):
                ui.label("Upload Custom Flag").classes("text-3xl").classes(
                    "font-bold"
                ).classes("text-center").classes("leading-loose")
                ui.label(
                    "If image does not already have a border or have rounded corners, click the applicable checkboxes"
                ).classes("text-xs").classes("italic").classes("text-center").classes(
                    "align-baseline"
                ).classes(
                    "leading-relaxed"
                )
            ui.separator()
            flag_name = ui.input(label="Flag Name").props("size=100")
            with ui.grid(columns=2).classes("gap-x-10"):
                corner = ui.checkbox("Round Corners")
                border = ui.checkbox("Add Border")
            ui.upload(
                on_upload=lambda e: self.handle_file_accept(
                    e, flag_name.value, corner.value, border.value, player, dialog
                ),
                on_rejected=self.handle_file_reject,
                max_file_size=60_000,
            ).classes("h-full").props("accept= .jpg").props("accept= .png").props(
                "accept= .jpeg"
            )
            ui.card_actions()
        dialog.open()

    async def handle_file_reject(self):
        ui.notify("Invalid File", type="negative")
        return

    async def handle_file_accept(self, image, flag_name, corner, border, player, dialog):

        corner_radius = 30
        border_size = 10

        if corner == False:
            corner_radius = 0
        if border == False:
            border_size = 0

        if flag_name == "":
            flag_name = remove_all_extensions(image.name)

        try:
            upload_flag(image, flag_name, border_size, corner_radius)
            ui.notify(f"File uploaded successfully: {image.name}", type="positive")
        except:
            ui.notify("Upload Failed", type="negative")
            return
        
        await self.set_flag_options(flag_name,player)    

        dialog.close()
        
    async def set_flag_options(self, flag_name, player):
        
        append_unique_item(self.flag_options,flag_name)
    
            
        if player == 1:
            self.player_1_flag.set_options(options=self.flag_options, value=flag_name)
            player_2_flag = self.player_2_flag.value
            self.player_2_flag.set_options(
                options=self.flag_options, value=player_2_flag
            )
        if player == 2:
            self.player_2_flag.set_options(options=self.flag_options, value=flag_name)
            player_1_flag = self.player_1_flag.value
            self.player_1_flag.set_options(
                options=self.flag_options, value=player_1_flag
            )
            
        self.player_1_flag.update()
        self.player_2_flag.update()



