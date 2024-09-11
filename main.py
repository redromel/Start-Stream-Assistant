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

    with ui.grid(columns=10).classes(
        "w-full gap-4 justify-items-stretch items-end align-center"
    ):
        slug_input = (
            ui.input(
                label="start.gg URL or Slug",
                placeholder="https://www.start.gg/tournament/name",
            )
            .props("rounded outlined dense")
            .classes("col-start-1 col-span-6")
        )

        slug_button = (
            ui.button(
                "Submit",
                on_click=lambda e: get_tourney_info(
                    e.sender, slug_input, event_select, stream_select, footer
                ),
            )
            .props("rounded outlined dense")
            .classes("col-start-7 col-span-2 self-center")
        )

    with ui.header(elevated=True):
        
        with ui.grid(columns=10).classes("w-full h-10 align-center"):
            footer = ui.label("FGC Stream Assistant").classes(
                "text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-3xl dark:text-white text-align:center col-span-9 self-center")


    with ui.grid(rows=1).classes("w-full gap-3 align-center"):
        ui.space().classes("span-row-1")

    with ui.grid(columns=4):
        event_select = ui.select(
            label="Select Event",
            options=["Insert Slug"],
            on_change=lambda e: get_phases(e, phase_select),
            value=[],
        ).classes("col-span-1 w-full")

        phase_select = ui.select(
            label="Select Phase",
            options=["Insert Slug"],
            on_change=lambda e: get_pools(e, pool_select),
            value=[],
        ).classes("col-span-1 w-full")

        pool_select = ui.select(
            label="Select Pool",
            options=["Insert Slug"],
            on_change=lambda e: print(e.value),
            value=[],
        ).classes("col-span-1 w-full")

        bracket_switch = ui.switch(
            "Bracket Listener",
            on_change=lambda e: bracket_listner(
                e.sender, phase_select, stream_select, slug_input
            ),
        ).classes("col-span-1 w-full")

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


if __name__ in {"__main__", "__mp_main__"}:

    main()
    ui.run(title="FGC Scoreboard Assistant", favicon="🥊")
