import base64
from unittest.mock import Mock, patch

import pytest
from src.gitlab.gitlab_api import read_repo_file


@pytest.fixture
def mock_content_success():
    """Fixture to create a mock response that simulates a server error (500)."""
    mock_response = Mock()
    file_content = "Hello, GitLab!"
    encoded_content = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")
    mock_response.json.return_value = {"content": encoded_content}

    return mock_response


@pytest.fixture
def mock_content_insuccess():
    """Fixture to create a mock response that simulates a server error (500)."""
    mock_response = Mock()
    file_content = "Hello, GitLab!"
    encoded_content = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")
    mock_response.json.return_value = {"contents": encoded_content}

    return mock_response


@pytest.fixture
def mock_requests_get():
    """Fixture to patch requests.get globally in all tests."""
    with patch("requests.get") as mock_get:
        yield mock_get


def test_read_repo_file_success(mock_requests_get, mock_content_success):
    """Test the read_repo_file function."""
    mock_requests_get.return_value = mock_content_success

    content = read_repo_file(
        organization="example.com",
        repo_url="org/repo",
        gitlab_token="token",
        file_path="file.py",
        main_branch="main",
    )
    assert content == "Hello, GitLab!"


def test_read_repo_file_insuccess(mock_requests_get, mock_content_insuccess):
    """Test the read_repo_file function."""
    mock_requests_get.return_value = mock_content_insuccess

    content = read_repo_file(
        organization="example.com",
        repo_url="org/repo",
        gitlab_token="token",
        file_path="file.py",
        main_branch="main",

    )
    assert content is None
