from datetime import datetime
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field

from models.article import CommentModel
from models.user import UserModel
from schemas.base import BaseSchema
from schemas.user import Profile, User


class CommentBase(BaseSchema):
    """Schéma de base pour les commentaires."""

    body: str


class CommentCreate(CommentBase):
    """Schéma pour la création d'un commentaire."""

    pass


class CommentUpdate(CommentBase):
    """Schéma pour la mise à jour d'un commentaire."""

    pass


class Comment(CommentBase):
    """Schéma pour un commentaire."""

    id: int
    created_at: datetime
    updated_at: datetime
    author: User

    class Config:
        from_attributes = True


class SingleCommentResponse(BaseSchema):
    comment: Comment


class MultipleCommentsResponse(BaseSchema):
    comments: List[Comment]

    @classmethod
    def from_comments_and_authors(cls, data: List[Tuple[CommentModel, UserModel]]):
        return cls(
            comments=[{**comment.dict(), "author": author} for comment, author in data]
        )


class NewComment(BaseSchema):
    body: str


class ProfileResponse(BaseSchema):
    profile: Profile
