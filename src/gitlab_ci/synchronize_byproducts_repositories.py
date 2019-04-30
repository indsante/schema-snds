import logging
import os
import shlex
import shutil
import subprocess
from os.path import join as pjoin
from typing import List, Tuple

import requests

from src.constants import BYPRODUCTS_DIR

GITLAB_TOKEN = os.environ['GITLAB_TOKEN']

HDH_GITLAB_URL = 'https://gitlab.com/healthdatahub'
GITLAB_COM_API_V4 = 'https://gitlab.com/api/v4'
TMP_DIR = 'tmp'
LIST_TUPLE_STR_STR = List[Tuple[str, str]]


def main():
    current_commit = bash("git rev-parse --verify HEAD").strip()

    synchronize_byproduct_repository(current_commit,
                                     repository_name="documentation-snds",
                                     project_id=11935953,
                                     local_to_target_directories=[('markdown', 'docs/tables')],
                                     local_to_target_files=[('tables_sidebar.js', 'docs/.vuepress/tables_sidebar.js')],
                                     automatic_merge=True)

    synchronize_byproduct_repository(current_commit,
                                     repository_name="dico-snds",
                                     project_id=11925754,
                                     local_to_target_directories=[],
                                     local_to_target_files=[
                                         ('snds_links.csv', 'app/app_data/snds_links.csv'),
                                         ('snds_nodes.csv', 'app/app_data/snds_nodes.csv'),
                                         ('snds_tables.csv', 'app/app_data/snds_tables.csv'),
                                         ('snds_vars.csv', 'app/app_data/snds_vars.csv')
                                     ])


def synchronize_byproduct_repository(current_commit: str, repository_name: str, project_id: int,
                                     local_to_target_directories: LIST_TUPLE_STR_STR,
                                     local_to_target_files: LIST_TUPLE_STR_STR,
                                     automatic_merge: bool = False) -> None:
    clone_repository_to_tmp_directory(repository_name)
    copy_local_to_target_repository(repository_name, local_to_target_directories, local_to_target_files)

    os.chdir(pjoin(TMP_DIR, repository_name))
    if not bash("git status --porcelain"):
        logging.info("No modifications in target repository. Exit.")
        return

    bash("git config user.name 'schema-snds GitLab-CI robot'")
    bash('git config user.mail "ld-lab-github@sante.gouv.fr"')
    branch_name = "update-from-schema-snds-{}".format(current_commit)
    commit_and_push_modifications(branch_name, current_commit)

    merge_request_iid = create_merge_request(project_id, branch_name, repository_name)
    if automatic_merge:
        merge_when_pipeline_succeeds(project_id, merge_request_iid)


def clone_repository_to_tmp_directory(repository_name: str):
    shutil.rmtree(TMP_DIR, ignore_errors=True)
    git_clone_cmd = "git clone https://oauth2:{gitlab_token}@gitlab.com/healthdatahub/{repository}.git/ tmp/{repository}" \
        .format(gitlab_token=GITLAB_TOKEN, repository=repository_name)
    bash(git_clone_cmd)


def copy_local_to_target_repository(repository_name: str, local_to_target_directories: LIST_TUPLE_STR_STR,
                                    local_to_target_files: LIST_TUPLE_STR_STR):
    for source_dir, target_dir in local_to_target_directories:
        copy_directory_to_target_repository(source_dir, repository_name, target_dir)
    for source_file, target_file in local_to_target_files:
        copy_file_to_target_repository(source_file, repository_name, target_file)


def copy_file_to_target_repository(source_file: str, target_repo: str, target_file: str) -> None:
    source_file_path = pjoin(BYPRODUCTS_DIR, target_repo, source_file)
    target_file_path = pjoin(TMP_DIR, target_repo, target_file)
    shutil.copy(source_file_path, target_file_path)


def copy_directory_to_target_repository(source_dir: str, target_repo: str, target_dir: str) -> None:
    source_dir_path = pjoin(BYPRODUCTS_DIR, target_repo, source_dir)
    target_dir_path = pjoin(TMP_DIR, target_repo, target_dir)
    shutil.rmtree(target_dir_path, ignore_errors=True)
    shutil.copytree(source_dir_path, target_dir_path)


def commit_and_push_modifications(branch_name: str, current_commit: str):
    bash("git checkout -b {}".format(branch_name))
    bash("git add -A")

    commit_message = "MAJ automatique depuis 'schema-snds', commit {}\n\nCf '{}/{}/commit/{}'".format(
        current_commit, HDH_GITLAB_URL, 'schema-snds', current_commit)

    bash("git commit -m '{}'".format(commit_message))
    bash("git push --set-upstream origin {}".format(branch_name))


def create_merge_request(project_id: int, source_branch: str, repository_name: str) -> int:
    logging.info("Create merge request for branch '{}".format(source_branch))
    r = requests.post(
        GITLAB_COM_API_V4 + "/projects/{}/merge_requests".format(project_id),
        params={
            'source_branch': source_branch,
            'target_branch': 'master',
            'title': "MAJ automatique depuis 'schema-snds'",
            'remove_source_branch': 'true',
            'private_token': GITLAB_TOKEN
        }
    )
    check_response_code(r, 201)
    merge_request_iid = r.json()['iid']
    logging.info("Merge request '{}/{}/merge_requests/{}' was created.".format(
        HDH_GITLAB_URL, repository_name, merge_request_iid))
    return merge_request_iid


def merge_when_pipeline_succeeds(project_id: int, merge_request_iid: int) -> None:
    logging.info('Accept merge request with automatic merge when pipeline succeeds.')
    r = requests.put(
        GITLAB_COM_API_V4 + "/projects/{}/merge_requests/{}/merge".format(project_id, merge_request_iid),
        params={
            'merge_when_pipeline_succeeds': 'true',
            'private_token': GITLAB_TOKEN
        }
    )
    check_response_code(r, 200)


def bash(bash_command: str) -> str:
    logging.info("Execute: {}".format(bash_command))
    bash_command_list = shlex.split(bash_command)
    return subprocess.check_output(bash_command_list).decode()


def check_response_code(response: requests.Response, expected_status_code: int) -> None:
    response_log_msg = '{} {}\n{}'.format(response.status_code, response.reason, response.text)
    if response.status_code != expected_status_code:
        logging.error(response_log_msg)
        raise Exception("wrong status_code")
    else:
        logging.debug(response_log_msg)


if __name__ == '__main__':
    main()
