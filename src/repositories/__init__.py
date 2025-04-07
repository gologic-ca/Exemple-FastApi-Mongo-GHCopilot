"""
Repositories pour l'accès aux données avec SQLAlchemy
"""

from repositories.article_repository import (
    create_article,
    delete_article,
    favorite_article,
    follow_user,
    get_article_by_slug,
    get_articles,
    get_articles_count,
    unfavorite_article,
    unfollow_user,
    update_article,
)
from repositories.comment_repository import (
    create_comment,
    delete_comment,
    get_article_comments,
    get_comment_by_id,
)
from repositories.user_repository import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_email,
    get_user_by_username,
    update_user,
)

__all__ = [
    # User repository
    "get_user_by_username",
    "get_user_by_email",
    "get_all_users",
    "create_user",
    "update_user",
    "delete_user",
    # Article repository
    "get_article_by_slug",
    "get_articles",
    "get_articles_count",
    "create_article",
    "update_article",
    "delete_article",
    "favorite_article",
    "unfavorite_article",
    "follow_user",
    "unfollow_user",
    # Comment repository
    "get_article_comments",
    "get_comment_by_id",
    "create_comment",
    "delete_comment",
]
