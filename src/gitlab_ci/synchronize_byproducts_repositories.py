import logging
import os
import shlex
import shutil
import subprocess
from os.path import join as pjoin
from typing import List, Tuple

import requests

from src.constants import BYPRODUCTS_DIR

GITLAB_TOKEN = os.environ.get('GITLAB_TOKEN', None)

HDH_GITLAB_URL = 'https://gitlab.com/healthdatahub'
GITLAB_COM_API_V4 = 'https://gitlab.com/api/v4'
TMP_DIR = 'tmp'
LIST_TUPLE_STR_STR = List[Tuple[str, str]]


def synchronize_all_byproducts() -> None:
    if GITLAB_TOKEN is None:
        logging.error("GITLAB TOKEN is not set. "
                      "This is expected, if we are not executing on GitLab-CI runners, for protected branches. "
                      "Exiting, as we cannot automatically synchronize byproducts. "
                      )
        return

    current_commit = bash("git rev-parse --verify HEAD").strip()
    shutil.rmtree(TMP_DIR, ignore_errors=True)

    synchronize_byproduct_repository_with_local_changes(current_commit,
                                                        byproduct_repository="documentation-snds",
                                                        byproduct_project_id=11935953,
                                                        local_to_byproduct_directories=[('markdown', 'docs/tables')],
                                                        local_to_byproduct_files=[
                                                            ('tables_sidebar.js', 'docs/.vuepress/tables_sidebar.js')],
                                                        automatic_merge=True)

    synchronize_byproduct_repository_with_local_changes(current_commit,
                                                        byproduct_repository="dico-snds",
                                                        byproduct_project_id=11925754,
                                                        local_to_byproduct_directories=[],
                                                        local_to_byproduct_files=[
                                                            ('snds_links.csv', 'app/app_data/snds_links.csv'),
                                                            ('snds_nodes.csv', 'app/app_data/snds_nodes.csv'),
                                                            ('snds_tables.csv', 'app/app_data/snds_tables.csv'),
                                                            ('snds_vars.csv', 'app/app_data/snds_vars.csv')
                                                        ],
                                                        automatic_merge=True)


def synchronize_byproduct_repository_with_local_changes(current_commit: str,
                                                        byproduct_repository: str, byproduct_project_id: int,
                                                        local_to_byproduct_directories: LIST_TUPLE_STR_STR,
                                                        local_to_byproduct_files: LIST_TUPLE_STR_STR,
                                                        automatic_merge: bool = False) -> None:
    """
    Synchronize byproduct repository with byproduct version in this repository current commit

    :param current_commit: commit sha
    :param byproduct_repository: repository name
    :param byproduct_project_id: byproduct GitLab project id
    :param local_to_byproduct_directories: directories to erase and replace from this repository to byproduct repository
    :param local_to_byproduct_files: files to replace from this repository to byproduct repository
    :param automatic_merge: do we approve and merge Merge Request automatically when pipeline succeeds
    """
    clone_repository_to_tmp_directory(byproduct_repository)
    copy_local_to_byproduct_repository(byproduct_repository, local_to_byproduct_directories, local_to_byproduct_files)

    current_dir = os.getcwd()
    os.chdir(pjoin(TMP_DIR, byproduct_repository))
    if not bash("git status --porcelain"):
        logging.info("No modifications in target repository. Exit.")
    else:
        bash("git config user.name 'schema-snds GitLab-CI robot'")
        bash('git config user.email "ld-lab-github@sante.gouv.fr"')
        branch_name = "update-from-schema-snds-{}".format(current_commit)
        commit_and_push_modifications(branch_name, current_commit)

        merge_request_iid = create_merge_request(byproduct_project_id, branch_name, byproduct_repository)
        if automatic_merge:
            merge_when_pipeline_succeeds(byproduct_project_id, merge_request_iid)

    os.chdir(current_dir)


def clone_repository_to_tmp_directory(repository_name: str):
    git_clone_cmd = \
        "git clone https://oauth2:{gitlab_token}@gitlab.com/healthdatahub/{repository}.git/ tmp/{repository}" \
            .format(gitlab_token=GITLAB_TOKEN, repository=repository_name)
    bash(git_clone_cmd)


def copy_local_to_byproduct_repository(byproduct_repository: str,
                                       local_to_byproduct_directories: LIST_TUPLE_STR_STR,
                                       local_to_byproduct_files: LIST_TUPLE_STR_STR):
    for source_dir, target_dir in local_to_byproduct_directories:
        copy_directory_to_byproduct_repository(source_dir, byproduct_repository, target_dir)
    for source_file, target_file in local_to_byproduct_files:
        copy_file_to_byproduct_repository(source_file, byproduct_repository, target_file)


def copy_file_to_byproduct_repository(source_file: str, byproduct_repository: str, target_file: str) -> None:
    """
    Replace file in byproducts's repository local copy by source file.
    """
    source_file_path = pjoin(BYPRODUCTS_DIR, byproduct_repository, source_file)
    target_file_path = pjoin(TMP_DIR, byproduct_repository, target_file)
    shutil.copy(source_file_path, target_file_path)


def copy_directory_to_byproduct_repository(source_dir: str, byproduct_repository: str, target_dir: str) -> None:
    """
    Erase target directory in byproduct's repository local copy. Replace it with source directory.
    """
    source_dir_path = pjoin(BYPRODUCTS_DIR, byproduct_repository, source_dir)
    target_dir_path = pjoin(TMP_DIR, byproduct_repository, target_dir)
    shutil.rmtree(target_dir_path, ignore_errors=True)
    shutil.copytree(source_dir_path, target_dir_path)


def commit_and_push_modifications(branch_name: str, current_commit: str):
    bash("git checkout -b {}".format(branch_name))
    bash("git add -A")

    commit_message = "MAJ automatique depuis 'schema-snds', commit {}\n\n" \
                     "Cf '{}/{}/commit/{}'".format(current_commit, HDH_GITLAB_URL, 'schema-snds', current_commit)

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
    logging.info("Execute: {}".format(bash_command.replace(GITLAB_TOKEN, 'XXXXXXXX')))
    bash_command_list = shlex.split(bash_command)
    return subprocess.check_output(bash_command_list).decode()


def check_response_code(response: requests.Response, expected_status_code: int) -> None:
    response_log_msg = ('{} {}\n{}'
                        .format(response.status_code, response.reason, response.text)
                        .replace(GITLAB_TOKEN, 'XXXXXXXX')
                        )
    if response.status_code != expected_status_code:
        logging.error(response_log_msg)
        raise Exception("wrong status_code")
    else:
        logging.debug(response_log_msg)


if __name__ == '__main__':
    synchronize_all_byproducts()
