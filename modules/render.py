from modules.handlers import forced_position_handler
from GlobalData.GlobalContext import Context
from GlobalData.Metric import MetricData, Log
from core.GlobalHelpers import clear_console
import json

def build_column(name: str, lines: list[str]) -> tuple[str, list[str], int]:
        """
        Returns a column with a header and an underline.
        Format: (name, lines, width)
        """
        width = max(len(line) for line in lines) + 5 if lines else 40
        formatted = [name, "-" * width] + lines
        return (name, formatted, width)

def render_menu(spacing: int, name_of_section: str, menu_content: list):
        Log.add(f"menu {name_of_section} start generate", level="DEBUG")

        generate_menu = [f"{name_of_section}{' ' * (spacing - len(name_of_section))}|"]

        top_restriction = len(generate_menu)

        for value in menu_content:
                generate_menu.append(f"{value}{' ' * (spacing - len(value))}|")

        Context.rendered_area = generate_menu
        range_y = len(Context.rendered_area)

        Context.position_modifier = {
                "x_min": spacing,
                "x_max": spacing,
                "y_min": top_restriction,
                "y_max": range_y,
                "x_start": spacing,
                "y_start": top_restriction,
        }

        Log.add(f"menu {name_of_section} has been generated successfully", level="DEBUG")
        forced_position_handler([spacing, top_restriction])
def render_mine_grid()-> list[list[str]]:
        Log.add(message="Mine Grid generation initialized", level="DEBUG")

        raw_grid = Context.grid.render_grid()
        visual_grid = []

        for row in raw_grid:
                visual_row = []
                for tile in row:
                        visual_row.append(Context.sprites.get(tile, " ? "))
                visual_grid.append(visual_row)

        # Compute grid dimensions early to use them for padding
        range_y = len(visual_grid)
        range_x = len(visual_grid[0]) if range_y > 0 else 0

        # Create and insert padded title row
        title = "MINE SWEEPER"
        padding = max(0, range_x * len(Context.sprites["0"]) - len(title))
        visual_grid.insert(0, [title + " " * padding])

        # Update the rendered area
        Context.rendered_area = visual_grid

        # Position modifier (no need to recompute range_x/range_y again)
        Context.position_modifier = {
                "x_min": 0,
                "x_max": range_x - 1,
                "y_min": 1,
                "y_max": range_y+1,
                "x_start": range_x // 2,
                "y_start": range_y // 2,
        }

        forced_position_handler([range_x // 2, range_y // 2])
        Log.add(message="Mine Grid successfully generated", level="DEBUG")

def render_user(render_object: list, sprite: str) -> list:
        Log.add("user has start generate", level="DEBUG")
        position_2D = Context.position_2D
        line = list(render_object[position_2D[1]])
        line[position_2D[0]] = sprite
        render_object[position_2D[1]] = ''.join(line)

        if render_object and isinstance(render_object[2], list):
                render_object = ["".join(row) for row in render_object]
        
        Log.add("user has been successfully generated", level="DEBUG")
        return render_object








def final_render(sprite: str):
        clear_console()
        Log.add("final render starts", level="DEBUG")

        columns = []

        # === main display ===
        main_display = Context.rendered_area.copy()
        rendered_with_cursor = render_user(main_display, Context.sprites[sprite])
        if rendered_with_cursor and isinstance(rendered_with_cursor[0], list):
                rendered_with_cursor = ["".join(row) for row in rendered_with_cursor]
        
        if rendered_with_cursor:
                underline_length = max(len(line) for line in rendered_with_cursor)
                underline = "-" * underline_length
                rendered_with_cursor.insert(1, underline)

        board_width = max(len(line) for line in rendered_with_cursor) 
        columns.append(("Board", rendered_with_cursor, board_width))

        # === if enabled info log ===
        if getattr(Context, "log_info_state", False):
                columns.append(build_column("INFO TERMINAL", Log.get_log_info()))
        # === if enabled debug log ===
        if getattr(Context, "log_debug_state", False):
                columns.append(build_column("DEBUG TERMINAL", Log.get_log_debug()))
        # === if enabled error log ===
        if getattr(Context, "log_error_state", False):
                columns.append(build_column("ERROR TERMINAL", Log.get_log_error()))
        # === if enabled metric ===
        if getattr(Context, "metric_state", False):
                metric_data_lines = []
                for entry in MetricData.metric_data_all():
                        if isinstance(entry, dict) and entry:
                                key, value = list(entry.items())[0]
                                metric_data_lines.append(f"{key} : {value}")
                columns.append(build_column("METRICS TERMINAL", metric_data_lines))

        # render all
        max_lines = max(len(col[1]) for col in columns)

        for i in range(max_lines):
                line_parts = []
                for _, lines, width in columns:
                        line = lines[i] if i < len(lines) else ""
                        line_parts.append(line.ljust(width))
                
                print(" | ".join(line_parts))

        Log.add("final render has been successful", level="DEBUG")


def get_data_snapshot():
        Log.add("taken snapshot", level="DEBUG")
        return json.dumps({
                "vector": Context.vector,
                "log": Log.log,
                "metrics": MetricData.metric_data_all(),
        }, default=str)
