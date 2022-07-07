from typing import NoReturn, Union

from pythondi import inject

from core.db import Propagation, Transactional

from ..exception import (DuplicateEmailOrNicknameException,
                         UserNotFoundException)
from ..models import UserModel
from ..repository import UserRepo
from ..schema import User


class UserCommandService:
    @inject()
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_user(
        self, email: str, password1: str, password2: str, nickname: str
    ) -> Union[User, NoReturn]:
        if await self.user_repo.get_by_email_or_nickname(
            email=email,
            nickname=nickname,
        ):
            raise DuplicateEmailOrNicknameException

        user = UserModel.create(
            password1=password1,
            password2=password2,
            email=email,
            nickname=nickname,
        )
        user = await self.user_repo.save(user=user)
        return User.from_orm(user)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_password(
        self,
        user_id: int,
        password1: str,
        password2: str,
    ) -> Union[User, NoReturn]:
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException

        user.change_password(password1=password1, password2=password2)
        return User.from_orm(user)
