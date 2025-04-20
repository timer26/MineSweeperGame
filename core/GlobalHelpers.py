from typing import Literal, Union

from GlobalData.GlobalContext import Context
from pynput import keyboard
from GlobalData.Metric import MetricData, Log
import os



def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    Log.add(message="console has been cleared",level="DEBUG")

def user_input_record(mode: Literal["str", "int", "float"]) -> Union[str, int, float, None]:
    Log.add(message=f"user input record start in MODE {mode}", level="DEBUG")
    Log.add(message="Write value", level="INFO")

    raw_input_val = input()
    result = None

    if mode == "str":
        result = raw_input_val

    elif mode == "int":
        try:
            result = int(raw_input_val)
        except ValueError:
            try:
                float_value = float(raw_input_val)
                rounded_value = int(float_value)
                result = rounded_value
                Log.add(message=f"Your number {float_value} was rounded to {rounded_value}", level="INFO")
                Log.add(message=f"Number {float_value} was rounded to {rounded_value}", level="DEBUG")
            except ValueError:
                Log.add(message=f"Invalid input: {raw_input_val}", level="INFO")
                Log.add(message=f"Invalid input: {raw_input_val} requires Int", level="ERROR")

    elif mode == "float":
        try:
            result = float(raw_input_val)
        except ValueError:
            Log.add(message=f"Invalid input: {raw_input_val}", level="INFO")
            Log.add(message=f"Invalid input: {raw_input_val} requires Float", level="ERROR")

    Log.add(message=f"user input record has finished with result: {result}", level="DEBUG")
    return result
    
    
def user_input_on_press() -> str or None:
    Log.add(message=f"user input on press has started", level="DEBUG")
    pressed_key = []

    def on_press(key):
        try:
           
            if hasattr(key, "char") and key.char is not None:
                k = key.char.lower()
            
            elif hasattr(key, "name"):
                k = key.name
            else:
                Log.add(message=f"Ignored unknown key input: {key}", level="ERROR")



            valid_keys = {"w", "a", "s", "d", "up", "down", "left", "right", "enter", "esc", "backspace"}

            if k in valid_keys:
                pressed_key.append(k)
                return False 
            else:
                Log.add(message=f"Ignored unsupported key: {k}", level="ERROR")


        except Exception as e:
            Log.add(message=f"Error while processing key: {e}", level="ERROR")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


    user_input = pressed_key[0]
    MetricData.append_metric_data("Last key pressed", user_input)
    Context.metric_data = {"Latest key pressed": pressed_key}
    Log.add(message=f"user input finished whit {user_input} result", level="DEBUG")
    
    if user_input in ("w", "up"):
        Context.vector = [0, -1]
        return Context.vector
    elif user_input in ("s", "down"):
        Context.vector = [0, 1]
        return Context.vector
    elif user_input in ("a", "left"):
        Context.vector = [-1, 0]
        return Context.vector
    elif user_input in ("d", "right"):
        Context.vector = [1, 0]
        return Context.vector
    elif user_input == "enter":
        return "enter"
    elif user_input == "esc":
        return "esc"
    elif user_input == "backspace":
        return "backspace"
    else:
        return None

    
def back():
    if len(Context.last_menu_position_stack) > 1:
        Context.last_menu_position_stack.pop(-1)
        Context.menu_position = Context.last_menu_position_stack[-1]
        Context.all_menu_functions[Context.menu_position]()
    else:
        Context.menu_position = "main_menu"
        Context.all_menu_functions["main_menu"]()
        Log.add(message=f"handled error empty Context.last_menu_position_stack", level="ERROR")
        
        
def push_menu_position(current:str):
    if not Context.last_menu_position_stack or Context.last_menu_position_stack[-1] != current:
        Context.last_menu_position_stack.append(current)
        Log.add(message=f"{current} has been pushed to Context.last_menu_position_stack", level="DEBUG")
        
        
def difficulty_setter(difficulty: str):
    if difficulty == "easy":
        Context.difficulty = "easy"
        Context.difficulty_modifier = 1.0
    elif difficulty == "medium":
        Context.difficulty = "medium"
        Context.difficulty_modifier = 1.5
    elif difficulty == "hard":
        Context.difficulty = "hard"
        Context.difficulty_modifier = 2.0
    Log.add(message=f"difficulty has been changed to {difficulty}", level="INFO")
        
def grid_setter(chosed: str):
    
    if chosed == "5x5":
        Context.grid_width = 5
        Context.grid_height = 5
    
    elif chosed == "10x10":
        Context.grid_width = 10
        Context.grid_height = 10
    elif chosed == "20x20":
        Context.grid_width = 20
        Context.grid_height = 20
    elif chosed == "custom":
        Log.add(message="insert custom wight",level="INFO")
        inserted_number = user_input_record("int")
        Log.add(message=f"inserted width: {inserted_number}",level="INFO")
        Context.grid_width = inserted_number

        Log.add(message="insert custom height",level="INFO")
        inserted_number = user_input_record("int")
        Log.add(message=f"inserted height: {inserted_number}",level="INFO")
        Context.grid_height = inserted_number
        
        
        
            
