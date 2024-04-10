from typing import List

from core.exceptions import UserNotFoundException
from models.user import UserModel
from odmantic import AIOEngine


async def get_user_by_username(engine: AIOEngine, username: str) -> UserModel:
    user = await engine.find_one(UserModel, UserModel.username == username)
    if user is None:
        raise UserNotFoundException()
    return user


async def get_all_users(engine: AIOEngine) -> List[UserModel]:
    """
    Retrieve all users from the database.

    Args:
        engine (AIOEngine): The database engine.

    Returns:
        List[UserModel]: A list of user models.
    """
    return await engine.find(UserModel)
