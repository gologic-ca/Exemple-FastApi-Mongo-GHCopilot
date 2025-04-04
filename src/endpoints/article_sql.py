from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ArticleNotFoundException, NotArticleAuthorException
from dependencies import get_current_active_user, get_db
from models.article_sql import ArticleModel
from models.user_sql import UserModel
from repositories.article_repository import (
    create_article,
    delete_article,
    favorite_article,
    get_article_by_slug,
    get_articles,
    get_articles_count,
    unfavorite_article,
    update_article,
)
from schemas.article import (
    MultipleArticlesResponse,
    NewArticle,
    SingleArticleResponse,
    UpdateArticle,
)

router = APIRouter()


@router.get("/articles", response_model=MultipleArticlesResponse)
async def get_articles_endpoint(
    author: str | None = None,
    favorited: str | None = None,
    tag: str | None = None,
    limit: int = 20,
    offset: int = 0,
    current_user: Optional[UserModel] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Récupère les articles avec filtres optionnels."""
    articles = await get_articles(
        db, author=author, favorited=favorited, tag=tag, limit=limit, offset=offset
    )
    articles_count = await get_articles_count(
        db, author=author, favorited=favorited, tag=tag
    )

    return MultipleArticlesResponse(
        articles=articles,
        articles_count=articles_count,
    )


@router.get("/articles/feed", response_model=MultipleArticlesResponse)
async def get_feed_articles(
    limit: int = 20,
    offset: int = 0,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Récupère les articles des utilisateurs suivis."""
    articles = await get_articles(
        db, followed_by=current_user.id, limit=limit, offset=offset
    )
    articles_count = await get_articles_count(db, followed_by=current_user.id)

    return MultipleArticlesResponse(
        articles=articles,
        articles_count=articles_count,
    )


@router.get("/articles/{slug}", response_model=SingleArticleResponse)
async def get_article(
    slug: str,
    current_user: Optional[UserModel] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Récupère un article par son slug."""
    article = await get_article_by_slug(db, slug)
    return SingleArticleResponse(article=article)


@router.post("/articles", response_model=SingleArticleResponse)
async def create_article_endpoint(
    article: NewArticle = Body(..., embed=True),
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Crée un nouvel article."""
    new_article = await create_article(
        db,
        title=article.title,
        description=article.description,
        body=article.body,
        tag_list=article.tag_list,
        author_id=current_user.id,
    )
    return SingleArticleResponse(article=new_article)


@router.put("/articles/{slug}", response_model=SingleArticleResponse)
async def update_article_endpoint(
    slug: str,
    article: UpdateArticle = Body(..., embed=True),
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Met à jour un article existant."""
    existing_article = await get_article_by_slug(db, slug)

    # Vérifier que l'utilisateur est l'auteur de l'article
    if existing_article.author_id != current_user.id:
        raise NotArticleAuthorException()

    # Extraire les champs à mettre à jour
    update_data = article.dict(exclude_unset=True)

    updated_article = await update_article(
        db,
        article=existing_article,
        title=update_data.get("title"),
        description=update_data.get("description"),
        body=update_data.get("body"),
        tag_list=update_data.get("tag_list"),
    )

    return SingleArticleResponse(article=updated_article)


@router.delete("/articles/{slug}")
async def delete_article_endpoint(
    slug: str,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Supprime un article."""
    existing_article = await get_article_by_slug(db, slug)

    # Vérifier que l'utilisateur est l'auteur de l'article
    if existing_article.author_id != current_user.id:
        raise NotArticleAuthorException()

    await delete_article(db, existing_article.id)
    return {"status": "ok"}


@router.post("/articles/{slug}/favorite", response_model=SingleArticleResponse)
async def favorite_article_endpoint(
    slug: str,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Ajoute un article aux favoris."""
    article = await get_article_by_slug(db, slug)
    await favorite_article(db, article.id, current_user.id)
    return SingleArticleResponse(article=article)


@router.delete("/articles/{slug}/favorite", response_model=SingleArticleResponse)
async def unfavorite_article_endpoint(
    slug: str,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Retire un article des favoris."""
    article = await get_article_by_slug(db, slug)
    await unfavorite_article(db, article.id, current_user.id)
    return SingleArticleResponse(article=article)
