import asyncio
import os

from sqlalchemy.ext.asyncio import create_async_engine

from database import Base


async def init_db():
    """Initialise la base de données SQLite."""
    # Vérifier si la base de données existe déjà
    db_path = "realworld.db"
    if os.path.exists(db_path):
        print(f"La base de données {db_path} existe déjà.")
        return

    # Créer le moteur asynchrone
    engine = create_async_engine("sqlite+aiosqlite:///./realworld.db", echo=True)

    # Créer les tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print(f"Base de données {db_path} créée avec succès.")


if __name__ == "__main__":
    asyncio.run(init_db())
