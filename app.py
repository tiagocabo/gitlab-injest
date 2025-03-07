import streamlit as st
import tiktoken
from src.utils import iterate_folder_simple

gitlab_repo = st.text_input("Provide Gitlab Url.")

with st.sidebar:
    gitlab_token = st.text_input("Gitlab Token", type="password")


col1, col2 = st.columns(2)


if gitlab_repo:
    # remove https if present
    gitlab_repo = gitlab_repo.replace("https://", "")

    # extract organization
    organization = gitlab_repo.split("/")[0]

    gitlab_repo = "/".join(gitlab_repo.split("/")[1:])

    # parse url
    repo_url = gitlab_repo.replace("/", "%2F")

    list_files, full_content, n_files = iterate_folder_simple(
        organization, repo_url, gitlab_token
    )

    with col1:
        enc = tiktoken.get_encoding("o200k_base")

        count_tokens = len(enc.encode(full_content))
        text_summary = st.code(
            f""""Summary"\n **Repository**:  {gitlab_repo} \n\n **Analysed files**:  {n_files} \n\n **Token Count**:  {count_tokens} Openai tokens""",
            language="text",
            height=300,
        )

    with col2:
        directory_text = st.code(
            "List of files \n Repo structure:\n" + "\n".join(list_files),
            language="text",
            height=300,
        )

    ta = st.code("Repo Contents: \n " + full_content, language="text", height=600)
