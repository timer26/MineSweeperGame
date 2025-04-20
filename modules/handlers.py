from global_data.global_context import Context
from global_data.metric import MetricData, Log

from modules import *

from core.global_helpers import (
    user_input_on_press,
    difficulty_setter,
    back,
    push_menu_position,
    grid_setter,
)

    

def position_handler() -> list:
    x, y = Context.position_2D
    dx, dy = Context.vector
    x += dx
    y += dy

    modifier = Context.position_modifier
    x = max(modifier["x_min"], min(x, modifier["x_max"]))
    y = max(modifier["y_min"], min(y, modifier["y_max"] - 1))
    
    Context.position_2D = [x, y]
    Log.add(f"position has been set {x,y}", level="DEBUG")
    return Context.position_2D


def forced_position_handler(forced_position: list) -> list:
    Context.position_2D = list(forced_position)
    Log.add(f"forced position was set {list(forced_position)}", level="DEBUG")
    
    return Context.position_2D


def menu_handler(menu_content: list):
    Log.add(message="Menu handler triggerd", level="DEBUG")
    
    selected_option = Context.position_2D[1] - Context.position_modifier["y_start"]
    selected_key = menu_content[selected_option]
    
    MetricData.append_metric_data("Selected menu option", selected_key)
    
    result = user_input_on_press()
    position_handler()
    
    if result == "enter":
        if Context.menu_position == "difficulty":
            difficulty_setter(selected_key)
        elif selected_key == "back":
            back()
        elif Context.menu_position == "5x5" or "10x10" or "20x20" or "custom":
            grid_setter(selected_key)
        else:
            push_menu_position(Context.menu_position)

            Context.menu_position = selected_key
            Context.all_menu_functions[selected_key]()
    elif result == "esc":
        Context.menu_position = "main_menu"
        Context.all_menu_functions["main_menu"]()
    elif result == "backspace":
        back()
    Log.add(message=f"menu handler ended whit {selected_key} selected",level= "DEBUG" )