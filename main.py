# TODO:  Loser Identifier for Grands
# TODO:  Better Error Handling when querying
# TODO:  NiceGUI Implementation for fun
# TODO:  Dropdown Flag Implementation -> State, Coutnry, Custom
# TODO:  Custom Flags (AT THE END)
# TODO:  Figure out edge Case where Stream isn't added until later

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
            label="start.gg URL or Slug",
            placeholder="https://www.start.gg/tournament/name",
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

    bracket_switch = ui.switch(
        "Bracket Listener",
        on_change=lambda e: bracket_listner(
            e.sender, phase_select, stream_select, slug_input
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

    grab_matches_switch.on_value_change(
        lambda e: scoreboard.handle_grab_match_click(
            e, slug=extract_slug(slug_input.value)
        )
    )
    ui.scroll_area().classes("h-1/2")

    event_select.disable()
    phase_select.disable()
    stream_select.disable()

    # Styling stuff
    ui.dark_mode().enable()
    ui.colors(primary="#8d0ebf")
    ui.query("body").style(
        "background-image: url(https://github.com/redromel/Top-8-Graphic-Maker/blob/master/utils/ggbackground-03.jpg)").style("background-size: 600px 600px")


if __name__ in {"__main__", "__mp_main__"}:

    main()
    ui.run(title="FGC Scoreboard Assistant", favicon="🥊")
