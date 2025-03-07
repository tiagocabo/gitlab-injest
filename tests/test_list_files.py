import base64
from unittest.mock import Mock, patch
from src.utils import (
    iterate_folder_simple,
    list_subfolder,
    prepare_content,
    prepare_info,
    read_repo_file,
)

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


def test_list_subfolder_404(mock_requests_get, mock_404_response):
    """Test when the API call returns a 404 Not Found."""
    mock_requests_get.return_value = mock_404_response

    results = list_subfolder(
        organization="example.com", repo_url="org/repo", gitlab_token="token"
    )
    assert results == []


def test_list_subfolder_json_error(mock_requests_get, mock_json_error_response):
    """Test when the API call returns invalid JSON."""
    mock_requests_get.return_value = mock_json_error_response

    results = list_subfolder(
        organization="example.com", repo_url="org/repo", gitlab_token="token"
    )
    assert results == []


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


def test_read_repo_file_success(mock_requests_get, mock_content_success):
    """Test the read_repo_file function."""
    mock_requests_get.return_value = mock_content_success

    content = read_repo_file(
        organization="example.com",
        repo_url="org/repo",
        gitlab_token="token",
        file_path="file.py",
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
    )
    assert content == None


def test_prepare_content_python_file():
    """Test when a Python file is processed successfully."""
    with patch("src.utils.read_repo_file", return_value="print('Hello, world!')"):
        result = prepare_content(
            "gitlab.example.com", "script.py", "my-repo", "fake_token"
        )

    expected_header = "=" * 50 + "\nscript.py\n" + "=" * 50
    expected_content = f"\n{expected_header}\nprint('Hello, world!')"
    assert result == expected_content


def test_prepare_content_markdown_file():
    """Test when a Markdown file is processed successfully."""
    with patch("src.utils.read_repo_file", return_value="# This is a README file."):
        result = prepare_content(
            "gitlab.example.com", "README.md", "my-repo", "fake_token"
        )

    expected_header = "=" * 50 + "\nREADME.md\n" + "=" * 50
    expected_content = f"\n{expected_header}\n# This is a README file."
    assert result == expected_content


def test_prepare_content_empty_python_file():
    """Test when a Python file is empty."""
    with patch("src.utils.read_repo_file", return_value=""):
        result = prepare_content(
            "gitlab.example.com", "empty_file.py", "my-repo", "fake_token"
        )

    expected_header = "=" * 50 + "\nempty_file.py\n" + "=" * 50
    expected_content = f"\n{expected_header}\n"
    assert result == expected_content


def test_prepare_content_unsupported_file():
    """Test when a file that is not .py or .md is provided."""
    with patch("src.utils.read_repo_file", return_value="Some content"):
        result = prepare_content(
            "gitlab.example.com", "image.jpg", "my-repo", "fake_token"
        )

    assert result == ""  # The function should return an empty string


def test_prepare_info_single_file():
    """Test when a single file is processed with no subfolders."""
    with (
        patch("src.utils.list_subfolder", return_value=[]),
        patch("src.utils.prepare_content", return_value="File content"),
    ):
        files = ["script.py"]
        result_files, result_content = prepare_info(
            "gitlab.example.com", "my-repo", "fake_token", files, 0
        )

    expected_files = ["|----script.py"]
    expected_content = "File content\n"

    assert result_files == expected_files
    assert result_content == expected_content


def test_prepare_info_multiple_files():
    """Test when multiple files are processed."""
    with (
        patch("src.utils.list_subfolder", side_effect=[[], []]),
        patch("src.utils.prepare_content", side_effect=["Content A", "Content B"]),
    ):
        files = ["script.py", "README.md"]
        result_files, result_content = prepare_info(
            "gitlab.example.com", "my-repo", "fake_token", files, 0
        )

    expected_files = ["|----script.py", "|----README.md"]
    expected_content = "Content A\nContent B\n"

    assert result_files == expected_files
    assert result_content == expected_content


def test_prepare_info_with_subfolder():
    """Test when a subfolder is present with files inside."""
    with (
        patch("src.utils.list_subfolder", side_effect=[["subfolder/file1.py"], []]),
        patch("src.utils.prepare_content", return_value="File content"),
    ):
        files = ["subfolder"]
        result_files, result_content = prepare_info(
            "gitlab.example.com", "my-repo", "fake_token", files, 0
        )

    expected_files = ["|----subfolder/", "|    |----file1.py"]
    expected_content = "File content\n\n"

    assert result_files == expected_files
    assert result_content == expected_content


def test_prepare_info_nested_subfolders():
    """Test when multiple levels of subfolders exist."""
    with (
        patch(
            "src.utils.list_subfolder",
            side_effect=[
                ["subfolder/nested"],
                ["nested/file.py"],
                [],
            ],
        ),
        patch("src.utils.prepare_content", return_value="Nested File Content"),
    ):
        files = ["subfolder"]
        result_files, result_content = prepare_info(
            "gitlab.example.com", "my-repo", "fake_token", files, 0
        )

    expected_files = ["|----subfolder/", "|    |----nested/", "|    |    |----file.py"]
    expected_content = "Nested File Content\n\n\n"

    assert result_files == expected_files
    assert result_content == expected_content


def test_prepare_info_no_files():
    """Test when an empty file list is given."""
    with (
        patch("src.utils.list_subfolder", return_value=[]),
        patch("src.utils.prepare_content", return_value=""),
    ):
        files = []
        result_files, result_content = prepare_info(
            "gitlab.example.com", "my-repo", "fake_token", files, 0
        )

    assert result_files == []
    assert result_content == ""


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
