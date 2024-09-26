import pytest
from datetime import datetime
from motion.resources.comment import CommentResource
from motion.models import Comment, ListComments, User

@pytest.fixture
def comment_resource(mock_client):
    return CommentResource(mock_client)

def test_create_comment(comment_resource, mock_client):
    mock_client.call_api.return_value.json.return_value = {
        "id": "123",
        "taskId": "task123",
        "content": "Test comment",
        "creator": {"id": "user1", "name": "John Doe"},
        "createdAt": "2023-06-01T12:00:00Z"
    }
    
    comment = comment_resource.create({"taskId": "task123", "content": "Test comment"})
    
    assert isinstance(comment, Comment)
    assert comment.id == "123"
    assert comment.taskId == "task123"
    assert comment.content == "Test comment"
    assert isinstance(comment.creator, User)
    assert isinstance(comment.createdAt, datetime)

def test_list_comments(comment_resource, mock_client):
    mock_client.call_api.return_value.json.return_value = {
        "comments": [
            {
                "id": "123",
                "taskId": "task123",
                "content": "Test comment",
                "creator": {"id": "user1", "name": "John Doe"},
                "createdAt": "2023-06-01T12:00:00Z"
            }
        ],
        "meta": {"pageSize": 10}
    }
    
    comments = comment_resource.list({"taskId": "task123"})
    
    assert isinstance(comments, ListComments)
    assert len(comments.comments) == 1
    assert isinstance(comments.comments[0], Comment)
    assert comments.meta.pageSize == 10