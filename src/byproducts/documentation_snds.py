import shutil
from os.path import join as pjoin
from os.path import exists
from pathlib import Path
from src.constants import SCHEMAS_DIR, SCHEMAS_MD_DIR, TEMPLATES_DIR, ROOT_DIR
from src.utils import get_all_schema_path
import subprocess


def convert_schema_to_md(file_path, template, fields_format):
    file_path_dst = file_path.replace(SCHEMAS_DIR, SCHEMAS_MD_DIR)
    schemas_md_path = Path(file_path_dst).parent.as_posix().replace(" ", "\\ ")
    subprocess.run("mkdir -p " + schemas_md_path, shell=True)

    cmd = "table-schema-to-markdown " + file_path.replace(" ", "\\ ") + \
          " --template=" + template + " --fields-format="+fields_format+" >> " + \
          file_path_dst.replace(".json", ".md").replace(" ", "\\ ")

    subprocess.run(cmd, shell=True)


def generate_schema_md(work_dir):
    # delete the current generated md schemas if exist
    if exists(pjoin(work_dir, SCHEMAS_MD_DIR)):
        shutil.rmtree(pjoin(work_dir, SCHEMAS_MD_DIR))

    for schema in get_all_schema_path(work_dir):
        convert_schema_to_md(schema, TEMPLATES_DIR+"/template_schema.hbs", "table")


if __name__ == '__main__':
    generate_schema_md(ROOT_DIR)
