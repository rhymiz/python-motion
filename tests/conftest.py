import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_client():
    return Mock()