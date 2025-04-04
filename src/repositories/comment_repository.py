from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.exceptions import (
    ArticleNotFoundException,
    CommentNotFoundException,
    NotCommentAuthorException,
)
from models.article_sql import ArticleModel, CommentModel
from models.user_sql import UserModel


async def get_article_comments(
    session: AsyncSession, article_slug: str
) -> List[CommentModel]:
    """Récupère tous les commentaires d'un article."""
    query = (
        select(CommentModel)
        .join(ArticleModel, CommentModel.article_id == ArticleModel.id)
        .options(joinedload(CommentModel.author))
        .where(ArticleModel.slug == article_slug)
    )
    result = await session.execute(query)
    return list(result.scalars().all())


async def get_comment_by_id(session: AsyncSession, comment_id: int) -> CommentModel:
    """Récupère un commentaire par son ID."""
    query = (
        select(CommentModel)
        .options(joinedload(CommentModel.author))
        .where(CommentModel.id == comment_id)
    )
    result = await session.execute(query)
    comment = result.scalar_one_or_none()

    if comment is None:
        raise CommentNotFoundException()

    return comment


async def create_comment(
    session: AsyncSession,
    article_slug: str,
    body: str,
    author_id: int,
) -> CommentModel:
    """Crée un nouveau commentaire."""
    # Récupérer l'article
    article_query = select(ArticleModel).where(ArticleModel.slug == article_slug)
    article_result = await session.execute(article_query)
    article = article_result.scalar_one_or_none()

    if article is None:
        raise ArticleNotFoundException()

    # Créer le commentaire
    comment = CommentModel(
        body=body,
        article_id=article.id,
        author_id=author_id,
    )

    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return comment


async def delete_comment(session: AsyncSession, comment_id: int, user_id: int) -> None:
    """Supprime un commentaire."""
    # Récupérer le commentaire
    comment = await get_comment_by_id(session, comment_id)

    # Vérifier que l'utilisateur est l'auteur du commentaire
    if comment.author_id != user_id:
        raise NotCommentAuthorException()

    # Supprimer le commentaire
    await session.delete(comment)
    await session.commit()
