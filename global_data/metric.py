from datetime import datetime, timezone
import os
import json
import inspect
from global_data.global_context import Context
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









class Log:
    log = ["TERMINAL"]
    log_index = 0

    # Standard session ID (ISO 8601 UTC with milliseconds)
    session_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%f")[:-3] + "Z"
    # Use absolute path to log_storage
    base_dir = os.path.abspath(os.path.dirname(__file__))
    log_dir = os.path.join(base_dir, "..", "..", "log_storage")
    os.makedirs(log_dir, exist_ok=True)  # ✅ Create directory immediately
    info_file = "log_info.json"
    debug_file = "log_debug.json"
    error_file = "log_error.json"

    @classmethod
    def _init_log_files(cls):
        os.makedirs(cls.log_dir, exist_ok=True) 
    
        session_header = f"============== session ID: {cls.session_id} =============="
        base_data = {"header": session_header, "logs": []}
    
        # Always clear info and debug logs each session
        for file in [cls.info_file, cls.debug_file]:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(base_data, f, indent=2)
            cls.add(f"Initialized and cleared log file: {file}", "DEBUG")
    
        # Ensure error log exists and append session header
        if not os.path.exists(cls.error_file):
            with open(cls.error_file, "w", encoding="utf-8") as f:
                json.dump({"logs": [{"header": session_header}]}, f, indent=2)
            cls.add("Created new error log file and added session header", "DEBUG")
        else:
            try:
                with open(cls.error_file, "r+", encoding="utf-8") as f:
                    data = json.load(f)
                    if "logs" not in data or not isinstance(data["logs"], list):
                        data["logs"] = []
    
                    data["logs"].append({"header": session_header})
    
                    f.seek(0)
                    json.dump(data, f, indent=2)
                    f.truncate()
    
                cls.add("Appended session header to existing error log", "DEBUG")
            except Exception as e:
                fallback = f"000 [ERROR] {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} - Failed to update log_error.json: {e}"
                cls.log.append(fallback)

    @classmethod
    def _get_caller_context(cls) -> str:
        frame = inspect.stack()[2]
        filename = os.path.basename(frame.filename)
        line = frame.lineno
        function = frame.function
        return f"{filename}:{function}():{line}"

    @classmethod
    def _to_json_entry(cls, index: int, level: str, timestamp: str, message: str, location: str) -> dict:
        return {
                "session_id": cls.session_id,
                "id": index,
                "timestamp": timestamp,
                "level": level,
                "message": message,
                "location": location
        }
    @classmethod
    def _to_string_entry(cls, index: int, level: str, timestamp: str, message: str) -> str:
        return f"{index:03d} [{level}] {timestamp} - {message}"

    @classmethod
    def _append_to_file(cls, entry: dict, file_path: str):
        try:
            with open(file_path, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.setdefault("logs", []).append(entry)
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        except Exception as e:
            fallback = cls._to_string_entry(
                    0, "ERROR",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    f"Log write failed: {e}"
            )
            cls.log.append(fallback)

    @classmethod
    def add(cls, message: str, level: Literal["INFO", "ERROR", "DEBUG"]):
        cls.log_index += 1
        level = level.upper()
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        location = cls._get_caller_context()
    
        # Use clean message for display and add location as separate JSON key
        string_entry = cls._to_string_entry(cls.log_index, level, timestamp, f"{message}  [from {location}]")
        json_entry = cls._to_json_entry(cls.log_index, level, timestamp, message, location)
    
        cls.log.append(string_entry)
    
        if level == "ERROR":
            cls._append_to_file(json_entry, cls.error_file)
        elif level == "DEBUG":
            cls._append_to_file(json_entry, cls.debug_file)
        else:
            cls._append_to_file(json_entry, cls.info_file)

    @classmethod
    def _read_json_logs(cls, file_path: str) -> list[dict]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [
                        entry for entry in data.get("logs", [])
                        if isinstance(entry, dict) and entry.get("session_id") == cls.session_id
                ]
        except Exception as e:
            cls.log.append(f"000 [ERROR] Failed to read {file_path}: {e}")
            return []
    
    @classmethod
    def get_log_info(cls) -> list[str]:
        logs = cls._read_json_logs(cls.info_file)
        return [f'{entry["id"]:03d} [{entry["level"]}] {entry["message"]}' for entry in logs]
    
    @classmethod
    def get_log_debug(cls) -> list[str]:
        logs = cls._read_json_logs(cls.debug_file)
        return [f'{entry["id"]:03d} [{entry["level"]}] {entry["message"]}' for entry in logs[-19:]]
    
    @classmethod
    def get_log_error(cls) -> list[str]:
        logs = cls._read_json_logs(cls.error_file)
        return [
                       f'{entry["id"]:03d} [{entry["level"]}] {entry["message"]}'
                       for entry in logs
                       if isinstance(entry, dict) and "level" in entry and entry["level"] == "ERROR"
               ][-9:]


# === Initialize log files when class is defined ===
Log._init_log_files()