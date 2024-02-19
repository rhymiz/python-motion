from requests import Response

from ..client import HttpMethod
from .base import Resource


class WorkspaceResource(Resource):
    base_path = "/workspaces"

    def list_statuses(self, workspace_id: str) -> Response:
        return self._client.call_api(
            HttpMethod.GET,
            path=f"{self.base_path}/statuses",
            params={"workspaceId": workspace_id},
        )
