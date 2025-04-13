from keyboard.mouse import get_position

from GlobalServices.GlobalData import Context
from GlobalServices.GlobalHelpers import user_input_handler


def menu_handler(menu_content: list):
    selected_option = data.get_position_2D()[1] - data.get_position_modifier()["y_start"]
    result = user_input_handler()
    selected_key = menu_content[selected_option]

    data.set_metric_data({"Current menu": data.get_menu_position()})
    data.set_metric_data({"Previous menu": data.get_last_menu_position()})
    data.set_metric_data({"Menu stack": list(data._last_menu_position)})
    if result == "enter":
        current_menu = data.get_menu_position()
        data.set_last_menu_position(current_menu)  # Push current menu to stack
        data.set_menu_position(selected_key)
        data.get_all_menu_functions()[selected_key]()
    elif result == "esc":
        data.set_menu_position("main_menu")
        data.get_all_menu_functions()["main_menu"]()
    elif result == "backspace":
        data.get_all_menu_functions()["back"]()