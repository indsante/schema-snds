import logging
import os

from src.constants import ROOT_DIR, SCHEMAS_DIR, SCHEMAS_DOCUMENTATION_SNDS_DIR
from os.path import join as pjoin
import shutil


def generate_documentation_snds(work_dir) -> None:
    rooted_schemas_dir = pjoin(work_dir, SCHEMAS_DIR)
    rooted_schemas_documentation_snds_dir = pjoin(work_dir, SCHEMAS_DOCUMENTATION_SNDS_DIR)
    logging.info("Copy schemas for documentation in directory '{}'"
                 .format(rooted_schemas_documentation_snds_dir))
    if os.path.exists(rooted_schemas_documentation_snds_dir):
        shutil.rmtree(rooted_schemas_documentation_snds_dir)
    shutil.copytree(rooted_schemas_dir, rooted_schemas_documentation_snds_dir)


if __name__ == '__main__':
    generate_documentation_snds(ROOT_DIR)
