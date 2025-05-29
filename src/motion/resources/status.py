from typing import Any, List, Required

from ..client import GenericTypedDict
from ..models import Status
from .base import SimpleListResource


class StatusListParams(GenericTypedDict[Any]):
    workspaceId: Required[str]


class StatusResource(SimpleListResource[StatusListParams, Status]):
    base_path = "/statuses"

    def _parse_list(self, data: Any) -> List[Status]:
        return [Status.model_validate(item) for item in data]
