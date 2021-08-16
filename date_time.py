import datetime
import pytz


def get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


