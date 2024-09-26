from typing import TypedDict

from ..client import HttpMethod
from ..models import ListUsers, User
from .base import Resource


class UserListParams(TypedDict, total=False):
    cursor: str
    workspaceId: str
    teamId: str


class UserResource(Resource):
    base_path = "/users"

    def get_self(self) -> User:
        response = self._client.call_api(
            HttpMethod.GET,
            path=f"{self.base_path}/me",
        )
        return User.model_validate(response.json())

    def list(self, params: UserListParams | None = None) -> ListUsers:
        response = super().list(params)
        return ListUsers.model_validate(response.json())
