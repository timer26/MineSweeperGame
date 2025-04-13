

import os
from GlobalServices.GlobalData import Context, PositionModifier
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
class MenuRender:
    def __init__(self, context: Context):
        self.context = context

    def render_menu(self, spacing: int, name_of_section: str, menu_content: list[str])-> tuple[dict[str: int], str]:
        generate_menu = [
                name_of_section + " " * (spacing - len(name_of_section)) + "|",
                "-" * spacing
        ]
        top_restriction = len(generate_menu)

        for value in menu_content:
            generate_menu.append(value + " " * (spacing - len(value)) + "|")

        self.context.temporary_render = generate_menu

        range_y = len(generate_menu)
        position_modifier = {
                "x_min": spacing,
                "x_max": spacing,
                "y_min": top_restriction,
                "y_max": range_y,
                "x_start": spacing,
                "y_start": top_restriction,
        }
        
        return position_modifier, generate_menu

        
def render_board():
    pass
def render_user(render_object: list, sprite: str):
    position_2D = Context.current_position
    line = render_object[position_2D[1]]
    line = list(line)
    line[position_2D[0]] = sprite
    render_object[position_2D[1]] = ''.join(line)
    return render_object




# metric data need switch from settings
def final_render(sprite: str):
    clear_console()
    metric_offset = 10
    rendered_lines = data.get_rendered_area().copy()
    rendered_with_cursor = render_user(rendered_lines, data.get_sprites()[sprite])

    metric_data = data.get_metric_data()
    max_lines = max(len(rendered_with_cursor), len(metric_data))

    for i in range(max_lines):
        line = rendered_with_cursor[i] if i < len(rendered_with_cursor) else ""

        if i < len(metric_data):
            metric_dict = metric_data[i]
            key, value = list(metric_dict.items())[0]
            metric = f"{key} : {value}"
        else:
            metric = ""


        padded_line = line.ljust(data.get_position_modifier()["x_max"]+metric_offset)
        print(f"{padded_line}{"||- "}{metric}")

    data.clear_metric_data()
