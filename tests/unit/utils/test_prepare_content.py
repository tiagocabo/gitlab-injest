from unittest.mock import patch
from src.utils import prepare_content


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
    with patch(
        "src.utils.read_repo_file",
        return_value="# This is a README file.",
    ):
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
