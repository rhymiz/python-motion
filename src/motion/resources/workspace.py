from typing import Any, List

from ..client import GenericTypedDict
from ..models import ListWorkspaces, Workspace
from .base import Resource


class WorkspaceListParams(GenericTypedDict[Any], total=False):
    cursor: str
    ids: List[str]


class WorkspaceResource(
    Resource[
        GenericTypedDict[Any],
        GenericTypedDict[Any],
        WorkspaceListParams,
        Workspace,
        ListWorkspaces,
    ]
):
    base_path = "/workspaces"

    def _parse_model(self, data: Any) -> Workspace:
        return Workspace.model_validate(data)

    def _parse_list_model(self, data: Any) -> ListWorkspaces:
        return ListWorkspaces.model_validate(data)
