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
from typing import Dict

from tableschema import Schema

from src.constants import NO_NOMENCLATURE, ROOTED_SCHEMAS_DIR, ROOTED_NOMENCLATURES_DIR, NOMENCLATURES_DIR, \
    SCHEMAS_SYNTHETIC_SNDS_DIR, NOMENCLATURES_SYNTHETIC_SNDS_DIR
from src.constants import STRING, NUMBER, INTEGER
from src.utils import get_all_schema_path, get_all_nomenclatures_schema


def generate_synthetic_snds():
    generate_tsfaker_schemas()
    copy_nomenclatures_for_tsfaker()
    run_tsfaker()


def run_tsfaker():
    tsfaker_cmd = "tsfaker {schemas_dir} " \
                  "--resources {nomenclatures} " \
                  "--output {fake_dir} " \
                  "--nrows 10 " \
                  "--overwrite  " \
                  "--limit-fk 10 " \
                  "--logging-level WARNING" \
        .format(schemas_dir=SCHEMAS_SYNTHETIC_SNDS_DIR,
                nomenclatures=NOMENCLATURES_DIR,
                fake_dir=SCHEMAS_SYNTHETIC_SNDS_DIR)
    logging.info("Use tsfaker to generate fake data.")
    logging.info("Command used: '{}'".format(tsfaker_cmd))
    os.makedirs(SCHEMAS_SYNTHETIC_SNDS_DIR, exist_ok=True)
    subprocess.run(tsfaker_cmd.split())


def copy_nomenclatures_for_tsfaker():
    logging.info("Copy nomenclatures for tsfaker in directory '{}'"
                 .format(NOMENCLATURES_SYNTHETIC_SNDS_DIR))
    if os.path.exists(NOMENCLATURES_SYNTHETIC_SNDS_DIR):
        shutil.rmtree(NOMENCLATURES_SYNTHETIC_SNDS_DIR)
    shutil.copytree(ROOTED_NOMENCLATURES_DIR, NOMENCLATURES_SYNTHETIC_SNDS_DIR)


def generate_tsfaker_schemas():
    logging.info("Build standard tables schemas for tsfaker in directory '{}'"
                 .format(SCHEMAS_SYNTHETIC_SNDS_DIR))
    nomenclature_to_fk_reference = build_nomenclature_to_foreign_keys_reference()

    for source_schema_path in get_all_schema_path():
        schema = Schema(source_schema_path)
        replace_length_by_bounds_and_number_by_integer(schema)
        replace_nomenclatures_by_foreign_key_reference(schema, nomenclature_to_fk_reference)
        schema.commit(strict=True)

        target_schema_path = source_schema_path.replace(ROOTED_SCHEMAS_DIR, SCHEMAS_SYNTHETIC_SNDS_DIR)
        schema.save(target_schema_path, ensure_ascii=False)


def replace_length_by_bounds_and_number_by_integer(schema):
    for field in schema.fields:
        tstype = field.descriptor.get('type')
        length = field.descriptor.get('length')
        if length is None:
            continue

        if ',' in length:
            assert tstype == NUMBER
            length, decimals = length.split(',')
            assert schema.update_field(field.name,
                                       {'constraints': {'minimum': 0, 'maximum': 10 ** int(length),
                                                        'decimals': int(decimals)}})
            continue

        length = int(length)
        if tstype == STRING:
            assert schema.update_field(field.name, {'constraints': {'maximum': length}})
        if tstype == NUMBER:
            assert length <= 19, "   - field '{}' of schema '{}' is of length '{}'"\
                .format(field.name, schema.descriptor["name"], length)
            assert schema.update_field(field.name,
                                       {'type': INTEGER, 'constraints': {'minimum': 0, 'maximum': 10 ** length}})


def replace_nomenclatures_by_foreign_key_reference(schema, nomenclature_to_fk_reference):
    for field in schema.fields:
        nomenclature = field.descriptor.get('nomenclature')
        if nomenclature == NO_NOMENCLATURE:
            continue
        if nomenclature not in nomenclature_to_fk_reference:
            raise ValueError("Nomenclature {} is referenced in schemas, but missing in nomenclatures' folder."
                             .format(nomenclature))
        foreign_key = {
            "fields": [field.name],
            "reference": nomenclature_to_fk_reference[nomenclature],
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
    generate_synthetic_snds()
