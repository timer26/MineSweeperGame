from dataclasses import dataclass

def back():
    from GlobalData.GlobalContext import Context
    if len(Context.last_menu_position_stack) > 1:
        Context.last_menu_position_stack.pop(-1)
        Context.menu_position = Context.last_menu_position_stack[-1]
        Context.all_menu_functions[Context.menu_position]()
    else:
        Context.menu_position = "main_menu"
        Context.all_menu_functions["main_menu"]()
def push_menu_position(current:str):
    from GlobalData.GlobalContext import Context
    if not Context.last_menu_position_stack or Context.last_menu_position_stack[-1] != current:
        Context.last_menu_position_stack.append(current)
def difficulty_setter(difficulty: str):
    from GlobalData.GlobalContext import Context
    if difficulty == "easy":
        Context.difficulty = "easy"
        Context.difficulty_modifier = 1.0
    elif difficulty == "medium":
        Context.difficulty = "medium"
        Context.difficulty_modifier = 1.5
    elif difficulty == "hard":
        Context.difficulty = "hard"
        Context.difficulty_modifier = 2.0

@dataclass
class MetricData:
    metrics_from_system = []

    @classmethod
    def metric_data_init(cls) -> list:
        from GlobalData.GlobalContext import Context
        return [
                {"vector": Context.vector},
                {"position": Context.position_2D},
                {"Selected difficulty": Context.difficulty},
                {"Current menu": Context.menu_position},
                {"Minimum X,Y": (Context.position_modifier["x_min"], Context.position_modifier["y_min"])} if Context.position_modifier else {},
                {"Maximum X,Y": (Context.position_modifier["x_max"], Context.position_modifier["y_max"])} if Context.position_modifier else {},
                {"last_menu_position": Context.last_menu_position_stack},
                {"last_menu_position_stack": Context.last_menu_position_stack[-1]},

        ]

    @classmethod
    def append_metric_data(cls, Text: str = "unnamed_metric", value: any = None) -> None:
        for i, item in enumerate(cls.metrics_from_system):
            if Text in item:
                cls.metrics_from_system[i] = {Text: value}
                return
            
        cls.metrics_from_system.append({Text: value})

    @classmethod
    def metric_data_all(cls) -> list:
        return [entry for entry in cls.metric_data_init() if entry] + cls.metrics_from_system