from typing import TypedDict, List
from .base import Resource
from ..models import Project, ListProjects


class ProjectCreate(TypedDict):
    name: str
    workspaceId: str
    description: str | None
    labels: List[str] | None
    status: str | None
    priority: str

class ProjectListParams(TypedDict, total=False):
    cursor: str
    workspaceId: str

class ProjectResource(Resource):
    base_path = "/projects"

    def create(self, data: ProjectCreate) -> Project:
        response = super().create(data)
        return Project.model_validate(response.json())

    def list(self, params: ProjectListParams | None = None) -> ListProjects:
        response = super().list(params)
        return ListProjects.model_validate(response.json())

    def retrieve(self, object_id: str) -> Project:
        response = super().retrieve(object_id)
        return Project.model_validate(response.json())
