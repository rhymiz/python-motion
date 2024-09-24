from typing import TypedDict, List

from ..client import HttpMethod
from ..models import ListWorkspaces, Status
from .base import Resource


class WorkspaceListParams(TypedDict, total=False):
    cursor: str
    ids: List[str]


class WorkspaceResource(Resource):
    base_path = "/workspaces"

    def list(
        self, params: WorkspaceListParams | None = None
    ) -> ListWorkspaces:
        response = super().list(params)
        return ListWorkspaces.model_validate(response.json())

    def list_statuses(self, workspace_id: str) -> List[Status]:
        response = self._client.call_api(
            HttpMethod.GET,
            path="/statuses",
            params={"workspaceId": workspace_id},
        )
        return [Status.model_validate(item) for item in response.json()]
