from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.exceptions import ArticleNotFoundException
from models.article_sql import ArticleModel, ArticleTag, CommentModel
from models.user_sql import UserModel


def generate_slug(title: str) -> str:
    """Génère un slug à partir d'un titre."""
    words = title.split()[:5]
    words = [w.lower() for w in words]
    return "-".join(words) + f"-{str(uuid4()).split('-')[0]}"


async def get_article_by_slug(session: AsyncSession, slug: str) -> ArticleModel:
    """Récupère un article par son slug."""
    query = (
        select(ArticleModel)
        .options(
            joinedload(ArticleModel.author),
            joinedload(ArticleModel.comments).joinedload(CommentModel.author),
            joinedload(ArticleModel.tags),
        )
        .where(ArticleModel.slug == slug)
    )
    result = await session.execute(query)
    article = result.scalar_one_or_none()

    if article is None:
        raise ArticleNotFoundException()

    return article


async def get_articles(
    session: AsyncSession,
    author: Optional[str] = None,
    favorited: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> List[ArticleModel]:
    """Récupère les articles avec filtres optionnels."""
    query = select(ArticleModel).options(
        joinedload(ArticleModel.author),
        joinedload(ArticleModel.tags),
    )

    # Appliquer les filtres
    if author:
        query = query.join(UserModel).where(UserModel.username == author)

    if favorited:
        query = query.join(UserModel, ArticleModel.favorited_by).where(
            UserModel.username == favorited
        )

    if tag:
        query = query.join(ArticleTag, ArticleModel.tags).where(ArticleTag.name == tag)

    # Trier par date de création décroissante
    query = query.order_by(desc(ArticleModel.created_at))

    # Pagination
    query = query.limit(limit).offset(offset)

    result = await session.execute(query)
    return list(result.scalars().all())


async def get_articles_count(
    session: AsyncSession,
    author: Optional[str] = None,
    favorited: Optional[str] = None,
    tag: Optional[str] = None,
) -> int:
    """Compte le nombre d'articles avec les mêmes filtres."""
    query = select(func.count()).select_from(ArticleModel)

    # Appliquer les filtres
    if author:
        query = query.join(UserModel).where(UserModel.username == author)

    if favorited:
        query = query.join(UserModel, ArticleModel.favorited_by).where(
            UserModel.username == favorited
        )

    if tag:
        query = query.join(ArticleTag, ArticleModel.tags).where(ArticleTag.name == tag)

    result = await session.execute(query)
    return result.scalar_one()


async def create_article(
    session: AsyncSession,
    title: str,
    description: str,
    body: str,
    author_id: int,
    tag_list: List[str] = None,
) -> ArticleModel:
    """Crée un nouvel article."""
    # Générer le slug
    slug = generate_slug(title)

    # Créer l'article
    article = ArticleModel(
        slug=slug,
        title=title,
        description=description,
        body=body,
        author_id=author_id,
    )

    # Ajouter les tags
    if tag_list:
        for tag_name in tag_list:
            # Vérifier si le tag existe déjà
            tag_query = select(ArticleTag).where(ArticleTag.name == tag_name)
            tag_result = await session.execute(tag_query)
            tag = tag_result.scalar_one_or_none()

            if tag is None:
                # Créer un nouveau tag
                tag = ArticleTag(name=tag_name)
                session.add(tag)

            article.tags.append(tag)

    session.add(article)
    await session.commit()
    await session.refresh(article)

    return article


async def update_article(
    session: AsyncSession,
    article: ArticleModel,
    title: Optional[str] = None,
    description: Optional[str] = None,
    body: Optional[str] = None,
    tag_list: Optional[List[str]] = None,
) -> ArticleModel:
    """Met à jour un article existant."""
    if title is not None:
        article.title = title
        # Mettre à jour le slug si le titre change
        article.slug = generate_slug(title)

    if description is not None:
        article.description = description

    if body is not None:
        article.body = body

    if tag_list is not None:
        # Supprimer tous les tags existants
        article.tags = []

        # Ajouter les nouveaux tags
        for tag_name in tag_list:
            # Vérifier si le tag existe déjà
            tag_query = select(ArticleTag).where(ArticleTag.name == tag_name)
            tag_result = await session.execute(tag_query)
            tag = tag_result.scalar_one_or_none()

            if tag is None:
                # Créer un nouveau tag
                tag = ArticleTag(name=tag_name)
                session.add(tag)

            article.tags.append(tag)

    await session.commit()
    await session.refresh(article)

    return article


async def delete_article(session: AsyncSession, article: ArticleModel) -> None:
    """Supprime un article."""
    await session.delete(article)
    await session.commit()


async def favorite_article(
    session: AsyncSession, article_id: int, user_id: int
) -> ArticleModel:
    """Marque un article comme favori pour un utilisateur."""
    # Récupérer l'article et l'utilisateur
    article_query = select(ArticleModel).where(ArticleModel.id == article_id)
    article_result = await session.execute(article_query)
    article = article_result.scalar_one_or_none()

    user_query = select(UserModel).where(UserModel.id == user_id)
    user_result = await session.execute(user_query)
    user = user_result.scalar_one_or_none()

    if article and user and user not in article.favorited_by:
        article.favorited_by.append(user)
        await session.commit()
        await session.refresh(article)

    return article


async def unfavorite_article(
    session: AsyncSession, article_id: int, user_id: int
) -> ArticleModel:
    """Retire un article des favoris d'un utilisateur."""
    # Récupérer l'article et l'utilisateur
    article_query = select(ArticleModel).where(ArticleModel.id == article_id)
    article_result = await session.execute(article_query)
    article = article_result.scalar_one_or_none()

    user_query = select(UserModel).where(UserModel.id == user_id)
    user_result = await session.execute(user_query)
    user = user_result.scalar_one_or_none()

    if article and user and user in article.favorited_by:
        article.favorited_by.remove(user)
        await session.commit()
        await session.refresh(article)

    return article


async def follow_user(
    session: AsyncSession, user_id: int, user_to_follow_id: int
) -> UserModel:
    """Fait suivre un utilisateur par un autre."""
    # Récupérer les utilisateurs
    user_query = select(UserModel).where(UserModel.id == user_id)
    user_result = await session.execute(user_query)
    user = user_result.scalar_one_or_none()

    user_to_follow_query = select(UserModel).where(UserModel.id == user_to_follow_id)
    user_to_follow_result = await session.execute(user_to_follow_query)
    user_to_follow = user_to_follow_result.scalar_one_or_none()

    if user and user_to_follow and user_to_follow not in user.following:
        user.following.append(user_to_follow)
        await session.commit()
        await session.refresh(user)

    return user


async def unfollow_user(
    session: AsyncSession, user_id: int, user_to_unfollow_id: int
) -> UserModel:
    """Fait ne plus suivre un utilisateur."""
    # Récupérer les utilisateurs
    user_query = select(UserModel).where(UserModel.id == user_id)
    user_result = await session.execute(user_query)
    user = user_result.scalar_one_or_none()

    user_to_unfollow_query = select(UserModel).where(
        UserModel.id == user_to_unfollow_id
    )
    user_to_unfollow_result = await session.execute(user_to_unfollow_query)
    user_to_unfollow = user_to_unfollow_result.scalar_one_or_none()

    if user and user_to_unfollow and user_to_unfollow in user.following:
        user.following.remove(user_to_unfollow)
        await session.commit()
        await session.refresh(user)

    return user


async def get_all_tags(session: AsyncSession) -> List[str]:
    """Récupère tous les tags disponibles."""
    query = select(ArticleTag.name).distinct()
    result = await session.execute(query)
    return [tag[0] for tag in result.all()]
