from typing import List, Optional

from core.user import get_all_users, get_user_by_username
from fastapi import APIRouter, Depends
from models.user import UserModel
from schemas.user import Profile, ProfileResponse
from settings import Engine
from utils.security import get_current_user_instance, get_current_user_optional_instance

router = APIRouter()


@router.get("/profiles/{username}", response_model=ProfileResponse)
async def get_profile(
    username: str,
    logged_user: Optional[UserModel] = Depends(get_current_user_optional_instance),
):
    user = await get_user_by_username(Engine, username)
    following = False
    if logged_user is not None and user.id in logged_user.following_ids:
        following = True
    return ProfileResponse(profile=Profile(following=following, **user.dict()))


@router.get("/profiles", response_model=List[ProfileResponse])
async def get_all_profiles(
    logged_user: Optional[UserModel] = Depends(get_current_user_optional_instance),
):
    """
    Retrieve all user profiles.

    Args:
        logged_user (Optional[UserModel], optional): The logged-in user. Defaults to None.

    Returns:
        List[Profile]: A list of user profiles.
    """
    users = await get_all_users(Engine)
    profiles = []
    for user in users:
        following = False
        if logged_user is not None and user.id in logged_user.following_ids:
            following = True
        profiles.append(Profile(following=following, **user.dict()))
    return profiles


@router.post("/profiles/{username}/follow", response_model=ProfileResponse)
async def follow_user(
    username: str,
    user_instance: UserModel = None,
):
    if user_instance is None:
        user_instance = Depends(get_current_user_instance)
    user_to_follow = await get_user_by_username(Engine, username)
    following_set = set(user_instance.following_ids) | set((user_to_follow.id,))
    user_instance.following_ids = tuple(following_set)
    await Engine.save(user_instance)
    profile = Profile(following=True, **user_to_follow.dict())
    return ProfileResponse(profile=profile)


@router.delete("/profiles/{username}/follow", response_model=ProfileResponse)
async def unfollow_user(
    username: str,
    user_instance: UserModel = Depends(get_current_user_instance),
):
    user_to_unfollow = await get_user_by_username(Engine, username)
    following_set = set(user_instance.following_ids) - set((user_to_unfollow.id,))
    user_instance.following_ids = tuple(following_set)
    await Engine.save(user_instance)
    profile = Profile(following=False, **user_to_unfollow.dict())
    return ProfileResponse(profile=profile)
