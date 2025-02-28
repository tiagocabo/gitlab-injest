import pytest

from src.utils import iterate_folder, iterate_folder_simple

def test_content_generation():
    directory, content, n_files = iterate_folder_simple(repo_url="global-data-science%2Fgenai%2Fmotors-seller-assistant", gitlab_token=token)

    # 1st approach
    d1,c1,n_files1 = iterate_folder(repo_url="global-data-science%2Fgenai%2Fmotors-seller-assistant", gitlab_token=token)

    d1 == directory
    c1 == content
    n_files == n_files1
    assert True