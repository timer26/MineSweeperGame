
from GlobalServices.GlobalData import Context

def position_handler() -> None:
    x, y = Context.current_position
    dx, dy = Context.vector
    x += dx
    y += dy

    modifier = Context.position_modifier
    x = max(modifier["x_min"], min(x, modifier["x_max"]))
    y = max(modifier["y_min"], min(y, modifier["y_max"] - 1))
    Context.current_position = (x, y)



def forced_position_handler(forced_position: list) -> None:
    Context.current_position = forced_position
