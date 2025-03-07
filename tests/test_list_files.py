from src.utils import iterate_folder, iterate_folder_simple

# load dotenv in order to get the token
from dotenv import load_dotenv
import os

load_dotenv()

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")


def test_content_generation():
    directory, content, n_files = iterate_folder_simple(
        organation="",
        repo_url="global-data-science%2Fgenai%2Fmotors-seller-assistant",
        gitlab_token=GITLAB_TOKEN,
    )

    # 1st approach
    d1, c1, n_files1 = iterate_folder(
        organation="",
        repo_url="global-data-science%2Fgenai%2Fmotors-seller-assistant",
        gitlab_token=GITLAB_TOKEN,
    )

    d1 == directory
    c1 == content
    n_files == n_files1
    assert True
