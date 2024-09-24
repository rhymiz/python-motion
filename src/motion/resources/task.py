from typing import Any, List, TypedDict

from ..client import HttpMethod
from ..models import ListRecurringTasks, ListTasks, RecurringTask, Task
from .base import Resource


class TaskCreate(TypedDict, total=False):
    name: str
    workspaceId: str
    dueDate: str
    duration: int | str
    status: str
    autoScheduled: dict[str, Any] | None
    projectId: str | None
    description: str | None
    priority: str
    labels: List[str] | None
    assigneeId: str | None


class TaskUpdate(TypedDict, total=False):
    name: str
    dueDate: str
    assigneeId: str | None
    duration: int | str
    status: str
    autoScheduled: dict[str, Any] | None
    projectId: str
    description: str
    priority: str
    labels: List[str]


class TaskListParams(TypedDict, total=False):
    cursor: str
    label: str
    status: List[str]
    includeAllStatuses: bool
    workspaceId: str
    projectId: str
    name: str
    assigneeId: str


class TaskMoveWorkspace(TypedDict):
    workspaceId: str
    assigneeId: str | None


class RecurringTaskCreate(TypedDict):
    frequency: str
    deadlineType: str
    duration: int | str
    startingOn: str
    idealTime: str | None
    schedule: str
    name: str
    workspaceId: str
    description: str | None
    priority: str
    assigneeId: str


class RecurringTaskListParams(TypedDict, total=False):
    cursor: str
    workspaceId: str


class TaskResource(Resource):
    base_path = "/tasks"

    def create(self, data: TaskCreate) -> Task:
        response = super().create(data)
        return Task.model_validate(response.json())

    def update(self, object_id: str, data: TaskUpdate) -> Task:
        response = super().update(object_id, data)
        return Task.model_validate(response.json())

    def list(self, params: TaskListParams | None = None) -> ListTasks:
        response = super().list(params)
        return ListTasks.model_validate(response.json())

    def retrieve(self, object_id: str) -> Task:
        response = super().retrieve(object_id)
        return Task.model_validate(response.json())

    def unassign_task(self, task_id: str) -> None:
        self._client.call_api(
            HttpMethod.DELETE,
            path=f"{self.base_path}/{task_id}/assignee",
        )

    def move_workspace(self, task_id: str, data: TaskMoveWorkspace) -> Task:
        response = self._client.call_api(
            HttpMethod.PATCH,
            path=f"{self.base_path}/{task_id}/move",
            data=data,
        )
        return Task.model_validate(response.json())


class RecurringTaskResource(Resource):
    base_path = "/recurring-tasks"

    def create(self, data: RecurringTaskCreate) -> RecurringTask:
        response = super().create(data)
        return RecurringTask.model_validate(response.json())

    def list(
        self, params: RecurringTaskListParams | None = None
    ) -> ListRecurringTasks:
        response = super().list(params)
        return ListRecurringTasks.model_validate(response.json())

    def delete(self, object_id: str) -> None:
        super().delete(object_id)
