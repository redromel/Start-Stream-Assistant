# TODO:  Loser Identifier for Grands
# TODO:  Better Error Handling when querying
# TODO:  NiceGUI Implementation for fun
# TODO:  Dropdown Flag Implementation -> State, Coutnry, Custom
# TODO:  Custom Flags (AT THE END)
# TODO:  Figure out edge Case where Stream isn't added until later

from dotenv import load_dotenv
from bracket_listen import Bracket_Listen
from event_listner import *
from queries import *
from query_parser import *
from scoreboard_components import Scoreboard_Components
from writer import *
from nicegui import ui
from constants import *


def main():
    ...

    with ui.header(elevated=True):

        with ui.grid(columns=10).classes("w-full h-10 align-center"):
            header = ui.label("FGC Stream Assistant").classes(
                "text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-3xl dark:text-white text-align:center col-span-9 self-center"
            )

    # #  *Grabbing Events and Phases based on tournament slug

    with ui.row().classes(
        "w-full justify-center"
    ):
        slug_input = (
            ui.input(
                label="start.gg URL or Slug",
                placeholder="https://www.start.gg/tournament/name",
            )
            .props("rounded outlined dense")
            .classes("w-1/3 min-w-96")
        )

        slug_button = (
            ui.button(
                "Submit",
                on_click=lambda e: get_tourney_info(
                    e.sender, slug_input, event_select, stream_select, header
                ),
            )
            .props("rounded outlined dense")
            .classes("w-1/12 min-w-20")
        )

    with ui.grid(rows=1).classes("w-full gap-3 align-center"):
        ui.space().classes("span-row-1")

    with ui.tabs().classes("w-full") as tabs:

        scoreboard_tab = ui.tab("Scoreboard")
        bracket_tab = ui.tab("Bracket Listener")

    # *Scoreboard Stuff

    with ui.tab_panels(tabs, value=scoreboard_tab).classes("w-full"):
        with ui.tab_panel(scoreboard_tab):
            scoreboard = Scoreboard_Components()
            stream_select = scoreboard.stream_select
            grab_matches_switch = scoreboard.grab_match_switch

            grab_matches_switch.on_value_change(
                lambda e: scoreboard.handle_grab_match_click(
                    e, slug=extract_slug(slug_input.value)
                )
            )
            ui.scroll_area().classes("h-1/2")

            stream_select.disable()
        with ui.tab_panel(bracket_tab):
            bracket = Bracket_Listen()
            event_select = bracket.event_select

    # Styling stuff
    ui.dark_mode().enable()


if __name__ in {"__main__", "__mp_main__"}:

    main()
    ui.run(title="FGC Scoreboard Assistant", favicon="🥊")
