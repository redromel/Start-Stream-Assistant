# TODO:  Loser Identifier for Grands
# TODO:  Better Error Handling when querying
# TODO:  NiceGUI Implementation for fun
# TODO:  Dropdown Flag Implementation -> State, Coutnry, Custom
# TODO:  Custom Flags (AT THE END)

from dotenv import load_dotenv
from event_listner import *
from queries import *
from query_parser import *
from scoreboard_components import Scoreboard_Components
from writer import *
from nicegui import ui
from constants import *


def main():
    ...

    # #  *Grabbing Events and Phases based on tournament slug
    slug_input = (
        ui.input(
            label="start.gg tournament slug", placeholder="tournament/tournament-name/"
        )
        .props("size=80")
        .props("rounded outlined dense")
    )

    slug_button = ui.button(
        "Submit",
        on_click=lambda e: get_tourney_info(
            e.sender, slug_input, event_select, stream_select
        ),
    )

    event_select = ui.select(
        label="Select Event",
        options=["Insert Slug"],
        on_change=lambda e: get_phases(e, phase_select),
        value=[],
    ).classes("w-60")

    phase_select = ui.select(
        label="Select Phase",
        options=["Insert Slug"],
        on_change=lambda e: get_pools(e, pool_select),
        value=[],
    ).classes("w-60")

    pool_select = ui.select(
        label="Select Pool",
        options=["Insert Slug"],
        on_change=lambda e: print(e.value),
        value=[],
    ).classes("w-60")

    ui.separator()

    # *Scoreboard Stuff

    scoreboard = Scoreboard_Components()

    stream_select = scoreboard.stream_select
    grab_matches_switch = scoreboard.grab_match_switch
    player_1_score = scoreboard.player_1_score
    player_2_score = scoreboard.player_2_score
    
    
    grab_matches_switch.on_value_change(
        lambda e: scoreboard.handle_grab_match_click(
            e, slug=extract_slug(slug_input.value)
        )
    )



    # stream_select = ui.select(
    #     label="Select Stream",
    #     options=["Insert Slug"],
    #     on_change=lambda e: print(e.value),
    #     value=[],
    # ).classes("w-60")

    # round = ui.input(
    #     label="Round",
    #     on_change=lambda e: change_text(e.value, path="match_info\match_round.txt"),
    # )
    # player_1_input = ui.input(
    #     label="Player 1",
    #     on_change=lambda e: change_text(
    #         e.value, path="match_info\player_1_gamertag.txt"
    #     ),
    # )
    # player_1_score = ui.number(
    #     "P1 Score",
    #     min=0,
    #     precision=0,
    #     value=0,
    #     on_change=lambda e: mutate_score(
    #         p1_score=int(e.value),
    #         p2_score=int(player_2_score.value),
    #         player_1=player_1_input.value,
    #         player_2=player_2_input.value,
    #         player = 1,
    #         path="match_info\player_1_score.txt",
    #         match_button=grab_match_button,
    #     ),
    # )

    # player_2_input = ui.input(
    #     label="Player 2",
    #     on_change=lambda e: change_text(
    #         e.value, path="match_info\player_2_gamertag.txt"
    #     ),
    # )

    # player_2_score = ui.number(
    #     "P2 Score",
    #     min=0,
    #     precision=0,
    #     value=0,
    #     on_change=lambda e: mutate_score(
    #         p1_score=int(player_1_score.value),
    #         p2_score=int(e.value),
    #         player = 2,
    #         player_1=player_1_input.value,
    #         player_2=player_2_input.value,
    #         path="match_info\player_2_score.txt",
    #         match_button=grab_match_button,
    #     ),
    # )
    # grab_match_button = ui.button(
    #     "Grab Matches",
    #     on_click=lambda e: get_scoreboard_data(
    #         e.sender,
    #         report_score_button,
    #         slug_input.value,
    #         round,
    #         player_1_input,
    #         player_1_score,
    #         player_2_input,
    #         player_2_score,
    #         stream_select,
    #     ),
    # )
    # swap_button = ui.button(
    #     "Swap Players",
    #     on_click=lambda: swap_player_ui(
    #         round,
    #         player_1_input,
    #         player_1_score,
    #         player_2_input,
    #         player_2_score,
    #         grab_match_button,
    #     ),
    # )

    # report_score_button = ui.button("Report Score", on_click=lambda e: report_score())

    # if grab_match_button.enabled == True:
    #     report_score_button.disable()
    # else:
    #     report_score_button.enable()

    event_select.disable()
    phase_select.disable()
    stream_select.disable()

    # Styling stuff
    ui.dark_mode().enable()
    ui.colors(primary="#8d0ebf")


if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run()
