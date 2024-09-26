from typing import List
from .base import Resource
from ..models import Schedule

class ScheduleResource(Resource):
    base_path = "/schedules"

    def list(self) -> List[Schedule]:
        response = super().list()
        return [Schedule.model_validate(item) for item in response.json()]
