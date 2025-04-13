from GlobalServices.GlobalData import Context
from services import *
from pynput import keyboard

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



    if user_input in ("w", "up"):
        Context(vector = (0,-1))
        position_handler()

    elif user_input in ("s", "down"):
        Context(vector = (0,1))
        position_handler()

    elif user_input in ("a", "left"):
        Context(vector = (-1,0))
        position_handler()

    elif user_input in ("d", "right"):
        Context(vector = (1,0))
        position_handler()
    elif user_input == "enter":
        return "enter"
    elif user_input == "esc":
        return "esc"
    elif user_input == "back":
        return "backspace"
    else:
        return None  # Fallback in case of unexpected input