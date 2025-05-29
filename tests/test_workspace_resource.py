from unittest.mock import Mock

import pytest

from motion.client import HttpMethod
from motion.resources.workspace import WorkspaceResource


@pytest.fixture
def workspace_resource(mock_client: Mock) -> WorkspaceResource:
    return WorkspaceResource(mock_client)


def test_list_workspaces(
    workspace_resource: WorkspaceResource, mock_client: Mock
) -> None:
    mock_client.call_api.return_value.json.return_value = {
        "workspaces": [
            {
                "id": "ws123",
                "name": "Personal Workspace",
                "type": "PERSONAL",
                "statuses": [
                    {
                        "name": "To Do",
                        "isDefaultStatus": True,
                        "isResolvedStatus": False,
                    },
                    {
                        "name": "Done",
                        "isDefaultStatus": False,
                        "isResolvedStatus": True,
                    },
                ],
                "labels": [{"name": "Bug"}, {"name": "Feature"}],
            },
            {
                "id": "ws456",
                "name": "Team Workspace",
                "type": "TEAM",
                "teamId": "team123",
                "statuses": [
                    {
                        "name": "Backlog",
                        "isDefaultStatus": True,
                        "isResolvedStatus": False,
                    },
                    {
                        "name": "In Progress",
                        "isDefaultStatus": False,
                        "isResolvedStatus": False,
                    },
                    {
                        "name": "Complete",
                        "isDefaultStatus": False,
                        "isResolvedStatus": True,
                    },
                ],
                "labels": [{"name": "Priority"}, {"name": "Blocked"}],
            },
        ],
        "meta": {"pageSize": 100},
    }

    workspaces = workspace_resource.list()

    assert len(workspaces.workspaces) == 2
    assert workspaces.workspaces[0].id == "ws123"
    assert workspaces.workspaces[0].name == "Personal Workspace"
    assert workspaces.workspaces[1].id == "ws456"
    assert workspaces.workspaces[1].teamId == "team123"
    assert len(workspaces.workspaces[0].statuses) == 2
    assert len(workspaces.workspaces[0].labels) == 2
    assert workspaces.meta is not None
    assert workspaces.meta.pageSize == 100
    mock_client.call_api.assert_called_once_with(
        HttpMethod.GET, "/workspaces", params=None
    )


def test_list_workspaces_with_ids(
    workspace_resource: WorkspaceResource, mock_client: Mock
) -> None:
    mock_client.call_api.return_value.json.return_value = {
        "workspaces": [
            {
                "id": "ws123",
                "name": "Personal Workspace",
                "type": "PERSONAL",
                "statuses": [],
                "labels": [],
            }
        ],
        "meta": {"pageSize": 100, "nextCursor": "cursor123"},
    }

    workspaces = workspace_resource.list({"ids": ["ws123", "ws456"]})

    assert len(workspaces.workspaces) == 1
    assert workspaces.meta is not None
    assert workspaces.meta.nextCursor == "cursor123"
    mock_client.call_api.assert_called_once_with(
        HttpMethod.GET, "/workspaces", params={"ids": ["ws123", "ws456"]}
    )
