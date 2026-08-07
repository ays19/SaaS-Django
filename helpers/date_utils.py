import datetime
from zoneinfo import ZoneInfo

def timestamp_as_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, tz=ZoneInfo("Asia/Dhaka"))