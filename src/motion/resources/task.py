from typing import Any, List, Literal, Union

from ..client import GenericTypedDict, HttpMethod
from ..models import ListRecurringTasks, ListTasks, RecurringTask, Task
from .base import Resource


class TaskCreate(GenericTypedDict[Any], total=False):
    name: str  # required
    workspaceId: str  # required
    dueDate: str
    duration: Union[Literal["NONE", "REMINDER"], int]
    status: str
    autoScheduled: dict[str, Any] | None
    projectId: str
    description: str
    priority: Literal["ASAP", "HIGH", "MEDIUM", "LOW"]
    labels: List[str]
    assigneeId: str


class TaskUpdate(GenericTypedDict[Any], total=False):
    name: str
    dueDate: str
    assigneeId: str | None
    duration: Union[Literal["NONE", "REMINDER"], int]
    status: str
    autoScheduled: dict[str, Any] | None
    projectId: str
    description: str
    priority: Literal["ASAP", "HIGH", "MEDIUM", "LOW"]
    labels: List[str]


class TaskListParams(GenericTypedDict[Any], total=False):
    cursor: str
    label: str
    status: List[str]
    includeAllStatuses: bool
    workspaceId: str
    projectId: str
    name: str
    assigneeId: str


class TaskMoveWorkspace(GenericTypedDict[Any]):
    workspaceId: str
    assigneeId: str  # will be optional in usage


class RecurringTaskCreate(GenericTypedDict[Any]):
    frequency: str
    deadlineType: Literal["HARD", "SOFT"]
    duration: Union[Literal["REMINDER"], int]
    startingOn: str
    idealTime: str
    schedule: str
    name: str
    workspaceId: str
    description: str
    priority: Literal["HIGH", "MEDIUM"]
    assigneeId: str


class RecurringTaskCreateOptional(GenericTypedDict[Any], total=False):
    frequency: str
    deadlineType: Literal["HARD", "SOFT"]
    duration: Union[Literal["REMINDER"], int]
    startingOn: str
    idealTime: str
    schedule: str
    name: str
    workspaceId: str
    description: str
    priority: Literal["HIGH", "MEDIUM"]
    assigneeId: str


class RecurringTaskListParams(GenericTypedDict[Any], total=False):
    cursor: str
    workspaceId: str


class TaskResource(
    Resource[TaskCreate, TaskUpdate, TaskListParams, Task, ListTasks]
):
    base_path = "/tasks"

    def _parse_model(self, data: Any) -> Task:
        return Task.model_validate(data)

    def _parse_list_model(self, data: Any) -> ListTasks:
        return ListTasks.model_validate(data)

    def patch(self, task_id: str, data: TaskUpdate) -> Task:
        response = self._client.call_api(
            HttpMethod.PATCH,
            f"{self.base_path}/{task_id}",
            data=data,
        )
        return Task.model_validate(response.json())

    def unassign_task(self, task_id: str) -> None:
        self._client.call_api(
            HttpMethod.DELETE,
            f"{self.base_path}/{task_id}/assignee",
        )

    def move_workspace(self, task_id: str, data: TaskMoveWorkspace) -> Task:
        response = self._client.call_api(
            HttpMethod.PATCH,
            f"{self.base_path}/{task_id}/move",
            data=data,
        )
        return Task.model_validate(response.json())


class RecurringTaskResource(
    Resource[
        RecurringTaskCreate,
        RecurringTaskCreateOptional,
        RecurringTaskListParams,
        RecurringTask,
        ListRecurringTasks,
    ]
):
    base_path = "/recurring-tasks"

    def _parse_model(self, data: Any) -> RecurringTask:
        return RecurringTask.model_validate(data)

    def _parse_list_model(self, data: Any) -> ListRecurringTasks:
        return ListRecurringTasks.model_validate(data)
