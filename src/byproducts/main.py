import logging
import shutil
import os
from os.path import exists
from os.path import join as pjoin
import subprocess
from src.byproducts.dico_snds import generate_dico_snds
from src.byproducts.documentation_snds import generate_documentation_snds
from src.byproducts.relational_diagram import generate_relational_diagram
from src.byproducts.tsfaker_schemas import generate_synthetic_snds
from src.constants import BYPRODUCTS_DIR
from pathlib import Path
from src.constants import SCHEMAS_DIR, SCHEMAS_MD_DIR, TEMPLATES_DIR
from src.utils import get_all_schema_path


def generate_byproducts(generate_erd, work_dir):
    rooted_byproducts_dir = pjoin(work_dir, BYPRODUCTS_DIR)

    logging.info("Suppression du dossier '{}' contenant les produits dérivés.".format(rooted_byproducts_dir))
    shutil.rmtree(rooted_byproducts_dir, ignore_errors=True)

    logging.info("Génération des produits dérivés dans le dossier '{}'.".format(rooted_byproducts_dir))
    generate_documentation_snds(work_dir)
    generate_dico_snds(work_dir)
    generate_synthetic_snds(work_dir)

    if generate_erd:
        generate_relational_diagram(work_dir)


def convert_schema_to_md(file_path, template, fields_format):
    file_path_dst = file_path.replace(SCHEMAS_DIR, SCHEMAS_MD_DIR)
    schemas_md_path = Path(file_path_dst).parent.as_posix().replace(" ", "\\ ")
    subprocess.run("mkdir -p " + schemas_md_path, shell=True)

    cmd = "table-schema-to-markdown " + file_path.replace(" ", "\\ ") + \
          " --template=" + template + " --fields-format="+fields_format+" >> " + \
          file_path_dst.replace(".json", ".md").replace(" ", "\\ ")

    subprocess.run(cmd, shell=True)


def generate_schema_md():
    # delete the current generated md schemas if exist
    if exists(SCHEMAS_MD_DIR):
        shutil.rmtree(SCHEMAS_MD_DIR)

    for schema in get_all_schema_path('.'):
        convert_schema_to_md(schema, TEMPLATES_DIR+"/template_schema.hbs", "table")

