import pytest
from motion.resources.project import ProjectResource
from motion.models import Project, ListProjects, Status

@pytest.fixture
def project_resource(mock_client):
    return ProjectResource(mock_client)

def test_create_project(project_resource, mock_client):
    mock_client.call_api.return_value.json.return_value = {
        "id": "proj123",
        "name": "Test Project",
        "description": "A test project",
        "workspaceId": "ws123",
        "status": {"name": "In Progress", "isDefaultStatus": False, "isResolvedStatus": False}
    }
    
    project = project_resource.create({
        "name": "Test Project",
        "workspaceId": "ws123",
        "description": "A test project",
        "priority": "MEDIUM"
    })
    
    assert isinstance(project, Project)
    assert project.id == "proj123"
    assert project.name == "Test Project"
    assert project.workspaceId == "ws123"
    assert isinstance(project.status, Status)

def test_list_projects(project_resource, mock_client):
    mock_client.call_api.return_value.json.return_value = {
        "projects": [
            {
                "id": "proj123",
                "name": "Test Project",
                "status": {"name": "In Progress", "isDefaultStatus": False, "isResolvedStatus": False}
            }
        ],
        "meta": {"pageSize": 10}
    }
    
    projects = project_resource.list({"workspaceId": "ws123"})
    
    assert isinstance(projects, ListProjects)
    assert len(projects.projects) == 1
    assert isinstance(projects.projects[0], Project)
    assert projects.meta.pageSize == 10

def test_retrieve_project(project_resource, mock_client):
    mock_client.call_api.return_value.json.return_value = {
        "id": "proj123",
        "name": "Test Project",
        "status": {"name": "In Progress", "isDefaultStatus": False, "isResolvedStatus": False}
    }
    
    project = project_resource.retrieve("proj123")
    
    assert isinstance(project, Project)
    assert project.id == "proj123"
    assert project.name == "Test Project"