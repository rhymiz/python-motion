from typing import Any, List, Literal

from ..client import GenericTypedDict
from ..models import ListProjects, Project
from .base import Resource


class ProjectCreate(GenericTypedDict[Any], total=False):
    name: str  # required
    workspaceId: str  # required
    priority: Literal["ASAP", "HIGH", "MEDIUM", "LOW"]  # required
    dueDate: str
    description: str
    labels: List[str]
    status: str


class ProjectListParams(GenericTypedDict[Any], total=False):
    cursor: str
    workspaceId: str  # required for list


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
