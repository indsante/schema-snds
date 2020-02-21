import os
import shlex
import shutil
import subprocess
from os.path import exists
from os.path import join as pjoin
from pathlib import Path

from src.constants import SCHEMAS_DIR, DOCUMENTATION_SCHEMAS_MD_DIR, ROOT_DIR, TEMPLATES_PATH
from src.utils import get_all_schema_path


def convert_schema_to_md(schema_path):
    md_path = schema_path.replace(SCHEMAS_DIR, DOCUMENTATION_SCHEMAS_MD_DIR).replace(".json", ".md")
    os.makedirs(Path(md_path).parent, exist_ok=True)

    command = f"table-schema-to-markdown '{schema_path}' " \
              f"--template '{TEMPLATES_PATH}' --fields-format table"

    command_list = shlex.split(command)
    with open(md_path, 'w') as f:
        subprocess.run(command_list, check=True, stdout=f)


def generate_schema_md(work_dir, products):
    shutil.rmtree(pjoin(work_dir, DOCUMENTATION_SCHEMAS_MD_DIR), ignore_errors=True)

    for schema_path in get_all_schema_path(work_dir, products):
        convert_schema_to_md(schema_path)

