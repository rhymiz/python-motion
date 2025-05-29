from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_client() -> Mock:
    """Fixture providing a mocked HttpClient for testing"""
    return Mock()
