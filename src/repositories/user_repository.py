from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import UserNotFoundException
from models.user_sql import UserModel


async def get_user_by_username(session: AsyncSession, username: str, raise_exception: bool = True) -> Optional[UserModel]:
    """Récupère un utilisateur par son nom d'utilisateur."""
    query = select(UserModel).where(UserModel.username == username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None and raise_exception:
        raise UserNotFoundException()

    return user


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[UserModel]:
    """Récupère un utilisateur par son email."""
    query = select(UserModel).where(UserModel.email == email)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession) -> List[UserModel]:
    """Récupère tous les utilisateurs."""
    query = select(UserModel)
    result = await session.execute(query)
    return list(result.scalars().all())


async def create_user(session: AsyncSession, user: UserModel) -> UserModel:
    """Crée un nouvel utilisateur."""
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(session: AsyncSession, user: UserModel) -> UserModel:
    """Met à jour un utilisateur existant."""
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user: UserModel) -> None:
    """Supprime un utilisateur."""
    await session.delete(user)
    await session.commit()
