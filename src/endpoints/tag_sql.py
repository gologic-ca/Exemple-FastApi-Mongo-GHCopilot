from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from repositories.article_repository import get_all_tags
from schemas.tag import TagsResponse

router = APIRouter()


@router.get("/tags", response_model=TagsResponse)
async def get_tags(
    db: AsyncSession = Depends(get_db),
):
    """Récupère tous les tags disponibles."""
    tags = await get_all_tags(db)
    return TagsResponse(tags=tags)
