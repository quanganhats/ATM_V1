import datetime
import time


def current_unix_time() -> int:
    current_unix_time = int(time.time())
    return current_unix_time


def unixtime_to_datetime(unix_time: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(unix_time)


def datetime_to_unixtime(date_time: datetime.datetime) -> int:
    return int(date_time.timestamp())

# 2024.7.18 14:47:45:123

def current_day_string_time() -> str:
    now = time.time()
    dt_object = datetime.datetime.fromtimestamp(now)
    year = dt_object.year
    month = dt_object.month
    day = dt_object.day
    hour = dt_object.hour
    minute = dt_object.minute
    second = dt_object.second
    millisecond = int(dt_object.microsecond / 1000)
    return f"{year}.{month}.{day} {hour}:{minute}:{second}:{millisecond}"
