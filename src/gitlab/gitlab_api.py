import base64
import requests
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


def try_request(url: str, headers: str, params: str):
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        try:
            files = response.json()
            return [file["path"] for file in files]
        except ValueError:
            logger.info("Failed to parse JSON response.")
            return []
    elif response.status_code == 404:
        logger.info("Folder not found.")
        return []


def list_branches(organization: str, repo_url: str, gitlab_token: str) -> tuple:
    """
    Lists the branches of a GitLab repository.
    Args:
        organization (str): The GitLab organization name.
        repo_url (str): The URL-encoded path of the repository.
        gitlab_token (str): The private token for GitLab API authentication.
    Returns:
        tuple: A tuple containing the default branch followed by other available branches.
               Returns an empty tuple if the request fails.
    """

    url = f"https://{organization}/api/v4/projects/{repo_url}/repository/branches"

    headers = {"PRIVATE-TOKEN": gitlab_token}

    response = requests.get(url, headers=headers)

    # hedge case no default branch is assigned
    main_branch = ["master", "main"]
    avl_branches = []
    if response.status_code == 200:
        branches = response.json()
        for branch in branches:
            if branch["default"]:
                main_branch = [branch["name"]]
            else:
                avl_branches.append(branch["name"])
        return tuple(main_branch + avl_branches)
    else:
        return ()


def list_subfolder(
    organization: str,
    repo_url: str,
    gitlab_token: str,
    main_branch: str,
    folder: str = ".",
) -> List[str]:
    """Lists the contents of a subfolder in a GitLab repository.

    Args:
        organization (str): The GitLab organization domain.
        repo_url (str): The repository URL slug (project path encoded).
        gitlab_token (str): The personal access token for authentication.
        folder (str, optional): The path of the folder to list. Defaults to ".".

    Returns:
        List[str]: A list of file and folder paths in the specified subfolder.
    """
    url = f"https://{organization}/api/v4/projects/{repo_url}/repository/tree"
    headers = {"PRIVATE-TOKEN": gitlab_token}
    params = {"ref": main_branch, "path": folder}
    result = try_request(url, headers, params)
    if len(result) == 0:
        params = {"ref": "master", "path": folder}
        return try_request(url, headers, params)
    return result


def read_repo_file(
    organization: str,
    repo_url: str,
    gitlab_token: str,
    file_path: str,
    main_branch: str,
) -> Optional[str]:
    """Reads a file from a GitLab repository and returns its content.

    Args:
        organization (str): The GitLab organization domain.
        repo_url (str): The repository URL slug (project path encoded).
        gitlab_token (str): The personal access token for authentication.
        file_path (str): The path of the file to read.

    Returns:
        Optional[str]: The decoded file content, or None if not found.
    """
    file_path = file_path.replace("/", "%2F")
    url = f"https://{organization}/api/v4/projects/{repo_url}/repository/files/{file_path}"
    params = {"ref": main_branch}
    headers = {"PRIVATE-TOKEN": gitlab_token}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        params = {"ref": "master"}
        response = requests.get(url, headers=headers, params=params)

    file = response.json()
    if "content" in file:
        file_content = base64.b64decode(file["content"]).decode("utf-8")
    else:
        return None
    return file_content
