from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotCommentAuthorException
from dependencies import get_current_active_user, get_db
from models.user_sql import UserModel
from repositories.comment_repository import (
    create_comment,
    delete_comment,
    get_article_comments,
    get_comment_by_id,
)
from schemas.comment import MultipleCommentsResponse, NewComment, SingleCommentResponse

router = APIRouter()


@router.get("/articles/{slug}/comments", response_model=MultipleCommentsResponse)
async def get_article_comments_endpoint(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Récupère tous les commentaires d'un article."""
    comments = await get_article_comments(db, slug)
    return MultipleCommentsResponse(comments=comments)


@router.post("/articles/{slug}/comments", response_model=SingleCommentResponse)
async def create_comment_endpoint(
    slug: str,
    comment: NewComment = Body(..., embed=True),
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Crée un nouveau commentaire pour un article."""
    new_comment = await create_comment(
        db,
        article_slug=slug,
        body=comment.body,
        author_id=current_user.id,
    )
    return SingleCommentResponse(comment=new_comment)


@router.delete("/articles/{slug}/comments/{comment_id}")
async def delete_comment_endpoint(
    slug: str,
    comment_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Supprime un commentaire."""
    try:
        await delete_comment(db, comment_id, current_user.id)
        return {"status": "ok"}
    except NotCommentAuthorException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment",
        )
