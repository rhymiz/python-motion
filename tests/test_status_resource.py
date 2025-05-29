import pytest

from motion.models import Status
from motion.resources.status import StatusResource


@pytest.fixture
def status_resource(mock_client):
    return StatusResource(mock_client)


def test_list_statuses(status_resource, mock_client):
    # Mock the API response
    mock_client.call_api.return_value.json.return_value = [
        {"name": "To Do", "isDefaultStatus": True, "isResolvedStatus": False},
        {"name": "Done", "isDefaultStatus": False, "isResolvedStatus": True},
    ]

    # Call the method
    statuses = status_resource.list({"workspaceId": "workspace123"})

    # Verify the response
    assert len(statuses) == 2
    assert isinstance(statuses[0], Status)
    assert statuses[0].name == "To Do"
    assert statuses[0].isDefaultStatus is True
    assert statuses[0].isResolvedStatus is False
    assert isinstance(statuses[1], Status)
    assert statuses[1].name == "Done"
    assert statuses[1].isDefaultStatus is False
    assert statuses[1].isResolvedStatus is True
