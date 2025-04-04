from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship

from database import Base
from models.article_sql import ArticleModel, CommentModel

# Table de liaison pour les utilisateurs suivis
user_follows = Table(
    "user_follows",
    Base.metadata,
    Column(
        "follower_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "followed_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class UserModel(Base):
    """Modèle pour les utilisateurs."""

    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    username: Mapped[str] = Column(String(50), unique=True, index=True)
    email: Mapped[str] = Column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = Column(String(255))
    bio: Mapped[Optional[str]] = Column(String(255), nullable=True)
    image: Mapped[Optional[str]] = Column(String(255), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relations
    articles: Mapped[List["ArticleModel"]] = relationship(
        "ArticleModel", back_populates="author", cascade="all, delete-orphan"
    )
    comments: Mapped[List["CommentModel"]] = relationship(
        "CommentModel", back_populates="author", cascade="all, delete-orphan"
    )
    following: Mapped[List["UserModel"]] = relationship(
        "UserModel",
        secondary=user_follows,
        primaryjoin=(id == user_follows.c.follower_id),
        secondaryjoin=(id == user_follows.c.followed_id),
        backref="followers",
    )
    favorite_articles: Mapped[List["ArticleModel"]] = relationship(
        "ArticleModel",
        secondary="article_favorites",
        back_populates="favorited_by",
    )

    def __repr__(self):
        return f"<User {self.username}>"
