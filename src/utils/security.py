from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.user_sql import UserModel as User
from settings import settings


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenContent(BaseModel):
    username: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe en clair correspond au hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Génère un hash pour le mot de passe."""
    return pwd_context.hash(password)


async def get_user_instance(
    db: AsyncSession, username: Optional[str] = None, email: Optional[str] = None
) -> Optional[User]:
    """Get a user instance from its username or email"""
    if username is not None:
        query = select(User).where(User.username == username)
    elif email is not None:
        query = select(User).where(User.email == email)
    else:
        return None

    result = await db.execute(query)
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """Verify the User/Password pair against the DB content"""
    user = await get_user_instance(db, email=email)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict | User, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT token from either a dict or User model."""
    if isinstance(data, User):
        # Create token with username as subject
        to_encode = {"sub": data.username}
    else:
        # Handle dictionary input
        to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # Get the raw secret value from SecretStr
    secret_key = settings.SECRET_KEY.get_secret_value()
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)
    return encoded_jwt
