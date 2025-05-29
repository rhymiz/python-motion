from typing import Any, List

from ..client import GenericTypedDict
from ..models import Schedule
from .base import SimpleListResource


class ScheduleResource(SimpleListResource[GenericTypedDict[Any], Schedule]):
    base_path = "/schedules"

    def _parse_list(self, data: Any) -> List[Schedule]:
        # The API returns a raw array, not a wrapped object
        return [Schedule.model_validate(item) for item in data]
