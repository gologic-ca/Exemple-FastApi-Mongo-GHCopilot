"""
FastAPI Odmantic RealWorld Example Application
"""

# Import des modèles ODMantic (à conserver pour la migration progressive)
from models.article import ArticleModel as ODManticArticleModel
from models.user import UserModel as ODManticUserModel

# Import des modèles SQLAlchemy
from models.article_sql import ArticleModel, CommentModel, ArticleTag
from models.user_sql import UserModel

__all__ = [
    "ODManticArticleModel",
    "ODManticUserModel",
    "ArticleModel",
    "CommentModel",
    "ArticleTag",
    "UserModel",
]
