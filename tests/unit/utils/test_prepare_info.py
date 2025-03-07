from unittest.mock import patch

from src.utils import prepare_info

def test_prepare_info_single_file():
    """Test when a single file is processed with no subfolders."""
    with (
        patch("src.gitlab.gitlab_api.list_subfolder", return_value=[]),
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
        patch("src.gitlab.gitlab_api.list_subfolder", side_effect=[[], []]),
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
    """Test when a § is present with files inside."""
    with (
        patch(
            "src.gitlab.gitlab_api.list_subfolder",
            side_effect=[["subfolder/file1.py"], []],
        ),
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
            "src.gitlab.gitlab_api.list_subfolder",
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
        patch("src.gitlab.gitlab_api.list_subfolder", return_value=[]),
        patch("src.utils.prepare_content", return_value=""),
    ):
        files = []
        result_files, result_content = prepare_info(
            "gitlab.example.com", "my-repo", "fake_token", files, 0
        )

    assert result_files == []
    assert result_content == ""
