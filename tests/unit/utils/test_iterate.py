from unittest.mock import patch
from src.config import SUPPORTED_EXTENSIONS
from src.utils import iterate_folder_simple


def test_iterate_folder_simple_with_files():
    """Test when the repository contains multiple files and folders."""

    with (
        patch(
            "src.utils.list_subfolder",
            return_value=["file1.py", "subfolder"],
        ),
        patch(
            "src.utils.prepare_info",
            return_value=(["|----file1.py", "|----subfolder/"], "Mocked Content"),
        ),
    ):
        directory, full_content, file_count = iterate_folder_simple(
            "gitlab.example.com", "my-repo", "fake_token", SUPPORTED_EXTENSIONS,"main"
        )

    expected_directory = ["|----file1.py", "|----subfolder/"]
    expected_content = "Mocked Content"
    expected_count = 2

    assert directory == expected_directory
    assert full_content == expected_content
    assert file_count == expected_count


def test_iterate_folder_simple_empty_repo():
    """Test when the repository is empty."""
    with (
        patch("src.utils.list_subfolder", return_value=[]),
        patch("src.utils.prepare_info", return_value=([], "")),
    ):
        directory, full_content, file_count = iterate_folder_simple(
            "gitlab.example.com", "my-repo", "fake_token", SUPPORTED_EXTENSIONS,"main"
        )

    assert directory == []
    assert full_content == ""
    assert file_count == 0


def test_iterate_folder_simple_nested_folders():
    """Test when the repository has nested folders."""
    with (
        patch("src.utils.list_subfolder", return_value=["folder1"]),
        patch(
            "src.utils.prepare_info",
            return_value=(["|----folder1/", "|    |----file.py"], "Nested Content"),
        ),
    ):
        directory, full_content, file_count = iterate_folder_simple(
            "gitlab.example.com", "my-repo", "fake_token", SUPPORTED_EXTENSIONS,"main"
        )

    expected_directory = ["|----folder1/", "|    |----file.py"]
    expected_content = "Nested Content"
    expected_count = 2

    assert directory == expected_directory
    assert full_content == expected_content
    assert file_count == expected_count


def test_iterate_folder_simple_complex_structure():
    """Test when the repository has multiple folders, subfolders, and files."""

    # Mock `list_subfolder` to return top-level folders
    with (
        patch(
            "src.utils.list_subfolder",
            return_value=["folder1", "folder2"],
        ),
        patch(
            "src.utils.prepare_info",
            return_value=(
                [
                    "|----folder1/",
                    "|    |----subfolder1/",
                    "|    |    |----file1.py",
                    "|    |----file2.md",
                    "|----folder2/",
                    "|    |----subfolder2/",
                    "|    |    |----file3.py",
                    "|    |    |----file4.md",
                    "|    |----file5.txt",
                ],
                "Mocked Content from multiple files",
            ),
        ),
    ):
        directory, full_content, file_count = iterate_folder_simple(
            "gitlab.example.com", "my-repo", "fake_token", SUPPORTED_EXTENSIONS,"main"
        )

    expected_directory = [
        "|----folder1/",
        "|    |----subfolder1/",
        "|    |    |----file1.py",
        "|    |----file2.md",
        "|----folder2/",
        "|    |----subfolder2/",
        "|    |    |----file3.py",
        "|    |    |----file4.md",
        "|    |----file5.txt",
    ]

    expected_content = "Mocked Content from multiple files"
    expected_count = len(
        expected_directory
    )  # Should match the number of directory entries

    assert directory == expected_directory
    assert full_content == expected_content
    assert file_count == expected_count
