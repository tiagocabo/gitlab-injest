import streamlit as st
import tiktoken
from src.utils import iterate_folder_simple
from src.config import SUPPORTED_EXTENSIONS

with st.container():
    gitlab_repo = st.text_input("Provide Gitlab Url.")

c1, c2 = st.columns(2)
exclude_all = c1.text_input("Exclude all i.e .md;.ipynb", value=".ipynb")
include_only = c2.text_input("Include only i.e .py;.txt")

if include_only:
    SUPPORTED_EXTENSIONS = [
        ext for ext in SUPPORTED_EXTENSIONS if ext in include_only.split(";")
    ]

if exclude_all:
    SUPPORTED_EXTENSIONS = [
        ext for ext in SUPPORTED_EXTENSIONS if ext not in exclude_all.split(";")
    ]

inspect = st.button("Inspect")

with st.sidebar:
    gitlab_token = st.text_input("Gitlab Token", type="password")


col1, col2 = st.columns(2)


if gitlab_repo and inspect:
    # remove https if present
    gitlab_repo = gitlab_repo.replace("https://", "")

    # extract organization
    organization = gitlab_repo.split("/")[0]

    gitlab_repo = "/".join(gitlab_repo.split("/")[1:])

    # parse url
    repo_url = gitlab_repo.replace("/", "%2F")

    list_files, full_content, n_files = iterate_folder_simple(
        organization, repo_url, gitlab_token, SUPPORTED_EXTENSIONS
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
            "'Repo structure':\n" + "\n".join(list_files),
            language="text",
            height=300,
        )

    ta = st.code("Repo Contents: \n " + full_content, language="text", height=600)
