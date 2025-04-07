from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Chemin vers la base de données SQLite
SQLITE_URL = "sqlite+aiosqlite:///./realworld.db"

# Création du moteur asynchrone
engine = create_async_engine(
    SQLITE_URL,
    echo=True,  # Active les logs SQL pour le débogage
    future=True,
)

# Création de la session asynchrone
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Classe de base pour tous les modèles
class Base(DeclarativeBase):
    pass


# Fonction pour obtenir une session de base de données
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
