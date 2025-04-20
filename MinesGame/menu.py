import time
from modules import render_menu, menu_handler,final_render,get_data_snapshot
from GlobalData.GlobalContext import Context
from GlobalData.Metric import Log




def run_menu(menu_content: list, spacing: int, name_of_section: str):
    render_menu(spacing, name_of_section, menu_content)
    Context.context_trigger +=1
    last_snapshot = get_data_snapshot()

    while True:
        current_snapshot = get_data_snapshot()

        if current_snapshot != last_snapshot:
            final_render("menu_cursor")
            last_snapshot = current_snapshot

        menu_handler(menu_content)

# menu functions----------------------------------------------------
def spacing_definition(content: list)->int:
    return len(max(content, key=len)) + 3
    

# menu pathing -----------------------------------------------------
def start_game():
    menu_content = [
            "start_game",
            "difficulty",
            "settings",
            "end_game",

    ]

    spacing = spacing_definition(menu_content)
    name_of_section = "start_game"
    Log.add(f"switched to menu ={name_of_section}", level="DEBUG")
    run_menu(menu_content, spacing, name_of_section)

def difficulty():
    menu_content = [
            "easy",
            "medium",
            "hard",
            "back",
    ]

    spacing = spacing_definition(menu_content)
    name_of_section = "difficulty"
    Log.add(f"switched to menu ={name_of_section}", level="DEBUG")
    run_menu(menu_content, spacing, name_of_section)
def grid_settings():
    menu_content = [
            "5x5",
            "10x10",
            "20x20",
            "custom",
            "back",

    ]

    spacing = spacing_definition(menu_content)
    name_of_section = "settings"
    Log.add(f"switched to menu ={name_of_section}", level="DEBUG")
    run_menu(menu_content, spacing, name_of_section)
    
def settings():
    menu_content = [
            "difficulty",
            "grid_settings",
            "log_settings"
            "back",
              
    ]

    spacing = spacing_definition(menu_content)
    name_of_section = "settings"
    Log.add(f"switched to menu ={name_of_section}", level="DEBUG")
    run_menu(menu_content, spacing, name_of_section)
    
    
def end_game():
    menu_content =["Thanks for playing!"]
    spacing = spacing_definition(menu_content)
    name_of_section = "end_game"
    render_menu(spacing, name_of_section, menu_content)
    Log.add(f"switched to menu ={name_of_section}", level="DEBUG")
    time.sleep(3)
    exit()


def main_menu():

    #####################---START OF MENU INITIATION---###############
    # initiation of menu API
    menu_content = [
            "start_game",
            "settings",
            "end_game",
    ]

    spacing = 15
    name_of_section = "MAIN MENU"
    Log.add(f"switched to menu ={name_of_section}", level="DEBUG")
    run_menu(menu_content, spacing, name_of_section)


Context.all_menu_functions = {
        "main_menu": main_menu,
        "start_game": start_game,
        "difficulty": difficulty,
        "settings": settings,
        "grid_settings": grid_settings,
        "end_game": end_game,
        # "metrics_analyze"metrics_analyze,
        # "log_settings",
}