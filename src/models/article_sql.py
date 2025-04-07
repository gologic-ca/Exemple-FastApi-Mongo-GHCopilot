from datetime import datetime
from typing import List
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, relationship

from database import Base
# from models.user_sql import UserModel


def generate_random_str():
    s = str(uuid4())
    return s.split("-")[0]


# Table de liaison pour les tags d'articles
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)

# Table de liaison pour les articles favoris
article_favorites = Table(
    "article_favorites",
    Base.metadata,
    Column(
        "article_id",
        Integer,
        ForeignKey("articles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

# Table d'association pour les relations de suivi
user_following = Table(
    "user_following",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class ArticleTag(Base):
    """Modèle pour les tags d'articles."""

    __tablename__ = "tags"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(50), unique=True, index=True)

    # Relations
    articles: Mapped[List["ArticleModel"]] = relationship(
        "ArticleModel",
        secondary=article_tags,
        back_populates="tags",
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


class CommentModel(Base):
    """Modèle pour les commentaires."""

    __tablename__ = "comments"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    body: Mapped[str] = Column(Text)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    article_id: Mapped[int] = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    author_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Relations
    article: Mapped["ArticleModel"] = relationship("ArticleModel", back_populates="comments")
    author: Mapped["UserModel"] = relationship("UserModel", back_populates="comments")

    def __repr__(self):
        return f"<Comment {self.id}>"


class ArticleModel(Base):
    """Modèle pour les articles."""

    __tablename__ = "articles"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = Column(String(255), unique=True, index=True)
    title: Mapped[str] = Column(String(255))
    description: Mapped[str] = Column(String(255))
    body: Mapped[str] = Column(Text)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    author_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Relations
    author: Mapped["UserModel"] = relationship("UserModel", back_populates="articles")
    comments: Mapped[List["CommentModel"]] = relationship(
        "CommentModel", back_populates="article", cascade="all, delete-orphan"
    )
    tags: Mapped[List[ArticleTag]] = relationship(
        ArticleTag,
        secondary=article_tags,
        back_populates="articles",
    )
    favorited_by: Mapped[List["UserModel"]] = relationship(
        "UserModel",
        secondary="article_favorites",
        back_populates="favorite_articles",
    )

    def __repr__(self):
        return f"<Article {self.slug}>"
