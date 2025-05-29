"""Test the HTTP client"""

from typing import Any
from unittest.mock import Mock, patch

import pytest
import requests

from motion.client import GenericTypedDict, HttpClient, HttpMethod


def test_httpclient_initialization() -> None:
    """Test HttpClient initialization"""
    api_key = "test-api-key"
    client = HttpClient(api_key)
    
    # Just verify it initializes without error
    assert client is not None


@patch("motion.client.requests.request")
def test_call_api_success(mock_request: Mock) -> None:
    """Test successful API call"""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"id": "123", "name": "Test"}
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response
    
    # Make API call
    client = HttpClient("test-api-key")
    response = client.call_api(
        HttpMethod.GET,
        "/tasks",
        params={"workspaceId": "ws123"}
    )
    
    # Verify request was made correctly
    mock_request.assert_called_once_with(
        method="GET",
        url="https://api.usemotion.com/v1/tasks",
        json=None,
        params={"workspaceId": "ws123"},
        headers={"X-API-Key": "test-api-key"}
    )
    
    # Verify response
    assert response == mock_response
    mock_response.raise_for_status.assert_called_once()


@patch("motion.client.requests.request")
def test_call_api_with_data(mock_request: Mock) -> None:
    """Test API call with data payload"""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"id": "123"}
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response
    
    # Make API call
    client = HttpClient("test-api-key")
    data: GenericTypedDict[Any] = {"name": "New Task", "workspaceId": "ws123"}  # type: ignore
    response = client.call_api(
        HttpMethod.POST,
        "/tasks",
        data=data
    )
    
    # Verify request was made correctly
    mock_request.assert_called_once_with(
        method="POST",
        url="https://api.usemotion.com/v1/tasks",
        json=data,
        params=None,
        headers={"X-API-Key": "test-api-key"}
    )
    
    # Verify response
    assert response == mock_response


@patch("motion.client.requests.request")
def test_call_api_strips_leading_slash(mock_request: Mock) -> None:
    """Test that leading slash is stripped from path"""
    # Setup mock response
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_request.return_value = mock_response
    
    # Make API call with leading slash
    client = HttpClient("test-api-key")
    client.call_api(HttpMethod.GET, "/tasks")
    
    # Verify URL doesn't have double slash
    mock_request.assert_called_once()
    call_args = mock_request.call_args
    assert call_args[1]["url"] == "https://api.usemotion.com/v1/tasks"


@patch("motion.client.requests.request")
def test_call_api_error_propagates(mock_request: Mock) -> None:
    """Test that HTTP errors are propagated"""
    # Setup mock response that raises on status check
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    mock_request.return_value = mock_response
    
    # Make API call and expect error
    client = HttpClient("test-api-key")
    with pytest.raises(requests.HTTPError):
        client.call_api(HttpMethod.GET, "/tasks/invalid") 