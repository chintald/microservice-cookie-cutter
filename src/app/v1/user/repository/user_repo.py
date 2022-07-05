from abc import ABCMeta, abstractmethod
from typing import Optional, List

from sqlalchemy import or_, select

from ..models import UserModel
from core.db import session


class UserRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        pass

    @abstractmethod
    async def get_by_email_or_nickname(
        self,
        email: str,
        nickname: str,
    ) -> Optional[UserModel]:
        pass

    @abstractmethod
    async def get_users(self) -> List[UserModel]:
        pass

    @abstractmethod
    async def save(self, user: UserModel) -> UserModel:
        pass

    @abstractmethod
    async def delete(self, user: UserModel) -> None:
        pass


class UserMySQLRepo(UserRepo):
    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return await session.get(UserModel, user_id)

    async def get_by_email_or_nickname(
        self,
        email: str,
        nickname: str,
    ) -> Optional[UserModel]:
        query = await session.execute(
            select(UserModel).where(or_(UserModel.email == email, UserModel.nickname == nickname))
        )

        return query.scalars().first()

    async def get_users(self) -> List[UserModel]:
        query = await session.execute(select(UserModel)).scalars()
        return query.all()

    async def save(self, user: UserModel) -> UserModel:
        session.add(user)
        return user

    async def delete(self, user: UserModel) -> None:
        await session.delete(user)
