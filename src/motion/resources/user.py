from requests import Response
from .base import Resource
from ..client import HttpMethod


class UserResource(Resource):
    base_path = "/users"

    def get_self(self) -> Response:
        return self._client.call_api(
            HttpMethod.GET,
            path=f"{self.base_path}/me",
        )
