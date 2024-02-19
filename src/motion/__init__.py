from .client import HttpClient
from .resources import (
    CommentResource,
    ProjectResource,
    RecurringTaskResource,
    ScheduleResource,
    TaskResource,
    UserResource,
    WorkspaceResource,
)


class Motion:
    """
    Main class for interacting with the Motion API
    """

    def __init__(self, api_key: str) -> None:
        self._client = HttpClient(api_key)
        self.tasks = TaskResource(self._client)
        self.users = UserResource(self._client)
        self.projects = ProjectResource(self._client)
        self.comments = CommentResource(self._client)
        self.workspaces = WorkspaceResource(self._client)
        self.schedules = ScheduleResource(self._client)
        self.recurring_tasks = RecurringTaskResource(self._client)


__all__ = ["Motion"]
