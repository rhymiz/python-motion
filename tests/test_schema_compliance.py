"""
Test schema compliance for Motion API models
"""

from typing import Any

from motion.models import (
    AutoScheduledInfo,
    CommentPost,
    ProjectPost,
    RecurringTask,
    Schedule,
    Task,
    TaskPost,
)


def test_task_model_schema_compliance():
    """Test that Task model matches the schema"""
    task_data: dict[str, Any] = {
        "id": "task123",
        "name": "Test Task",
        "description": "A test task",
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
        "parentRecurringTaskId": None,
    }

    task = Task.model_validate(task_data)
    assert task.id == "task123"
    assert task.priority == "HIGH"
    assert task.deadlineType == "SOFT"
    assert task.duration == 30


def test_task_post_schema_compliance() -> None:
    """Test that TaskPost model matches the schema"""
    task_post = TaskPost(
        name="New Task",
        workspaceId="ws123",
        priority="MEDIUM",
        duration="NONE",
        autoScheduled=AutoScheduledInfo(
            deadlineType="HARD", schedule="Work Hours"
        ),
    )

    data = task_post.model_dump(exclude_none=True)
    assert data["name"] == "New Task"
    assert data["priority"] == "MEDIUM"
    assert data["duration"] == "NONE"
    assert data["autoScheduled"]["deadlineType"] == "HARD"


def test_comment_post_schema_compliance():
    """Test that CommentPost model matches the schema"""
    comment_post = CommentPost(
        taskId="task123", content="This is a test comment"
    )

    data = comment_post.model_dump()
    assert data["taskId"] == "task123"
    assert data["content"] == "This is a test comment"


def test_project_post_schema_compliance():
    """Test that ProjectPost model matches the schema"""
    project_post = ProjectPost(
        name="New Project",
        workspaceId="ws123",
        priority="HIGH",
        description="A test project",
    )

    data = project_post.model_dump(exclude_none=True)
    assert data["name"] == "New Project"
    assert data["priority"] == "HIGH"
    assert data["workspaceId"] == "ws123"


def test_schedule_model_schema_compliance():
    """Test that Schedule model matches the schema"""
    schedule_data = {
        "name": "Work Hours",
        "isDefaultTimezone": True,
        "timezone": "America/New_York",
        "schedule": {
            "monday": [{"start": "09:00", "end": "17:00"}],
            "tuesday": [{"start": "09:00", "end": "17:00"}],
            "wednesday": [{"start": "09:00", "end": "17:00"}],
            "thursday": [{"start": "09:00", "end": "17:00"}],
            "friday": [{"start": "09:00", "end": "17:00"}],
            "saturday": [],
            "sunday": [],
        },
    }

    schedule = Schedule.model_validate(schedule_data)
    assert schedule.name == "Work Hours"
    assert schedule.isDefaultTimezone is True
    assert len(schedule.schedule.monday) == 1
    assert schedule.schedule.monday[0].start == "09:00"
    assert len(schedule.schedule.saturday) == 0


def test_recurring_task_schema_compliance():
    """Test that RecurringTask model matches the schema"""
    recurring_task_data: dict[str, Any] = {
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

    recurring_task = RecurringTask.model_validate(recurring_task_data)
    assert recurring_task.id == "rt123"
    assert recurring_task.priority == "HIGH"
    assert recurring_task.name == "Daily Standup"
