from typing import Any, List, Literal, NotRequired, Required

from ..client import GenericTypedDict
from ..models import ListProjects, Project
from .base import Resource


class ProjectCreate(GenericTypedDict[Any]):
    name: Required[str]
    workspaceId: Required[str]
    priority: Required[Literal["ASAP", "HIGH", "MEDIUM", "LOW"]]

    dueDate: NotRequired[str]
    description: NotRequired[str]
    labels: NotRequired[List[str]]
    status: NotRequired[str]


class ProjectListParams(GenericTypedDict[Any]):
    workspaceId: Required[str]
    cursor: NotRequired[str]


class ProjectResource(
    Resource[
        ProjectCreate, ProjectCreate, ProjectListParams, Project, ListProjects
    ]
):
    base_path = "/projects"

    def _parse_model(self, data: Any) -> Project:
        return Project.model_validate(data)

    def _parse_list_model(self, data: Any) -> ListProjects:
        return ListProjects.model_validate(data)
