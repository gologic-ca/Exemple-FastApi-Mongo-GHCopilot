from fastapi import APIRouter, Body, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import InvalidCredentialsException
from dependencies import get_current_active_user, get_db
from models.user_sql import UserModel
from repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    update_user,
)
from schemas.user import LoginUser, NewUser, UpdateUser, User, UserResponse
from utils.security import create_access_token

router = APIRouter()

# Configuration pour le hachage des mots de passe
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hache un mot de passe."""
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)


async def authenticate_user(db: AsyncSession, email: str, password: str) -> UserModel:
    """Vérifie les identifiants de l'utilisateur."""
    user = await get_user_by_email(db, email)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


@router.post("/users", response_model=UserResponse)
async def register_user(
    user: NewUser = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
):
    """Enregistre un nouvel utilisateur."""
    # Vérifier si l'utilisateur existe déjà
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Créer le nouvel utilisateur
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )

    # Sauvegarder l'utilisateur
    db_user = await create_user(db, db_user)

    # Générer le token
    token = create_access_token(db_user)

    return UserResponse(user=User(token=token, **user.dict()))


@router.post("/users/login", response_model=UserResponse)
async def login_user(
    user_input: LoginUser = Body(..., embed=True, alias="user"),
    db: AsyncSession = Depends(get_db),
):
    """Connecte un utilisateur existant."""
    try:
        password = user_input.password.get_secret_value()
    except AttributeError:
        # Si get_secret_value() n'est pas disponible, utiliser la valeur directement
        password = user_input.password

    user = await authenticate_user(db, user_input.email, password)
    if user is None:
        raise InvalidCredentialsException()

    # Générer le token
    token = create_access_token(user)

    return UserResponse(
        user=User(
            token=token,
            email=user.email,
            username=user.username,
            bio=user.bio,
            image=user.image,
        )
    )


@router.get("/user", response_model=UserResponse)
async def current_user(
    current_user: UserModel = Depends(get_current_active_user),
):
    """Récupère l'utilisateur actuel."""
    return UserResponse(
        user=User(
            email=current_user.email,
            username=current_user.username,
            bio=current_user.bio,
            image=current_user.image,
            token="",  # Le token n'est pas nécessaire ici
        )
    )


@router.put("/user", response_model=UserResponse)
async def update_current_user(
    user_update: UpdateUser = Body(..., embed=True, alias="user"),
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Met à jour l'utilisateur actuel."""
    # Mettre à jour les champs
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    # Sauvegarder les modifications
    updated_user = await update_user(db, current_user)

    return UserResponse(
        user=User(
            email=updated_user.email,
            username=updated_user.username,
            bio=updated_user.bio,
            image=updated_user.image,
            token="",  # Le token n'est pas nécessaire ici
        )
    )
