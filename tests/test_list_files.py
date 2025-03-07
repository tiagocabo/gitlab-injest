from unittest.mock import Mock, patch
from src.utils import iterate_folder_simple, list_subfolder

# load dotenv in order to get the token
from dotenv import load_dotenv
import os
import pytest

load_dotenv()

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")


@pytest.fixture
def mock_success_response():
    """Fixture to create a mock response for a successful API call."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"path": "folder1"},
        {"path": "folder2"},
        {"path": "folder3"},
    ]
    return mock_response


@pytest.fixture
def mock_404_response():
    """Fixture to create a mock response for a 404 Not Found."""
    mock_response = Mock()
    mock_response.status_code = 404
    return mock_response


@pytest.fixture
def mock_json_error_response():
    """Fixture to create a mock response that raises a JSON parsing error."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    return mock_response


@pytest.fixture
def mock_server_error_response():
    """Fixture to create a mock response that simulates a server error (500)."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    return mock_response


@pytest.fixture
def mock_requests_get():
    """Fixture to patch requests.get globally in all tests."""
    with patch("requests.get") as mock_get:
        yield mock_get


def test_list_subfolder_success(mock_requests_get, mock_success_response):
    """Test when the API call is successful and returns folder paths"""
    mock_requests_get.return_value = mock_success_response

    results = list_subfolder(
        organization="example.com", repo_url="org/repo", gitlab_token="token"
    )
    assert results == ["folder1", "folder2", "folder3"]


def content_generation():
    directory, content, n_files = iterate_folder_simple(
        organation="",
        repo_url="global-data-science%2Fgenai%2Fmotors-seller-assistant",
        gitlab_token=GITLAB_TOKEN,
    )

    d1 == directory
    c1 == content
    n_files == n_files1
    assert True
