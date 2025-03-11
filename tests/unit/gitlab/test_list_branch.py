from unittest.mock import Mock, patch
from src.gitlab.gitlab_api import (
    list_branches,
)  # Replace 'your_module' with the actual module name


@patch("requests.get")
def test_list_branches_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"name": "main", "default": True},
        {"name": "dev", "default": False},
        {"name": "feature-branch", "default": False},
    ]
    mock_get.return_value = mock_response

    result = list_branches("gitlab.com", "encoded-repo-path", "fake-token")
    assert result == ("main", "dev", "feature-branch")


@patch("requests.get")
def test_list_branches_no_default(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"name": "dev", "default": False},
        {"name": "feature-branch", "default": False},
    ]
    mock_get.return_value = mock_response

    result = list_branches("gitlab.com", "encoded-repo-path", "fake-token")
    assert result == ("master", "main", "dev", "feature-branch")


@patch("requests.get")
def test_list_branches_empty_response(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    result = list_branches("gitlab.com", "encoded-repo-path", "fake-token")
    assert result == ("master", "main")


@patch("requests.get")
def test_list_branches_failed_request(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = list_branches("gitlab.com", "encoded-repo-path", "fake-token")
    assert result == ()
