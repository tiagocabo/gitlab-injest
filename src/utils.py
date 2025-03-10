import logging
from typing import List, Tuple

from src.gitlab.gitlab_api import list_subfolder, read_repo_file

logger = logging.getLogger(__name__)


def prepare_content(
    organization: str,
    file: str,
    repo_url: str,
    gitlab_token: str,
    extentions: str,
    main_branch: str,
) -> str:
    """Prepares the content of a specified file if it is a Python (.py) or Markdown (.md) file.

    Args:
        organization (str): The organization name.
        file (str): The file path.
        repo_url (str): The repository URL.
        gitlab_token (str): The GitLab authentication token.
        extentions (str): The file extensions to include.
    Returns:
        str: The formatted file content if applicable, otherwise an empty string.
    """
    if any(file.endswith(ext) for ext in extentions):
        text_header = "=" * 50 + "\n" + file + "\n" + "=" * 50
        content = read_repo_file(
            organization, repo_url, gitlab_token, file, main_branch
        )
        full_content = "\n" + text_header + "\n" + content
    else:
        return ""
    return full_content


def prepare_info(
    organization: str,
    repo_url: str,
    gitlab_token: str,
    files: List[str],
    level: int,
    extentions: List[str],
    main_branch: str,
) -> Tuple[List[str], str]:
    """Recursively retrieves file and folder information, preparing a structured directory list and content.

    Args:
        organization (str): The organization name.
        repo_url (str): The repository URL.
        gitlab_token (str): The GitLab authentication token.
        files (List[str]): List of file paths.
        level (int): The current folder depth level.
        extentions (List[str]): The file extensions to include.

    Returns:
        Tuple[List[str], str]: A tuple containing a list of structured file paths and their corresponding content.
    """
    marker = "|----"
    base = "|    "
    list_files: List[str] = []
    full_content: str = ""

    while files:
        file = files.pop(0)
        sub_files = list_subfolder(
            organization, repo_url, gitlab_token, file, main_branch
        )
        if not sub_files:
            list_files += [level * base + marker + file.split("/")[-1]]
            file_content = prepare_content(
                organization, file, repo_url, gitlab_token, extentions, main_branch
            )
            if file_content:
                full_content += file_content + "\n"
        else:
            list_files.append(level * base + marker + file.split("/")[-1] + "/")
            level += 1
            level_files, level_content = prepare_info(
                organization,
                repo_url,
                gitlab_token,
                sub_files,
                level,
                extentions,
                main_branch,
            )
            level -= 1
            list_files += level_files
            if level_content:
                full_content += level_content + "\n"
    return list_files, full_content


def iterate_folder_simple(
    organization: str,
    repo_url: str,
    gitlab_token: str,
    extentions: List[str],
    main_branch: str,
) -> Tuple[List[str], str, int]:
    """Iterates through the repository folder structure, returning file structure and content.

    Args:
        organization (str): The organization name.
        repo_url (str): The repository URL.
        gitlab_token (str): The GitLab authentication token.

    Returns:
        Tuple[List[str], str, int]: A tuple containing a list of directory structure, concatenated file contents, and the count of directories/files.
    """
    files = list_subfolder(organization, repo_url, gitlab_token, main_branch)
    level = 0
    directory, full_content = prepare_info(
        organization, repo_url, gitlab_token, files, level, extentions, main_branch
    )

    return directory, full_content, len(directory)
