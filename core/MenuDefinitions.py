import time
from GlobalServices.GlobalData import Context
from services.Renders import MenuRender
Context = Context()




def run_menu(menu_content: list, spacing: int, name_of_section: str):

    render_menu(spacing, name_of_section, menu_content)
    while True:
        final_render("menu_cursor")
        menu_handler(menu_content)
# menu functions----------------------------------------------------
def back():
    data.set_menu_position(data.get_last_menu_position())


def difficulty_setter(difficulty: str):
    if difficulty == "easy":
        Context.difficulty = 1
    elif difficulty == "medium":
        Context.difficulty = 1.5
    elif difficulty == "hard":
        Context.difficulty = 2
    
# menu pathing -----------------------------------------------------
def start_game()-> tuple[tuple[str,...], int, str]:
    menu_content = (
            "start_game",
            "difficulty",
            "settings",
            "end_game",
    )

    spacing = 15
    name_of_section = "start_game"
    return menu_content, spacing, name_of_section

def difficulty():
    menu_content = [
            "easy",
            "medium",
            "hard",
            "back"
    ]

    spacing = 15
    name_of_section = "difficulty"
    return menu_content, spacing, name_of_section

def settings()-> tuple[tuple[str,...], int, str]:
    menu_content = (
            "metrics_analyze",
            "difficulty",
            "back",
    )

    spacing = 15
    name_of_section = "settings"
    return menu_content, spacing, name_of_section
def end_game():
    menu_content ="Thanks for playing!"
    len(menu_content)
    spacing = (15 - len(menu_content)) // 2
    print(spacing*" " + menu_content + spacing*" ")
    
    time.sleep(3)
    exit()


def main_menu()-> tuple[tuple[str,...], int, str]:
    menu_content = (
            "start_game",
            "settings",
            "end_game",
    )

    spacing = 15
    name_of_section = "MAIN MENU"
    return menu_content, spacing, name_of_section


class MenuBuilder:
    def __init__(self, context: Context):
        self.context = context
        self.menu_render = MenuRender(context)
        self.menu_functions = {
                "main_menu": main_menu,
                "start_game": start_game,
                "difficulty": difficulty,
                "settings": settings,
                "end_game": end_game,
                "back": back,
                "easy": difficulty_setter,
                "medium": difficulty_setter,
                "hard": difficulty_setter,
        }
        self.built_menus = self.build_menus()
        self.context.menus = self.built_menus 

    def build_menus(self) -> dict[str, dict]:
        pre_rendered_menus = {}

        for name, func in self.menu_functions.items():
            if name in ["back", "easy", "medium", "hard"]:
                continue

            menu_content, spacing, name_of_section = func()
            position_modifier, rendered_menu = self.menu_render.render_menu(
                    spacing, name_of_section, menu_content
            )

            pre_rendered_menus[name] = {
                    "name": name,
                    "position_modifier": position_modifier,
                    "rendered_menu": rendered_menu
            }

        return pre_rendered_menus