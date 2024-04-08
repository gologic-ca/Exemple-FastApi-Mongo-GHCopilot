# util method related to date. the first metho is used to convert a string to a datetime object

import datetime


def string_to_date(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d")
