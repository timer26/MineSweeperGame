import time
from modules.render import render_menu, final_render, get_data_snapshot
from modules.handlers import menu_handler
from global_data.global_context import Context
from global_data.metric import Log

def run_menu(menu_content: dict, spacing: int, name_of_section: str):
    render_menu(spacing, name_of_section, list(menu_content))
    Log.add(F"Switched to {name_of_section}", level="DEBUG")
    while True:
        final_render("menu cursor")
        result = menu_handler(menu_content)
        if result in menu_content:
            menu_content[result]()
            break  # Exit current menu after valid selection
        elif result not in menu_content:
            Log.add(f"Nothing has been selected in {name_of_section}", level="DEBUG")
        else:
            Log.add(f"Invalid selection: '{result}' in {name_of_section}", level="ERROR")
            
def spacing_definition(content: dict) -> int:
    return len(max(content, key=len)) + 3

# === Menu Definitions ===
def start_game():
    menu_content = {
            "start_game": lambda: None,
            "difficulty": difficulty,
            "settings": settings,
            "end_game": end_game,
    }
    run_menu(menu_content, spacing_definition(menu_content), "start_game")

def difficulty():
    menu_content = {
            "easy": lambda: None,
            "medium": lambda: None,
            "hard": lambda: None,
            "back": main_menu,
    }
    run_menu(menu_content, spacing_definition(menu_content), "difficulty")

def grid_settings():
    menu_content = {
            "10x10": lambda: None,
            "20x20": lambda: None,
            "30x30": lambda: None,
            "custom": lambda: None,
            "back": settings,
    }
    run_menu(menu_content, spacing_definition(menu_content), "grid_settings")

def settings():
    menu_content = {
            "difficulty": difficulty,
            "grid_settings": grid_settings,
            "log_settings": lambda: None,
            "back": main_menu,
    }
    run_menu(menu_content, spacing_definition(menu_content), "settings")

def end_game():
    render_menu(20, "end_game", ["Thanks for playing!"])
    Log.add("switched to menu = end_game", level="DEBUG")
    time.sleep(3)
    exit()

def main_menu():
    menu_content = {
            "start_game": start_game,
            "settings": settings,
            "end_game": end_game,
    }
    run_menu(menu_content, spacing_definition(menu_content), "MAIN MENU")