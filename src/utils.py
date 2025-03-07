import logging
from typing import List, Tuple

from src.gitlab.gitlab_api import list_subfolder, read_repo_file

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = [
    ".py",
    ".md",
    ".yaml",
    ".yml",
    ".ipynb",
    ".dockerignore",
    ".dockerfile",
    ".txt",
    ".sh",
    ".json",
    "Makefile",
    "Pipfile",
    "requirements.txt",
    "setup.py",
    "Dockerfile",
    "docker-compose.yml",
    ".tf",
    ".tfvars",
    ".hcl",
    ".toml",
    ".ini",
    ".conf",
    ".terraform-version",
]


def prepare_content(
    organization: str, file: str, repo_url: str, gitlab_token: str
) -> str:
    """Prepares the content of a specified file if it is a Python (.py) or Markdown (.md) file.

    Args:
        organization (str): The organization name.
        file (str): The file path.
        repo_url (str): The repository URL.
        gitlab_token (str): The GitLab authentication token.

    Returns:
        str: The formatted file content if applicable, otherwise an empty string.
    """
    if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
        text_header = "=" * 50 + "\n" + file + "\n" + "=" * 50
        content = read_repo_file(organization, repo_url, gitlab_token, file)
        full_content = "\n" + text_header + "\n" + content
    else:
        return ""
    return full_content


def prepare_info(
    organization: str, repo_url: str, gitlab_token: str, files: List[str], level: int
) -> Tuple[List[str], str]:
    """Recursively retrieves file and folder information, preparing a structured directory list and content.

    Args:
        organization (str): The organization name.
        repo_url (str): The repository URL.
        gitlab_token (str): The GitLab authentication token.
        files (List[str]): List of file paths.
        level (int): The current folder depth level.

    Returns:
        Tuple[List[str], str]: A tuple containing a list of structured file paths and their corresponding content.
    """
    marker = "|----"
    base = "|    "
    list_files: List[str] = []
    full_content: str = ""

    while files:
        file = files.pop(0)
        sub_files = list_subfolder(organization, repo_url, gitlab_token, file)
        if not sub_files:
            list_files += [level * base + marker + file.split("/")[-1]]
            file_content = prepare_content(organization, file, repo_url, gitlab_token)
            if file_content:
                full_content += file_content + "\n"
        else:
            list_files.append(level * base + marker + file.split("/")[-1] + "/")
            level += 1
            level_files, level_content = prepare_info(
                organization, repo_url, gitlab_token, sub_files, level
            )
            level -= 1
            list_files += level_files
            if level_content:
                full_content += level_content + "\n"
    return list_files, full_content


def iterate_folder_simple(
    organization: str, repo_url: str, gitlab_token: str
) -> Tuple[List[str], str, int]:
    """Iterates through the repository folder structure, returning file structure and content.

    Args:
        organization (str): The organization name.
        repo_url (str): The repository URL.
        gitlab_token (str): The GitLab authentication token.

    Returns:
        Tuple[List[str], str, int]: A tuple containing a list of directory structure, concatenated file contents, and the count of directories/files.
    """
    files = list_subfolder(organization, repo_url, gitlab_token)
    level = 0
    directory, full_content = prepare_info(
        organization, repo_url, gitlab_token, files, level
    )

    return directory, full_content, len(directory)
