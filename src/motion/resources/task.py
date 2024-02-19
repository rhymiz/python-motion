from requests import Response

from ..client import HttpMethod
from .base import Resource


class TaskResource(Resource):
    base_path = "/tasks"

    def unassign_task(self, task_id: str) -> Response:
        return self._client.call_api(
            HttpMethod.DELETE,
            path=f"{self.base_path}/{task_id}/assignee",
        )

    def move_workspace(
        self,
        task_id: str,
        workspace_id: str,
        assignee_id: str,
    ) -> Response:
        return self._client.call_api(
            HttpMethod.PATCH,
            path=f"{self.base_path}/{task_id}/move",
            data={
                "assigneeId": assignee_id,
                "workspaceId": workspace_id,
            },
        )


class RecurringTaskResource(Resource):
    base_path = "/recurringTasks"
