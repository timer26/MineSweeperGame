from GlobalData.GlobalContext import Context
from dataclasses import dataclass
from typing import Literal
@dataclass
class MetricData:
    metrics_from_system = []

    @classmethod
    def metric_data_init(cls) -> list:

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






@dataclass
class Log:
    log = ["TERMINAL"]
    log_index = 0

    @classmethod
    def add(cls, message: str, level: Literal["INFO", "ERROR", "DEBUG"]):
        cls.log_index += 1
        level = level.upper()
        entry = f"{cls.log_index:03d} [{level}] {message}"
        cls.log.append(entry)

    @classmethod
    def get_log_info(cls) -> list:
        max_log_lines = Context.grid_height - 1
        info_logs = [log[4:] for log in cls.log[1:] if "[INFO]" in log]
        return info_logs[-max_log_lines:]

    @classmethod
    def get_log_debug(cls) -> list:
        max_log_lines = 19
        debug_logs = [log[4:] for log in cls.log[1:] if "[DEBUG]" in log]
        return debug_logs[-max_log_lines:]

    @classmethod
    def get_log_error(cls) -> list:
        max_log_lines = 9
        error_logs = [log[4:] for log in cls.log[1:] if "[ERROR]" in log]
        return error_logs[-max_log_lines:]

    def get_log_all(self):
        return self.log
