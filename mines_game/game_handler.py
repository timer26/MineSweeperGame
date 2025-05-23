
from core.global_helpers import user_input_on_press
from modules.handlers import position_handler
from global_data.global_context import Context
from global_data.metric import MetricData, Log
from mines_game.mines_game import TileGrid, GridInterface
from modules.render import render_mine_grid, final_render, forced_position_handler
from core.timer_API import total_time



def init_mine_sweeper():
    width = Context.grid_width
    height = Context.grid_height
    difficulty_factor = Context.difficulty_modifier

    base_tiles = width * height
    num_mines = max(1, int(base_tiles *  difficulty_factor))

    Log.add(f"Initializing grid {width}x{height} with {num_mines} mines", level="DEBUG")


    Context.grid = TileGrid(num_mines=num_mines, width=width, height=height)
    Context.raw_grid = render_mine_grid()

    MetricData.append_metric_data("Selected difficulty", Context.difficulty)
    MetricData.append_metric_data("Grid size", f"{width}x{height}")
    MetricData.append_metric_data("Total mines", num_mines)



def run_game():
    init_mine_sweeper()
    forced_position_handler([Context.grid_height // 2, Context.grid_width // 2])
    total_mine_count = len(Context.mine_tiles)
    def user_input_game_handler():
        result = user_input_on_press()
        if result == "enter":
            if GridInterface.click():
                from mines_game.menu import win
                win(case=False, mines_count=total_mine_count)
        elif result == "space":
            GridInterface.flag()
        elif result == "esc":
            from mines_game.menu import main_menu
            main_menu()

    total_time()
    while True:
        MetricData.append_metric_data("Mines left", f"{len(Context.mine_tiles)}")
        MetricData.append_metric_data("Empty tiles left", f"{len(Context.empty_tiles)}")
        render_mine_grid()
        final_render(sprite="grid cursor")
        # print(Context.raw_grid)
        # print(len(Context.mine_tiles))
        # print(f"mines {Context.mine_tiles}")
        # print(f"tiles {Context.empty_tiles}")
        user_input_game_handler()
        position_handler()
        if len(Context.mine_tiles) == 0 or len(Context.empty_tiles) == 0:
            from mines_game.menu import win
            return win(case=True,mines_count=total_mine_count)
