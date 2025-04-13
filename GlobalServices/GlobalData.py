from dataclasses import dataclass




@dataclass
class Context:
    vector: tuple[int,int] = (0,0)
    current_position: tuple[int,int] = (0,0)
    difficulty: int or float

    temporary_render = str
     
    #menu data
    menus = any 
    current_menu_position = "main_menu"
    last_position = list
    