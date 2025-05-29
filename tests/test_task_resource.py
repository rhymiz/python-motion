from unittest.mock import Mock

import pytest

from motion.client import HttpMethod
from motion.resources.task import TaskResource


@pytest.fixture
def task_resource(mock_client: Mock) -> TaskResource:
    return TaskResource(mock_client)


def test_create_task(task_resource: TaskResource, mock_client: Mock) -> None:
    mock_client.call_api.return_value.json.return_value = {
        "id": "task123",
        "name": "New Task",
        "dueDate": "2024-03-12T10:52:55.724-06:00",
        "deadlineType": "SOFT",
        "completed": False,
        "duration": 30,
        "priority": "MEDIUM",
        "schedulingIssue": False,
        "createdTime": "2024-03-12T10:52:55.724-06:00",
        "workspace": {
            "id": "ws123",
            "name": "Test Workspace",
            "type": "PERSONAL",
            "statuses": [],
            "labels": [],
        },
        "creator": {"id": "user123", "name": "John Doe"},
        "status": {
            "name": "To Do",
            "isDefaultStatus": True,
            "isResolvedStatus": False,
        },
        "labels": [],
        "assignees": [],
    }

    task = task_resource.create({"name": "New Task", "workspaceId": "ws123"})

    assert task.id == "task123"
    assert task.name == "New Task"
    assert task.priority == "MEDIUM"
    mock_client.call_api.assert_called_once_with(
        HttpMethod.POST,
        "/tasks",
        data={"name": "New Task", "workspaceId": "ws123"},
    )


def test_list_tasks(task_resource: TaskResource, mock_client: Mock) -> None:
    mock_client.call_api.return_value.json.return_value = {
        "tasks": [
            {
                "id": "task123",
                "name": "Task 1",
                "dueDate": "2024-03-12T10:52:55.724-06:00",
                "deadlineType": "SOFT",
                "completed": False,
                "duration": 30,
                "priority": "HIGH",
                "schedulingIssue": False,
                "createdTime": "2024-03-12T10:52:55.724-06:00",
                "workspace": {
                    "id": "ws123",
                    "name": "Test Workspace",
                    "type": "PERSONAL",
                    "statuses": [],
                    "labels": [],
                },
                "creator": {"id": "user123", "name": "John Doe"},
                "status": {
                    "name": "To Do",
                    "isDefaultStatus": True,
                    "isResolvedStatus": False,
                },
                "labels": [],
                "assignees": [],
            }
        ],
        "meta": {"pageSize": 100},
    }

    tasks = task_resource.list({"workspaceId": "ws123"})

    assert len(tasks.tasks) == 1
    assert tasks.tasks[0].id == "task123"
    assert tasks.meta is not None
    assert tasks.meta.pageSize == 100


def test_retrieve_task(task_resource: TaskResource, mock_client: Mock) -> None:
    mock_client.call_api.return_value.json.return_value = {
        "id": "task123",
        "name": "Task 1",
        "dueDate": "2024-03-12T10:52:55.724-06:00",
        "deadlineType": "SOFT",
        "completed": False,
        "duration": 30,
        "priority": "HIGH",
        "schedulingIssue": False,
        "createdTime": "2024-03-12T10:52:55.724-06:00",
        "workspace": {
            "id": "ws123",
            "name": "Test Workspace",
            "type": "PERSONAL",
            "statuses": [],
            "labels": [],
        },
        "creator": {"id": "user123", "name": "John Doe"},
        "status": {
            "name": "To Do",
            "isDefaultStatus": True,
            "isResolvedStatus": False,
        },
        "labels": [],
        "assignees": [],
    }

    task = task_resource.retrieve("task123")

    assert task.id == "task123"
    assert task.name == "Task 1"
    mock_client.call_api.assert_called_once_with(
        HttpMethod.GET, "/tasks/task123"
    )


def test_patch_task(task_resource: TaskResource, mock_client: Mock) -> None:
    mock_client.call_api.return_value.json.return_value = {
        "id": "task123",
        "name": "Updated Task",
        "dueDate": "2024-03-12T10:52:55.724-06:00",
        "deadlineType": "SOFT",
        "completed": False,
        "duration": 60,
        "priority": "HIGH",
        "schedulingIssue": False,
        "createdTime": "2024-03-12T10:52:55.724-06:00",
        "workspace": {
            "id": "ws123",
            "name": "Test Workspace",
            "type": "PERSONAL",
            "statuses": [],
            "labels": [],
        },
        "creator": {"id": "user123", "name": "John Doe"},
        "status": {
            "name": "In Progress",
            "isDefaultStatus": False,
            "isResolvedStatus": False,
        },
        "labels": [],
        "assignees": [],
    }

    task = task_resource.patch(
        "task123", {"name": "Updated Task", "duration": 60}
    )

    assert task.id == "task123"
    assert task.name == "Updated Task"
    assert task.duration == 60
    mock_client.call_api.assert_called_once_with(
        HttpMethod.PATCH,
        "/tasks/task123",
        data={"name": "Updated Task", "duration": 60},
    )


def test_delete_task(task_resource: TaskResource, mock_client: Mock) -> None:
    task_resource.delete("task123")

    mock_client.call_api.assert_called_once_with(
        HttpMethod.DELETE, "/tasks/task123"
    )


def test_unassign_task(task_resource: TaskResource, mock_client: Mock) -> None:
    task_resource.unassign_task("task123")

    mock_client.call_api.assert_called_once_with(
        HttpMethod.DELETE, "/tasks/task123/assignee"
    )


def test_move_workspace(
    task_resource: TaskResource, mock_client: Mock
) -> None:
    mock_client.call_api.return_value.json.return_value = {
        "id": "task123",
        "name": "Moved Task",
        "dueDate": "2024-03-12T10:52:55.724-06:00",
        "deadlineType": "SOFT",
        "completed": False,
        "duration": 30,
        "priority": "MEDIUM",
        "schedulingIssue": False,
        "createdTime": "2024-03-12T10:52:55.724-06:00",
        "workspace": {
            "id": "ws456",
            "name": "New Workspace",
            "type": "TEAM",
            "statuses": [],
            "labels": [],
        },
        "creator": {"id": "user123", "name": "John Doe"},
        "status": {
            "name": "To Do",
            "isDefaultStatus": True,
            "isResolvedStatus": False,
        },
        "labels": [],
        "assignees": [],
    }

    task = task_resource.move_workspace(
        "task123", {"workspaceId": "ws456", "assigneeId": "user456"}
    )

    assert task.id == "task123"
    assert task.workspace.id == "ws456"
    mock_client.call_api.assert_called_once_with(
        HttpMethod.PATCH,
        "/tasks/task123/move",
        data={"workspaceId": "ws456", "assigneeId": "user456"},
    )
