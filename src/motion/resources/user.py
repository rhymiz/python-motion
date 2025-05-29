from typing import Any

from ..client import GenericTypedDict, HttpMethod
from ..models import ListUsers, User
from .base import Resource


class UserListParams(GenericTypedDict[Any], total=False):
    cursor: str
    workspaceId: str
    teamId: str


class UserResource(
    Resource[
        GenericTypedDict[Any],
        GenericTypedDict[Any],
        UserListParams,
        User,
        ListUsers,
    ]
):
    base_path = "/users"

    def _parse_model(self, data: Any) -> User:
        return User.model_validate(data)

    def _parse_list_model(self, data: Any) -> ListUsers:
        return ListUsers.model_validate(data)

    def get_self(self) -> User:
        response = self._client.call_api(
            HttpMethod.GET,
            f"{self.base_path}/me",
        )
        return User.model_validate(response.json())
