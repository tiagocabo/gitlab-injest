import base64
import requests
import logging

logger = logging.getLogger(__name__)


def list_subfolder(organization, repo_url, gitlab_token, folder="."):
    url = f"https://{organization}/api/v4/projects/{repo_url}/repository/tree"
    headers = {"PRIVATE-TOKEN": gitlab_token}
    params = {"ref": "main", "path": folder}

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


def read_repo_file(organization, repo_url, gitlab_token, file_path):
    file_path = file_path.replace("/", "%2F")
    url = f"https://{organization}/api/v4/projects/{repo_url}/repository/files/{file_path}"
    params = {"ref": "main"}
    headers = {"PRIVATE-TOKEN": gitlab_token}

    response = requests.get(url, headers=headers, params=params)
    file = response.json()
    if "content" in file:
        file_content = base64.b64decode(file["content"]).decode("utf-8")
    else:
        return None
    return file_content
