import datetime
from typing import datetime

from sympy import im

from .base import BaseSchema


class DateResponse(BaseSchema):
    date: datetime
