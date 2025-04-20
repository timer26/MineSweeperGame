from dataclasses import dataclass, field

@dataclass
class _Context:
    vector= (0,0)
    rendered_area: any = None
    position_modifier: any = None
    position_2D: any = None
    all_menu_functions: any = None
    context_trigger: int = 1
    
    difficulty: str = "easy"
    difficulty_modifier: float = None
    menu_position: str = "main_menu"
    last_menu_position_stack: list = field(default_factory=lambda: ["main_menu"])
    sprites: dict = field(default_factory=lambda: {
            "menu_cursor": "<--",
            "mine": "@"
    })
    
    grid_width = 5
    grid_height = 5
    
    #metric enable/disable
    metric_state = True
    
    #log enable/disable
    log_info_state = True
    log_debug_state = True
    log_error_state = True
    
    
    
    
    
Context = _Context()

