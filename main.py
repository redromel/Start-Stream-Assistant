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


    event_select.disable()
    phase_select.disable()
    stream_select.disable()

    # Styling stuff
    ui.dark_mode().enable()
    ui.colors(primary="#8d0ebf")


if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run()
