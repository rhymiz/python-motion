from __future__ import annotations  # For forward references in Pydantic v2
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Creator(BaseModel):
    id: str
    name: str
    email: str

class Status(BaseModel):
    name: str
    isDefaultStatus: bool
    isResolvedStatus: bool

class Label(BaseModel):
    name: str

class Assignee(BaseModel):
    email: str
    id: str
    name: str

class Project(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    workspaceId: str
    createdTime: datetime
    updatedTime: datetime

class Workspace(BaseModel):
    id: str
    name: str
    teamId: Optional[str] = None
    statuses: List[Status]
    labels: List[Label]
    type: str

class Meta(BaseModel):
    nextCursor: str
    pageSize: int

class Task(BaseModel):
    deadlineType: str
    id: str
    name: str
    description: Optional[str] = ""
    duration: int
    dueDate: datetime
    parentRecurringTaskId: Optional[str] = None
    creator: Creator
    workspace: Workspace
    project: Optional[Project] = None
    status: Status
    priority: str
    labels: List[Label]
    assignees: List[Assignee]
    scheduledStart: Optional[datetime] = None
    createdTime: datetime
    scheduledEnd: Optional[datetime] = None
    schedulingIssue: bool

class MotionResponse(BaseModel):
    meta: Meta
    tasks: List[Task]

