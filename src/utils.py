import requests
import base64


def list_subfolder(organization, repo_url, gitlab_token, folder="."):
    url = f"https://{organization}/api/v4/projects/{repo_url}/repository/tree"
    headers = {"PRIVATE-TOKEN": gitlab_token}
    params = {"ref": "main", "path": folder}

    for attempt in range(3):
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            try:
                files = response.json()
                return [file["path"] for file in files]
            except ValueError:
                print("Failed to parse JSON response.")
                return []
        elif response.status_code == 404:
            print("Folder not found.")
            return []
        else:
            print(
                f"Attempt {attempt + 1}: Request failed with status code {response.status_code}: {response.text}"
            )

    print("All retry attempts failed.")
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


def prepare_content(organization, file, repo_url, gitlab_token):
    if ".py" in file or ".md" in file:
        text_header = "=" * 50 + "\n" + file + "\n" + "=" * 50

        content = read_repo_file(organization, repo_url, gitlab_token, file)
        full_content = "\n" + text_header + "\n" + content
    else:
        return ""
    return full_content


def iterate_folder_simple(organization, repo_url, gitlab_token):
    def prepare_info(organization, repo_url, gitlab_token, files, level):
        marker = "|----"
        base = "|    "
        list_files = []
        full_content = ""
        while files:
            file = files.pop(0)
            sub_files = list_subfolder(organization, repo_url, gitlab_token, file)
            if not sub_files:
                list_files += [level * base + marker + file.split("/")[-1]]
                full_content += prepare_content(
                    organization, file, repo_url, gitlab_token
                )
            else:
                list_files.append(level * base + marker + file.split("/")[-1] + "/")
                level += 1
                level_files, level_content = prepare_info(
                    organization, repo_url, gitlab_token, sub_files, level
                )
                level -= 1
                list_files += level_files
                full_content += level_content
        return list_files, full_content

    files = list_subfolder(organization, repo_url, gitlab_token)
    level = 0
    directory, full_content = prepare_info(
        organization, repo_url, gitlab_token, files, level
    )

    return directory, full_content, len(directory)
