# TODO:  Loser Identifier for Grands
# TODO:  Better Error Handling when querying
# TODO:  NiceGUI Implementation for fun
from contextlib import contextmanager

from dotenv import load_dotenv
from event_listner import bracket_listner
from queries import *
from query_parser import *
from writer import *
from nicegui import ui




def main():
  
  # stringo = 'heheho'
  # button = ui.button('Click me!', on_click=lambda: ui.notify('hi'))
  # texto = ui.input(label='Phase',placeholder='Phase')
  
  # # button = ui.button('Full Test', on_click=lambda e: test_funct(e.sender, texto))
  # test_switch = ui.switch('Full Test',on_change=lambda e: bracket_listner(e.sender, texto))
  # ui.label('Top 8 Watcher on').bind_visibility_from(test_switch,'value')

  print("hello")

if __name__ in {"__main__", "__mp_main__"}:
  main()
  # ui.run()