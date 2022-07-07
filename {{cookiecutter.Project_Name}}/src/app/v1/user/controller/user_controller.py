from typing import NoReturn, Union

from fastapi import Depends
from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv
from fastapi_utils.guid_type import GUID
from fastapi_utils.inferring_router import InferringRouter

from core.fastapi.schemas.response import ExceptionResponseSchema

from ..schema import CreateUserRequest, CreateUserResponse, User
from ..service.user_command import UserCommandService

router = InferringRouter()


@cbv(router)
class UserController:

    @router.post(
        "/",
        response_model=CreateUserResponse,
        responses={"400": {"model": ExceptionResponseSchema}},
        summary="Create User",
    )
    async def create_user(self, request: CreateUserRequest) -> Union[User, NoReturn]:
        return await UserCommandService().create_user(**request.dict())

    @router.post(
        "/user/{user_id}",
        response_model=CreateUserResponse,
        responses={"400": {"model": ExceptionResponseSchema}},
        summary="Create User",
    )
    def read_item(self, user: str) -> User:
        pass

