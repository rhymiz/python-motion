from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str
    name: str
    email: Optional[str] = None


class Label(BaseModel):
    name: str


class Status(BaseModel):
    name: str
    isDefaultStatus: bool
    isResolvedStatus: bool


class Project(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    workspaceId: Optional[str] = None
    status: Optional[Status] = None


class Workspace(BaseModel):
    id: str
    name: str
    teamId: Optional[str] = None
    statuses: Optional[List[Status]] = None
    labels: Optional[List[Label]] = None
    type: str


class MetaResult(BaseModel):
    nextCursor: Optional[str] = Field(
        None,
        description="Returned if there are more entities to return. Pass back with the cursor param set to continue paging.",
    )
    pageSize: int = Field(
        ...,
        description="Maximum number of entities delivered per page",
    )


class Comment(BaseModel):
    id: str
    taskId: str
    content: str
    creator: User
    createdAt: datetime


class ListComments(BaseModel):
    comments: List[Comment]
    meta: Optional[MetaResult] = None


class ListProjects(BaseModel):
    projects: List[Project]
    meta: Optional[MetaResult] = None


class RecurringTask(BaseModel):
    workspace: Workspace
    id: str
    name: str
    description: Optional[str] = None
    creator: User
    assignee: User
    project: Optional[Project] = None
    status: Status
    priority: str
    labels: List[Label]


class ListRecurringTasks(BaseModel):
    tasks: List[RecurringTask]
    meta: Optional[MetaResult] = None


class DailySchedule(BaseModel):
    start: str
    end: str


class ScheduleBreakout(BaseModel):
    monday: List[DailySchedule]
    tuesday: List[DailySchedule]
    wednesday: List[DailySchedule]
    thursday: List[DailySchedule]
    friday: List[DailySchedule]
    saturday: List[DailySchedule]
    sunday: List[DailySchedule]


class Schedule(BaseModel):
    name: str
    isDefaultTimezone: bool
    timezone: str
    schedule: ScheduleBreakout


class Task(BaseModel):
    duration: Union[str, int]
    workspace: Workspace
    id: str
    name: str
    description: Optional[str] = None
    dueDate: datetime
    deadlineType: str
    parentRecurringTaskId: Optional[str] = None
    completed: bool
    creator: User
    project: Optional[Project] = None
    status: Status
    priority: str
    labels: List[Label]
    assignees: List[User]
    scheduledStart: Optional[datetime] = None
    createdTime: datetime
    scheduledEnd: Optional[datetime] = None
    schedulingIssue: bool


class ListTasks(BaseModel):
    tasks: List[Task]
    meta: Optional[MetaResult] = None


class ListUsers(BaseModel):
    users: List[User]
    meta: Optional[MetaResult] = None


class ListWorkspaces(BaseModel):
    workspaces: List[Workspace]
    meta: Optional[MetaResult] = None
