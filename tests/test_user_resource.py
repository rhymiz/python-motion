import pytest
from motion.resources.user import UserResource
from motion.models import User, ListUsers

@pytest.fixture
def user_resource(mock_client):
    return UserResource(mock_client)

def test_get_self(user_resource, mock_client):
    mock_client.call_api.return_value.json.return_value = {
        "id": "user1",
        "name": "John Doe",
        "email": "john@example.com"
    }
    
    user = user_resource.get_self()
    
    assert isinstance(user, User)
    assert user.id == "user1"
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

def test_list_users(user_resource, mock_client):
    mock_client.call_api.return_value.json.return_value = {
        "users": [
            {
                "id": "user1",
                "name": "John Doe",
                "email": "john@example.com"
            },
            {
                "id": "user2",
                "name": "Jane Doe",
                "email": "jane@example.com"
            }
        ],
        "meta": {"pageSize": 10}
    }
    
    users = user_resource.list({"workspaceId": "ws123"})
    
    assert isinstance(users, ListUsers)
    assert len(users.users) == 2
    assert isinstance(users.users[0], User)
    assert users.users[0].id == "user1"
    assert users.users[1].id == "user2"
    assert users.meta.pageSize == 10