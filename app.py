import streamlit as st
import tiktoken
from src.gitlab.gitlab_api import list_branches
from src.utils import iterate_folder_simple
from src.config import SUPPORTED_EXTENSIONS

if "AVAILABLE_BRANCHES" not in st.session_state:
    st.session_state.AVAILABLE_BRANCHES = "main"


with st.container():
    gitlab_repo = st.text_input("Provide Gitlab Url.")

c1, c2, c3 = st.columns(3)
exclude_all = c1.text_input("Exclude all i.e .md;.ipynb", value=".ipynb")
include_only = c2.text_input("Include only i.e .py;.txt")
branch = c3.selectbox("Pick your branch", st.session_state.AVAILABLE_BRANCHES)

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


if gitlab_repo and gitlab_token:
    # remove https if present
    gitlab_repo = gitlab_repo.replace("https://", "")

    # extract organization
    organization = gitlab_repo.split("/")[0]

    gitlab_repo = "/".join(gitlab_repo.split("/")[1:])

    # parse url
    repo_url = gitlab_repo.replace("/", "%2F")

    current_branches = list_branches(organization, repo_url, gitlab_token)
    st.session_state.AVAILABLE_BRANCHES = current_branches

if gitlab_repo and inspect:
    with st.spinner(f"Analysing repo {repo_url} and branch {branch}..."):
        list_files, full_content, n_files = iterate_folder_simple(
            organization, repo_url, gitlab_token, SUPPORTED_EXTENSIONS, branch
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
