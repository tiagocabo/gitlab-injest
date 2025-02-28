import requests
import base64
import streamlit as st

@st.cache_data
def list_repo_tree(organization, repo_url, gitlab_token):
    url = f"https://{organization}/api/v4/projects/{repo_url}/repository/tree?ref=main&recursive=true"
    headers = {
            "PRIVATE-TOKEN": gitlab_token
        }

    response = requests.get(url, headers=headers)
    files = response.json()
    files_list = []
    for file in files:
        files_list.append(file["path"])
    return files_list

@st.cache_data
def list_subfolder(organation, repo_url, gitlab_token, folder="."):
    url = f"https://{organation}/api/v4/projects/{repo_url}/repository/tree?ref=main&path={folder}"
    headers = {
            "PRIVATE-TOKEN": gitlab_token
        }

    response = requests.get(url, headers=headers)
    try:
        files = response.json()
        files_list = []
        for file in files:
            files_list.append(file["path"])
    except:
        return False
    return files_list

@st.cache_data
def read_repo_file(organation, repo_url, gitlab_token, file_path):
    file_path = file_path.replace("/", "%2F")
    url = f"https://{organation}/api/v4/projects/{repo_url}/repository/files/{file_path}"
    params = {'ref': "main"}
    headers = {'PRIVATE-TOKEN': gitlab_token}

    response = requests.get(url, headers=headers, params=params)
    file = response.json()
    if "content" in file:
        file_content = base64.b64decode(file['content']).decode('utf-8')
    else:
        return None
    return file_content

@st.cache_data
def prepare_content(organization, file, repo_url, gitlab_token):
    if ".py" in file or ".md" in file:
        text_header = "="*50 + "\n"+ file + "\n" + "="*50

        content = read_repo_file(organization, repo_url, gitlab_token, file)
        full_content = "\n" + text_header + "\n" + content
    else:
        return ""
    return full_content


@st.cache_data
def iterate_folder(repo_url, gitlab_token):
    base = "|"
    marker = "-"
    list_files = []
    full_content = ""

    files = list_subfolder(repo_url, gitlab_token)

    for file in files:
        if not list_subfolder(repo_url, gitlab_token, file):
            list_files.append(base + 2*marker + file)
            full_content += prepare_content(file, repo_url, gitlab_token)

        else:
            list_files.append(base + 2*marker + file + "/")
            sub_files = list_subfolder(repo_url, gitlab_token, file)
            for sub_file in sub_files:
                if not list_subfolder(repo_url, gitlab_token, sub_file):
                    list_files.append(base + 4*marker + sub_file.split("/")[-1])
                    full_content += prepare_content(sub_file, repo_url, gitlab_token)
                else:
                    list_files.append(base + 4*marker + sub_file.split("/")[-1] + "/")

                    sub_files = list_subfolder(repo_url, gitlab_token, sub_file)
                    for sub_file in sub_files:
                        if not list_subfolder(sub_file, gitlab_token, sub_file):
                            list_files.append(base + 6*marker + sub_file.split("/")[-1])
                            full_content += prepare_content(sub_file, repo_url, gitlab_token)

                        else:
                            sub_files = list_subfolder(repo_url, gitlab_token, sub_file)
    return list_files, full_content, len(list_files)

@st.cache_data
def iterate_folder_simple(organation, repo_url, gitlab_token):
    
    def prepare_info(organation,repo_url, gitlab_token, files, level):
        marker = "|----"
        base = "|    "
        list_files = []
        full_content = ""
        while files:
            file = files.pop(0)
            sub_files = list_subfolder(organation, repo_url, gitlab_token, file)
            if not sub_files :
                list_files += [level*base + marker + file.split("/")[-1]]
                full_content += prepare_content(organation, file, repo_url, gitlab_token)
            else:
                list_files.append(level*base + marker + file.split("/")[-1] + "/")
                level += 1
                level_files, level_content = prepare_info(organation, repo_url, gitlab_token, sub_files, level)
                level -= 1
                list_files += level_files
                full_content += level_content
        return list_files, full_content
                
        
    files = list_subfolder(organation, repo_url, gitlab_token)
    level = 0
    directory, full_content = prepare_info(organation, repo_url, gitlab_token, files, level)
    
    return directory, full_content, len(directory)