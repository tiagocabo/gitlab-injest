import logging

from src.gitlab.gitlab_api import list_subfolder, read_repo_file

logger = logging.getLogger(__name__)


def prepare_content(organization, file, repo_url, gitlab_token):
    if ".py" in file or ".md" in file:
        text_header = "=" * 50 + "\n" + file + "\n" + "=" * 50

        content = read_repo_file(organization, repo_url, gitlab_token, file)
        full_content = "\n" + text_header + "\n" + content
    else:
        return ""
    return full_content


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
            full_content += (
                prepare_content(organization, file, repo_url, gitlab_token) + "\n"
            )
        else:
            list_files.append(level * base + marker + file.split("/")[-1] + "/")
            level += 1
            level_files, level_content = prepare_info(
                organization, repo_url, gitlab_token, sub_files, level
            )
            level -= 1
            list_files += level_files
            full_content += level_content + "\n"
    return list_files, full_content


def iterate_folder_simple(organization, repo_url, gitlab_token):
    files = list_subfolder(organization, repo_url, gitlab_token)
    level = 0
    directory, full_content = prepare_info(
        organization, repo_url, gitlab_token, files, level
    )

    return directory, full_content, len(directory)
