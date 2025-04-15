import time
from _pyrepl.commands import backspace

from modules import *
from GlobalData.GlobalContext import Context
from pynput import keyboard
from GlobalData.GlobalHelpers import *
def user_input_handler() -> str:
    pressed_key = []

    def on_press(key):
        try:
            k = key.char.lower()
        except AttributeError:
            k = key.name  # Handle special keys like "enter", "esc", etc.

        valid_keys = {"w", "a", "s", "d", "up", "down", "left", "right", "enter", "esc", "backspace"}
        if k in valid_keys:
            pressed_key.append(k)
            return False  # Stop the listener

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    user_input = pressed_key[0]
    MetricData.append_metric_data("Last key pressed", user_input)
    Context.metric_data = {"Latest key pressed": pressed_key}   #sending data to metric storage
    
    if user_input in ("w", "up"):
        Context.vector = [0, -1]
        position_handler()
        return Context.vector
    elif user_input in ("s", "down"):
        Context.vector = [0, 1]
        position_handler()
        return Context.vector
    elif user_input in ("a", "left"):
        Context.vector = [-1, 0]
        position_handler()
        return Context.vector
    elif user_input in ("d", "right"):
        Context.vector = [1, 0]
        position_handler()
        return Context.vector
    elif user_input == "enter":
        return "enter"
    elif user_input == "esc":
        return "esc"
    elif user_input == "backspace":
        return "backspace"
    else:
        return None  # Fallback in case of unexpected input

def position_handler() -> list:
    x, y = Context.position_2D
    dx, dy = Context.vector
    x += dx
    y += dy

    modifier = Context.position_modifier
    x = max(modifier["x_min"], min(x, modifier["x_max"]))
    y = max(modifier["y_min"], min(y, modifier["y_max"] - 1))

    Context.position_2D = [x, y]
    return Context.position_2D

def forced_position_handler(forced_position: list) -> list:
    Context.position_2D = list(forced_position)
    return Context.position_2D

def menu_handler(menu_content: list):
    selected_option = Context.position_2D[1] - Context.position_modifier["y_start"]
    selected_key = menu_content[selected_option]
    MetricData.append_metric_data("Selected menu option", selected_key)
    
    result = user_input_handler()
    if result == "enter":
        if Context.menu_position == "difficulty":
            difficulty_setter(selected_key)
            menu_handler(menu_content)
        elif selected_key == "back":
            back()
        else:
            push_menu_position(Context.menu_position)
    
            Context.menu_position = selected_key
            Context.all_menu_functions[selected_key]()
    elif result == "esc":
        Context.menu_position = "main_menu"
        Context.all_menu_functions["main_menu"]()
    elif result == "backspace":
        back()
        