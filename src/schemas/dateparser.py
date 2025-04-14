from datetime import datetime
from .base import BaseSchema

class DateParseRequest(BaseSchema):
    date_string: str

class DateParseResponse(BaseSchema):
    parsed_date: datetime