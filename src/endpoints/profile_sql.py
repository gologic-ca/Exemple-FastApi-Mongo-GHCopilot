from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_current_active_user, get_db
from models.user_sql import UserModel
from repositories.article_repository import follow_user, unfollow_user
from repositories.user_repository import get_user_by_username
from schemas.user import Profile, ProfileResponse

router = APIRouter()


@router.get("/profiles/{username}", response_model=ProfileResponse)
async def get_profile(
    username: str,
    current_user: Optional[UserModel] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Récupère le profil d'un utilisateur."""
    user = await get_user_by_username(db, username)
    following = False

    if current_user is not None:
        # Vérifier si l'utilisateur actuel suit cet utilisateur
        following = user.id in [f.id for f in current_user.following]

    return ProfileResponse(profile=Profile(following=following, **user.dict()))


@router.post("/profiles/{username}/follow", response_model=ProfileResponse)
async def follow_user_endpoint(
    username: str,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Suit un utilisateur."""
    user_to_follow = await get_user_by_username(db, username)

    if user_to_follow.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot follow yourself",
        )

    await follow_user(db, current_user.id, user_to_follow.id)

    return ProfileResponse(profile=Profile(following=True, **user_to_follow.dict()))


@router.delete("/profiles/{username}/follow", response_model=ProfileResponse)
async def unfollow_user_endpoint(
    username: str,
    current_user: UserModel = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Ne suit plus un utilisateur."""
    user_to_unfollow = await get_user_by_username(db, username)
    await unfollow_user(db, current_user.id, user_to_unfollow.id)

    return ProfileResponse(profile=Profile(following=False, **user_to_unfollow.dict()))
