from typing import Optional

from pythondi import inject

from ..exception import UserNotFoundException
from ..repository import UserRepo
from ..schema import User


class UserQueryService:
    @inject()
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def get_user(self, user_id: int) -> Optional[User]:
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException

        return User.from_orm(user)

    async def is_admin(self, user_id: int) -> bool:
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True
