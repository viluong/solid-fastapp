from datetime import datetime

import pytz


def get_current_time() -> datetime:
    return datetime.now(pytz.UTC)


def to_datetime(timestamp: float) -> datetime:
    return datetime.fromtimestamp(timestamp, pytz.UTC)
