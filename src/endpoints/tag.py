from core.tag import get_all_tags
from fastapi import APIRouter
from schemas.date import DateResponse
from schemas.tag import TagsResponse
from settings import Engine
from utils.date import string_to_date

router = APIRouter()


@router.get("/tags", response_model=TagsResponse)
async def get_tags():
    tags = await get_all_tags(Engine)
    return TagsResponse(tags=tags)


# endpoint that use date util to convert a string date to a datetime object
# and return the date in a response model
@router.get("/date/{date}", response_model=DateResponse)
async def get_date(date: str):
    date = string_to_date(date)
    return DateResponse(date=date)
