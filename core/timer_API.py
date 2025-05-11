from datetime import datetime, timedelta
import requests
from global_data.metric import Log
from global_data.global_context import Context


class CantReachSide(Exception):
    """
    Raised when API request is not satisfied
    """
    pass


def get_time_context() -> datetime:
    try:
        response = requests.get(
            url="https://timeapi.io/api/Time/current/zone?timeZone=UTC", timeout=2
        )
        response.raise_for_status()
        json_data = response.json()

        return datetime(
            year=1,
            month=1,
            day=1,
            hour=json_data["hour"],
            minute=json_data["minute"],
            second=json_data["seconds"]
        )

    except requests.exceptions.RequestException as e:
        Log.add(message=f"Could not reach time API: {e}", level="ERROR")
        return datetime.now()


def total_time()->str|None:
    if not hasattr(Context, "base_time") or Context.base_time is None:
        Log.add(message="base time get initialized", level="DEBUG")
        Context.base_time = get_time_context()

    else:
        Log.add(message="end time get initialized", level="DEBUG")
        end_time = get_time_context()
        delta: timedelta = end_time - Context.base_time
        Context.base_time = None
        return str(delta)