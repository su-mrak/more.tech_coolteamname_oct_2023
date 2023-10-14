import random
from datetime import datetime

import pytz


def random_district_type() -> str:
    district_types = [
        "center",  # внутримкадье
        "suburb",  # замкадье
    ]

    i = random.randint(0, 1)

    # debug
    print(district_types[i])

    return district_types[i]


def current_weekday(timezone_="Europe/Moscow") -> int:
    current_timezone = pytz.timezone(timezone_)
    current_date = datetime.now(current_timezone).date()
    current_weekday = current_date.weekday()

    # debug
    print(current_weekday)

    # returns weekdays from 0 (mon) to 6 (sun)
    return current_weekday


def current_hour(timezone_="Europe/Moscow") -> int:
    current_timezone = pytz.timezone(timezone_)
    current_date = datetime.now(current_timezone).date()
    current_weekday = current_date.weekday()

    # debug
    print(current_weekday)


random_district_type()
current_weekday()
current_time()
