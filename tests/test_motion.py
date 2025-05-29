"""Test the main Motion client class"""

from motion import Motion
from motion.resources import (
    CommentResource,
    ProjectResource,
    RecurringTaskResource,
    ScheduleResource,
    StatusResource,
    TaskResource,
    UserResource,
    WorkspaceResource,
)


def test_motion_initialization() -> None:
    """Test that Motion class initializes all resources correctly"""
    api_key = "test-api-key"
    motion = Motion(api_key)
    
    # Check that all resources are initialized with correct types
    assert isinstance(motion.tasks, TaskResource)
    assert isinstance(motion.users, UserResource)
    assert isinstance(motion.projects, ProjectResource)
    assert isinstance(motion.comments, CommentResource)
    assert isinstance(motion.workspaces, WorkspaceResource)
    assert isinstance(motion.schedules, ScheduleResource)
    assert isinstance(motion.statuses, StatusResource)
    assert isinstance(motion.recurring_tasks, RecurringTaskResource) 