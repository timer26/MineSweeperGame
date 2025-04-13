from keyboard.mouse import get_position

from GlobalServices.GlobalData import Context
from GlobalServices.GlobalHelpers import user_input_handler



def menu_handler():
    current_menu_name = Context.current_menu_position
    menu_data = Context.menus[current_menu_name]
    menu_content = [
            line.strip(" |") for line in menu_data["rendered_menu"][2:]
    ]
    position_modifier = menu_data["position_modifier"]
    selected_index = Context.current_position[1] - position_modifier["y_start"]

    selected_key = menu_content[selected_index]
    result = user_input_handler()

    if result == "enter":
        Context.last_menu_position.append(current_menu_name)
        Context.current_menu_position = selected_key

        if selected_key in Context.menus:
            # Just update context — no rendering
            menu_data = Context.menus[selected_key]
            Context.temporary_render = menu_data["rendered_menu"]
            Context.position_modifier = menu_data["position_modifier"]
            Context.current_position = (
                    Context.position_modifier["x_start"],
                    Context.position_modifier["y_start"],
            )
        elif selected_key in ["easy", "medium", "hard"]:
            difficulty_setter(selected_key)
            Context.current_menu_position = Context.last_menu_position.pop()
        elif selected_key == "end_game":
            end_game()

    elif result == "esc":
        Context.current_menu_position = "main_menu"
        menu_data = Context.menus["main_menu"]
        Context.temporary_render = menu_data["rendered_menu"]
        Context.position_modifier = menu_data["position_modifier"]
        Context.current_position = (
                Context.position_modifier["x_start"],
                Context.position_modifier["y_start"],
        )

    elif result == "backspace":
        if Context.last_menu_position:
            Context.current_menu_position = Context.last_menu_position.pop()
            menu_data = Context.menus[Context.current_menu_position]
            Context.temporary_render = menu_data["rendered_menu"]
            Context.position_modifier = menu_data["position_modifier"]
            Context.current_position = (
                    Context.position_modifier["x_start"],
                    Context.position_modifier["y_start"],
            )
