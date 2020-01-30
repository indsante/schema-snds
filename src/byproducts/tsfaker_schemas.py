"""
L'objectif de ces fonctions est de générer des données synthétiques avec tsfkaker.
On commence par transformer les schémas pour transformer les informations en contraintes formalisées avec table schema:
- les nomenclatures comme des clés étrangères
- la longueur des champs comme des bornes en taille

"""

import logging
import os
import shutil
import subprocess
from os.path import join as pjoin
from shutil import copyfile
from typing import Dict

from tableschema import Schema

from src.constants import NO_NOMENCLATURE, IGNORED_DATE_NOMENCLATURE, SCHEMAS_DIR, NOMENCLATURES_DIR, BYPRODUCTS_DIR, ROOT_DIR
from src.constants import STRING, NUMBER, INTEGER, TYPE_CSV
from src.utils import get_all_schema_path, get_all_nomenclatures_schema, get_used_nomenclatures

SYNTHETIC_SNDS_DIR = pjoin(BYPRODUCTS_DIR, "synthetic-snds")


def generate_synthetic_snds(work_dir):
    rooted_schemas_synthetic_snds_dir = pjoin(work_dir, SYNTHETIC_SNDS_DIR, SCHEMAS_DIR)

    generate_tsfaker_schemas(rooted_schemas_synthetic_snds_dir, work_dir)
    copy_nomenclatures_for_tsfaker(work_dir)
    run_tsfaker(rooted_schemas_synthetic_snds_dir)


def run_tsfaker(rooted_schemas_synthetic_snds_dir):
    tsfaker_cmd = "tsfaker {schemas_dir} " \
                  "--resources {nomenclatures} " \
                  "--output {fake_dir} " \
                  "--nrows 10 " \
                  "--overwrite  " \
                  "--limit-fk 10 " \
                  "--logging-level WARNING" \
        .format(schemas_dir=rooted_schemas_synthetic_snds_dir,
                nomenclatures=NOMENCLATURES_DIR,
                fake_dir=rooted_schemas_synthetic_snds_dir)
    logging.info("Use tsfaker to generate fake data.")
    logging.info("Command used: '{}'".format(tsfaker_cmd))
    os.makedirs(rooted_schemas_synthetic_snds_dir, exist_ok=True)
    subprocess.run(tsfaker_cmd.split())


def copy_nomenclatures_for_tsfaker(work_dir):
    used_nomenclatures = get_used_nomenclatures(work_dir)
    rooted_nomenclatures_dir = pjoin(work_dir, NOMENCLATURES_DIR)
    rooted_nomenclatures_synthetic_snds_dir = pjoin(work_dir, SYNTHETIC_SNDS_DIR, NOMENCLATURES_DIR)
    logging.info("Copy nomenclatures for tsfaker in directory '{}'"
                 .format(rooted_nomenclatures_synthetic_snds_dir))
    if os.path.exists(rooted_nomenclatures_synthetic_snds_dir):
        shutil.rmtree(rooted_nomenclatures_synthetic_snds_dir)

    os.makedirs(rooted_nomenclatures_synthetic_snds_dir, exist_ok=True)
    for root, dirs, files in os.walk(rooted_nomenclatures_dir):
        for file in files:
            if file[:-4] in used_nomenclatures or file[:-5] in used_nomenclatures:
                source_file_path = pjoin(root, file)
                target_dir_path = root.replace(rooted_nomenclatures_dir, rooted_nomenclatures_synthetic_snds_dir)
                target_file_path = pjoin(target_dir_path, file)

                os.makedirs(target_dir_path, exist_ok=True)
                copyfile(source_file_path, target_file_path)


def generate_tsfaker_schemas(rooted_schemas_synthetic_snds_dir, work_dir):
    logging.info("Build standard tables schemas for tsfaker in directory '{}'"
                 .format(rooted_schemas_synthetic_snds_dir))
    nomenclature_to_fk_reference = build_nomenclature_to_foreign_keys_reference()

    for source_schema_path in get_all_schema_path(work_dir):
        schema = Schema(source_schema_path)
        replace_length_by_bounds(schema)
        get_enum_constraints(schema)
        replace_nomenclatures_by_foreign_key_reference(schema, nomenclature_to_fk_reference)
        schema.commit(strict=True)

        target_schema_path = source_schema_path.replace(SCHEMAS_DIR, pjoin(SYNTHETIC_SNDS_DIR, SCHEMAS_DIR))
        schema.save(target_schema_path, ensure_ascii=False)


def replace_length_by_bounds(schema):
    # logging.debug(" - Replace for schema '{}'".format(schema.descriptor["name"]))
    for field in schema.fields:
        # logging.debug("   - Replace for field '{}'".format(field.descriptor["name"]))
        tstype = field.descriptor.get(TYPE_CSV)
        length = field.descriptor.get('length')
        if length is None:
            continue

        if ',' in length:
            assert tstype == NUMBER, "field '{}' of schema '{}' is of lenght '{}' and type '{}'" \
                .format(field.name, schema.descriptor["name"], length, tstype)
            length, decimals = length.split(',')
            assert schema.update_field(field.name,
                                       {'constraints': {'minimum': 0, 'maximum': 10 ** int(length),
                                                        'decimals': int(decimals)}})
            continue

        length = int(length)
        constraints = field.descriptor.get('constraints')
        if tstype == STRING:
            minlength = constraints.get('minLength') if constraints and constraints.get('minLength') else None
            if minlength:
                assert schema.update_field(field.name, {'constraints': {'minLength': minlength, 'maxLength': length}})
            else:
                assert schema.update_field(field.name, {'constraints': {'maxLength': length}})
        if tstype == INTEGER:
            assert length <= 19, "field '{}' of schema '{}' is of length '{}', bigger than maximal value of 19" \
                .format(field.name, schema.descriptor["name"], length)
            if constraints:
                minimum = constraints.get('minimum') if constraints.get('minimum') else 0
                maximum = constraints.get('maximum') if constraints.get('maximum') else 10 ** length
            else:
                minimum, maximum = 0, 10 ** length
            assert schema.update_field(field.name, {'constraints': {'minimum': minimum, 'maximum': maximum}})


def get_enum_constraints(schema):
    for field in schema.fields:
        constraints = field.descriptor.get('constraints')
        if constraints and constraints.get('enum'):
            assert schema.update_field(field.name, {'constraints': {'enum': constraints.get('enum')}})


def replace_nomenclatures_by_foreign_key_reference(schema, nomenclature_to_fk_reference):
    for field in schema.fields:
        nom_col = field.descriptor.get('nomenclature').split(':')
        nomenclature = nom_col[0]
        if nomenclature == NO_NOMENCLATURE or nomenclature == IGNORED_DATE_NOMENCLATURE:
            continue
        if nomenclature not in nomenclature_to_fk_reference:
            raise ValueError("Nomenclature {} is referenced in schemas, but missing in nomenclatures' folder."
                             .format(nomenclature))
        if len(nom_col) > 1:
            reference = {
                "resource": nomenclature,
                "fields": [nom_col[1]]
            }
        else:
            reference = nomenclature_to_fk_reference[nomenclature]

        foreign_key = {
            "fields": [field.name],
            "reference": reference,
            "description": "Nomenclature"
        }
        if "foreignKeys" in schema.descriptor:
            schema.descriptor["foreignKeys"].append(foreign_key)
        else:
            schema.descriptor["foreignKeys"] = [foreign_key]


def build_nomenclature_to_foreign_keys_reference() -> Dict[str, dict]:
    nomenclature_to_fk_reference = dict()
    for schema in get_all_nomenclatures_schema():
        name = schema.descriptor.get("name")
        codes = schema.primary_key
        if len(codes) == 0:
            raise ValueError("Nomenclature {} should have a primary Key".format(name))

        if len(codes) >= 1:
            codes = list()
            for field in schema.fields:
                if field.descriptor.get("role") == "code":
                    codes.append(field.name)
            if len(codes) != 1:
                raise ValueError("Nomenclature {} should have one and one variable with role 'code'".format(name))

        reference = {
            "resource": name,
            "fields": codes
        }
        nomenclature_to_fk_reference[name] = reference
    return nomenclature_to_fk_reference


if __name__ == '__main__':
    copy_nomenclatures_for_tsfaker(ROOT_DIR)
    # generate_synthetic_snds(ROOT_DIR)
