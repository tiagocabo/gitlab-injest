import pyperclip
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

    list_files, full_content, n_files = iterate_folder_simple(organization, repo_url, gitlab_token)


    with col1:
        enc = tiktoken.get_encoding("o200k_base")

        count_tokens = len(enc.encode(full_content))
        text_summary = st.text_area("Summary",
                       f""" **Repository**:  {gitlab_repo} \n\n **Analysed files**:  {n_files} \n\n **Token Count**:  {count_tokens} Openai tokens""",
                       height=200)
        
        if st.button('Copy', key="copy Summary"):
            pyperclip.copy(text_summary)
            st.success('Text copied successfully!')


    with col2:
        directory_text = st.text_area("List of files", "Repo structure:\n" + "\n".join(list_files), height=200)
        if st.button('Copy', key="copy directory"):
            pyperclip.copy(directory_text)
            st.success('Text copied successfully!')

    ta = st.text_area("File Content", full_content, height=600)
    if st.button('Copy', key="copy content"):
        pyperclip.copy(ta)
        st.success('Text copied successfully!')
