from dataclasses import dataclass, field

@dataclass
class _Context:
    vector= (0,0)
    rendered_area: any = None
    position_modifier: any = None
    position_2D: any = None
    all_menu_functions: any = None

    difficulty: str = "easy"
    difficulty_modifier: float = None
    menu_position: str = "main_menu"
    last_menu_position_stack: list = field(default_factory=lambda: ["main_menu"])
    sprites: dict = field(default_factory=lambda: {
            "menu_cursor": "<--",
            "mine": "@"
    })


Context = _Context()

