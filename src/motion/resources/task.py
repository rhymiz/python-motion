from typing import Any, List, Literal, NotRequired, Required, Union

from ..client import GenericTypedDict, HttpMethod
from ..models import ListRecurringTasks, ListTasks, RecurringTask, Task
from .base import Resource


class TaskCreate(GenericTypedDict[Any]):
    name: Required[str]
    workspaceId: Required[str]

    dueDate: NotRequired[str]
    duration: NotRequired[Union[Literal["NONE", "REMINDER"], int]]
    status: NotRequired[str]
    autoScheduled: NotRequired[dict[str, Any] | None]
    projectId: NotRequired[str]
    description: NotRequired[str]
    priority: NotRequired[Literal["ASAP", "HIGH", "MEDIUM", "LOW"]]
    labels: NotRequired[List[str]]
    assigneeId: NotRequired[str]


class TaskUpdate(GenericTypedDict[Any], total=False):
    name: NotRequired[str]
    dueDate: NotRequired[str]
    assigneeId: NotRequired[str | None]
    duration: NotRequired[Union[Literal["NONE", "REMINDER"], int]]
    status: NotRequired[str]
    autoScheduled: NotRequired[dict[str, Any] | None]
    projectId: NotRequired[str]
    description: NotRequired[str]
    priority: NotRequired[Literal["ASAP", "HIGH", "MEDIUM", "LOW"]]
    labels: NotRequired[List[str]]


class TaskListParams(GenericTypedDict[Any], total=False):
    cursor: NotRequired[str]
    label: NotRequired[str]
    status: NotRequired[List[str]]
    includeAllStatuses: NotRequired[bool]
    workspaceId: NotRequired[str]
    projectId: NotRequired[str]
    name: NotRequired[str]
    assigneeId: NotRequired[str]


class TaskMoveWorkspace(GenericTypedDict[Any]):
    workspaceId: Required[str]
    assigneeId: NotRequired[str]


class RecurringTaskCreate(GenericTypedDict[Any]):
    frequency: Required[str]
    name: Required[str]
    workspaceId: Required[str]
    priority: Required[Literal["HIGH", "MEDIUM"]]
    assigneeId: Required[str]

    deadlineType: NotRequired[Literal["HARD", "SOFT"]]
    duration: NotRequired[Union[Literal["REMINDER"], int]]
    startingOn: NotRequired[str]
    idealTime: NotRequired[str]
    schedule: NotRequired[str]
    description: NotRequired[str]


class RecurringTaskCreateOptional(GenericTypedDict[Any], total=False):
    # This TypedDict mirrors RecurringTaskCreate but every key is
    # explicitly marked as NotRequired so that `PATCH` calls only need
    # to include fields that should be modified.

    frequency: NotRequired[str]
    deadlineType: NotRequired[Literal["HARD", "SOFT"]]
    duration: NotRequired[Union[Literal["REMINDER"], int]]
    startingOn: NotRequired[str]
    idealTime: NotRequired[str]
    schedule: NotRequired[str]
    name: NotRequired[str]
    workspaceId: NotRequired[str]
    description: NotRequired[str]
    priority: NotRequired[Literal["HIGH", "MEDIUM"]]
    assigneeId: NotRequired[str]


class RecurringTaskListParams(GenericTypedDict[Any]):
    workspaceId: Required[str]
    cursor: NotRequired[str]


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
