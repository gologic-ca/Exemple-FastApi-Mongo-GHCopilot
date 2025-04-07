import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire racine au chemin Python
sys.path.append(str(Path(__file__).parent.parent))

from passlib.context import CryptContext

from database import async_session
from models.article_sql import ArticleModel, ArticleTag, CommentModel
from models.user_sql import UserModel

# Configuration pour le hachage des mots de passe
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hache un mot de passe."""
    return PWD_CONTEXT.hash(password)


async def init_db():
    """Initialise la base de données avec des données de test."""
    async with async_session() as session:
        # Créer des utilisateurs de test
        users = [
            UserModel(
                username=f"test_user_{i}",
                email=f"test{i}@example.com",
                hashed_password=get_password_hash("test_password"),
                bio=f"Test bio {i}",
                image=f"https://example.com/image{i}.jpg",
            )
            for i in range(3)
        ]

        for user in users:
            session.add(user)

        await session.commit()

        # Créer des tags de test
        tags = ["test", "example", "demo"]
        tag_objects = []
        for tag_name in tags:
            tag = ArticleTag(name=tag_name)
            session.add(tag)
            tag_objects.append(tag)

        await session.commit()

        # Créer des articles de test
        articles = []
        for i, user in enumerate(users):
            article = ArticleModel(
                title=f"Test Article {i}",
                slug=f"test-article-{i}",
                description=f"Test description {i}",
                body=f"Test body {i}",
                author_id=user.id,
                tags=tag_objects,  # Ajouter tous les tags à chaque article
            )
            articles.append(article)
            session.add(article)

        await session.commit()

        # Créer des commentaires de test
        for i, article in enumerate(articles):
            for j, user in enumerate(users):
                comment = CommentModel(
                    body=f"Test comment {i}-{j}",
                    article_id=article.id,
                    author_id=user.id,
                )
                session.add(comment)

        await session.commit()

        print("Base de données initialisée avec succès!")


if __name__ == "__main__":
    asyncio.run(init_db())
