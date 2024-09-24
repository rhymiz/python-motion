import pytest
from motion.resources.schedule import ScheduleResource
from motion.models import Schedule

@pytest.fixture
def schedule_resource(mock_client):
    return ScheduleResource(mock_client)

def test_list_schedules(schedule_resource, mock_client):
    mock_client.call_api.return_value.json.return_value = [
        {
            "name": "Work Hours",
            "isDefaultTimezone": True,
            "timezone": "America/New_York",
            "schedule": {
                "monday": [{"start": "09:00", "end": "17:00"}],
                "tuesday": [{"start": "09:00", "end": "17:00"}],
                "wednesday": [{"start": "09:00", "end": "17:00"}],
                "thursday": [{"start": "09:00", "end": "17:00"}],
                "friday": [{"start": "09:00", "end": "17:00"}],
                "saturday": [],
                "sunday": []
            }
        }
    ]
    
    schedules = schedule_resource.list()
    
    assert isinstance(schedules, list)
    assert len(schedules) == 1
    assert isinstance(schedules[0], Schedule)
    assert schedules[0].name == "Work Hours"
    assert schedules[0].isDefaultTimezone == True
    assert schedules[0].timezone == "America/New_York"
    assert len(schedules[0].schedule.monday) == 1
    assert schedules[0].schedule.monday[0].start == "09:00"
    assert schedules[0].schedule.monday[0].end == "17:00"