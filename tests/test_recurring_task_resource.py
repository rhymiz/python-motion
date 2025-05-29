from unittest.mock import Mock

import pytest

from motion.client import HttpMethod
from motion.resources.task import RecurringTaskResource


@pytest.fixture
def recurring_task_resource(mock_client: Mock) -> RecurringTaskResource:
    return RecurringTaskResource(mock_client)


def test_create_recurring_task(
    recurring_task_resource: RecurringTaskResource, mock_client: Mock
) -> None:
    mock_client.call_api.return_value.json.return_value = {
        "id": "rt123",
        "name": "Daily Standup",
        "priority": "HIGH",
        "workspace": {
            "id": "ws123",
            "name": "Test Workspace",
            "type": "PERSONAL",
            "statuses": [],
            "labels": [],
        },
        "creator": {"id": "user123", "name": "John Doe"},
        "assignee": {"id": "user123", "name": "John Doe"},
        "status": {
            "name": "To Do",
            "isDefaultStatus": True,
            "isResolvedStatus": False,
        },
        "labels": [],
    }

    recurring_task = recurring_task_resource.create(
        {
            "frequency": "daily_every_week_day",
            "deadlineType": "SOFT",
            "duration": 30,
            "startingOn": "2024-03-12T06:00:00.000Z",
            "idealTime": "09:00",
            "schedule": "Work Hours",
            "name": "Daily Standup",
            "workspaceId": "ws123",
            "description": "Daily team standup meeting",
            "priority": "HIGH",
            "assigneeId": "user123",
        }
    )

    assert recurring_task.id == "rt123"
    assert recurring_task.name == "Daily Standup"
    assert recurring_task.priority == "HIGH"
    mock_client.call_api.assert_called_once()


def test_list_recurring_tasks(
    recurring_task_resource: RecurringTaskResource, mock_client: Mock
) -> None:
    mock_client.call_api.return_value.json.return_value = {
        "tasks": [
            {
                "id": "rt123",
                "name": "Daily Standup",
                "priority": "HIGH",
                "workspace": {
                    "id": "ws123",
                    "name": "Test Workspace",
                    "type": "PERSONAL",
                    "statuses": [],
                    "labels": [],
                },
                "creator": {"id": "user123", "name": "John Doe"},
                "assignee": {"id": "user123", "name": "John Doe"},
                "status": {
                    "name": "To Do",
                    "isDefaultStatus": True,
                    "isResolvedStatus": False,
                },
                "labels": [],
            },
            {
                "id": "rt124",
                "name": "Weekly Review",
                "priority": "MEDIUM",
                "workspace": {
                    "id": "ws123",
                    "name": "Test Workspace",
                    "type": "PERSONAL",
                    "statuses": [],
                    "labels": [],
                },
                "creator": {"id": "user123", "name": "John Doe"},
                "assignee": {"id": "user123", "name": "John Doe"},
                "status": {
                    "name": "To Do",
                    "isDefaultStatus": True,
                    "isResolvedStatus": False,
                },
                "labels": [],
            },
        ],
        "meta": {"pageSize": 100},
    }

    recurring_tasks = recurring_task_resource.list({"workspaceId": "ws123"})

    assert len(recurring_tasks.tasks) == 2
    assert recurring_tasks.tasks[0].id == "rt123"
    assert recurring_tasks.tasks[1].id == "rt124"
    assert recurring_tasks.meta is not None
    assert recurring_tasks.meta.pageSize == 100
    mock_client.call_api.assert_called_once_with(
        HttpMethod.GET, "/recurring-tasks", params={"workspaceId": "ws123"}
    )


def test_delete_recurring_task(
    recurring_task_resource: RecurringTaskResource, mock_client: Mock
) -> None:
    recurring_task_resource.delete("rt123")

    mock_client.call_api.assert_called_once_with(
        HttpMethod.DELETE, "/recurring-tasks/rt123"
    )
