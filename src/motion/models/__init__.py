from datetime import datetime
from typing import List, Literal, Optional, Union

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


# -------------------------------------------------------------
# Response / Domain Models
# -------------------------------------------------------------

# NOTE: The following models aim to mirror the schemas defined in the
#       `Motion REST API swagger.json` file located under the `data/`
#       directory.  Where the OpenAPI specification marks a field as
#       "required" the attribute is defined without a default (or with
#       an explicit `Field(...)`) even when the logical value might be
#       `None`/`null` in responses.  This guarantees that model
#       validation will fail if the API omits a required key, keeping
#       the SDK completely aligned with the contract.


class RecurringTask(BaseModel):
    workspace: Workspace
    id: str
    name: str
    description: Optional[str] = None
    creator: User
    assignee: User
    project: Optional[Project] = None
    status: Status
    # According to the schema the priority field in the response can be
    # one of the task-level priorities (ASAP/HIGH/MEDIUM/LOW).
    priority: Literal["ASAP", "HIGH", "MEDIUM", "LOW"]
    labels: List[Label]


class ListRecurringTasks(BaseModel):
    tasks: List[RecurringTask]
    meta: Optional[MetaResult] = None


class DailySchedule(BaseModel):
    start: str = Field(..., description="24 hour time format. HH:mm")
    end: str = Field(..., description="24 hour time format. HH:mm")


class ScheduleBreakout(BaseModel):
    monday: List[DailySchedule] = Field(
        ...,
        description="Array could be empty if there is no range for this day",
    )
    tuesday: List[DailySchedule] = Field(
        ...,
        description="Array could be empty if there is no range for this day",
    )
    wednesday: List[DailySchedule] = Field(
        ...,
        description="Array could be empty if there is no range for this day",
    )
    thursday: List[DailySchedule] = Field(
        ...,
        description="Array could be empty if there is no range for this day",
    )
    friday: List[DailySchedule] = Field(
        ...,
        description="Array could be empty if there is no range for this day",
    )
    saturday: List[DailySchedule] = Field(
        ...,
        description="Array could be empty if there is no range for this day",
    )
    sunday: List[DailySchedule] = Field(
        ...,
        description="Array could be empty if there is no range for this day",
    )


class Schedule(BaseModel):
    name: str
    isDefaultTimezone: bool
    timezone: str
    schedule: ScheduleBreakout = Field(
        ...,
        description="Schedule broken out by day. It is possible for a day to have more than one start/end time",
    )


class AutoScheduledInfo(BaseModel):
    startDate: Optional[datetime] = Field(
        None,
        description="ISO 8601 Date which is trimmed to the start of the day passed",
    )
    deadlineType: Literal["HARD", "SOFT", "NONE"] = Field(default="SOFT")
    schedule: str = Field(
        default="Work Hours",
        description="Schedule the task must adhere to. Schedule MUST be 'Work Hours' if scheduling the task for another user.",
    )


class Task(BaseModel):
    duration: Union[Literal["NONE", "REMINDER"], int] = Field(
        default=30,
        description='A duration can be one of the following... "NONE", "REMINDER", or a integer greater than 0',
    )
    workspace: Workspace
    id: str
    name: str
    description: Optional[str] = None
    dueDate: datetime
    deadlineType: Literal["HARD", "SOFT", "NONE"] = Field(default="SOFT")
    # The schema marks this field as required but allows it to be
    # `null` when the task is not generated from a recurring template.
    parentRecurringTaskId: Optional[str] = Field(
        ..., description="The id of the recurring task this task belongs to if any"
    )
    completed: bool
    creator: User
    project: Optional[Project] = None
    status: Status
    priority: Literal["ASAP", "HIGH", "MEDIUM", "LOW"]
    labels: List[Label]
    assignees: List[User]
    scheduledStart: Optional[datetime] = Field(
        None,
        description="The time that motion has scheduled this task to start",
    )
    createdTime: datetime = Field(
        ..., description="The time that the task was created"
    )
    scheduledEnd: Optional[datetime] = Field(
        None, description="The time that motion has scheduled this task to end"
    )
    schedulingIssue: bool = Field(
        ...,
        description="Returns true if Motion was unable to schedule this task. Check Motion directly to address",
    )


class ListTasks(BaseModel):
    tasks: List[Task]
    meta: Optional[MetaResult] = None


class ListUsers(BaseModel):
    users: List[User]
    meta: Optional[MetaResult] = None


class ListWorkspaces(BaseModel):
    workspaces: List[Workspace]
    meta: Optional[MetaResult] = None


# Request/Post Models
class CommentPost(BaseModel):
    taskId: str
    content: str


class ProjectPost(BaseModel):
    dueDate: Optional[datetime] = Field(
        None, description="ISO 8601 Due date on the task"
    )
    name: str = Field(..., min_length=1)
    workspaceId: str
    description: Optional[str] = None
    labels: Optional[List[str]] = None
    status: Optional[str] = None
    priority: Literal["ASAP", "HIGH", "MEDIUM", "LOW"] = Field(
        default="MEDIUM"
    )


class RecurringTasksPost(BaseModel):
    frequency: str = Field(
        ...,
        description="Frequency in which the task should be scheduled. Please carefully read how to construct above.",
    )
    deadlineType: Literal["HARD", "SOFT"] = Field(default="SOFT")
    duration: Union[Literal["REMINDER"], int] = Field(
        default=30,
        description='A duration can be one of the following... "REMINDER", or a integer greater than 0',
    )
    startingOn: Optional[datetime] = Field(
        default=None,
        description="ISO 8601 Date which is trimmed to the start of the day passed",
    )
    idealTime: Optional[str] = None
    schedule: str = Field(
        default="Work Hours", description="Schedule the task must adhere to"
    )
    name: str = Field(
        ..., min_length=1, description="Name / title of the task"
    )
    workspaceId: str
    description: Optional[str] = None
    priority: Literal["HIGH", "MEDIUM"] = Field(default="MEDIUM")
    assigneeId: str = Field(
        ..., description="The user id the task should be assigned too"
    )


class TaskPost(BaseModel):
    dueDate: Optional[datetime] = Field(
        None,
        description="ISO 8601 Due date on the task. REQUIRED for scheduled tasks",
    )
    duration: Union[Literal["NONE", "REMINDER"], int] = Field(
        default=30,
        description='A duration can be one of the following... "NONE", "REMINDER", or a integer greater than 0',
    )
    status: Optional[str] = Field(
        None, description="Defaults to workspace default status."
    )
    autoScheduled: Optional[AutoScheduledInfo] = Field(
        None,
        description="Set values to turn auto scheduling on, set value to null if you want to turn auto scheduling off. The status for the task must have auto scheduling enabled.",
    )
    name: str = Field(
        ..., min_length=1, description="Name / title of the task"
    )
    projectId: Optional[str] = None
    workspaceId: str
    description: Optional[str] = Field(
        None, description="Input as GitHub Flavored Markdown"
    )
    priority: Literal["ASAP", "HIGH", "MEDIUM", "LOW"] = Field(
        default="MEDIUM"
    )
    labels: Optional[List[str]] = None
    assigneeId: Optional[str] = Field(
        None, description="The user id the task should be assigned to"
    )


class TaskPatch(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, description="Name / title of the task"
    )
    dueDate: Optional[datetime] = Field(
        None,
        description="ISO 8601 Due date on the task. REQUIRED for scheduled tasks",
    )
    assigneeId: Optional[str] = Field(
        None,
        description="The user id the task should be assigned to, setting the value to null will remove the assignee",
    )
    duration: Optional[Union[Literal["NONE", "REMINDER"], int]] = Field(
        None,
        description='A duration can be one of the following... "NONE", "REMINDER", or a integer greater than 0',
    )
    status: Optional[str] = Field(
        None, description="Defaults to workspace default status."
    )
    autoScheduled: Optional[AutoScheduledInfo] = Field(
        None,
        description="Set values to turn auto scheduling on, set value to null if you want to turn auto scheduling off. The status for the task must have auto scheduling enabled.",
    )
    projectId: Optional[str] = None
    description: Optional[str] = Field(
        None, description="Input as GitHub Flavored Markdown"
    )
    priority: Optional[Literal["ASAP", "HIGH", "MEDIUM", "LOW"]] = None
    labels: Optional[List[str]] = None


class MoveTask(BaseModel):
    workspaceId: str
    assigneeId: Optional[str] = Field(
        None,
        description="The user id the task should be assigned to. Optional according to the OpenAPI specification.",
    )
