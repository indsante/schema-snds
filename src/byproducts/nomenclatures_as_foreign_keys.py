"""
L'objectif de ces fonctions est de créer des schémas dérivés, dans lesquels les nomenclatures sont des tables,
 reliées par des clés étrangères aux variables.

"""

from typing import Dict

from tableschema import Schema

from src.constants import NO_NOMENCLATURE
from src.utils import get_all_schema_path, get_all_nomenclatures_schema


def replace_nomenclature_by_foreign_key():
    nomenclature_to_fk_reference = build_nomenclature_foreign_keys_reference()

    for source_schema_path in get_all_schema_path():
        schema = Schema(source_schema_path)
        for field in schema.fields:
            nomenclature = field.descriptor.get('nomenclature')
            if nomenclature == NO_NOMENCLATURE:
                continue
            foreign_key = {
                "fields": [field.name],
                "reference": nomenclature_to_fk_reference[nomenclature],
                "description": "Nomenclature"
            }
            if "foreignKeys" in schema.descriptor:
                schema.descriptor["foreignKeys"].append(foreign_key)
            else:
                schema.descriptor["foreignKeys"] = [foreign_key]
        schema.commit(strict=True)

        target_schema_path = source_schema_path.replace("schemas", "data/byproducts/schemas_nomenclatures")
        schema.save(target_schema_path, ensure_ascii=False)


def build_nomenclature_foreign_keys_reference() -> Dict[str, dict]:
    nomenclature_to_fk_reference = dict()
    for schema in get_all_nomenclatures_schema():
        name = schema.descriptor.get("name")
        codes = schema.primary_key
        if len(codes) >= 1:
            codes = list()
            for field in schema.fields:
                if field.descriptor.get("role") == "code":
                    codes.append(field.name)
            assert len(codes) == 1

        if codes:
            reference = {
                "resource": name,
                "fields": codes
            }
            nomenclature_to_fk_reference[name] = reference
    return nomenclature_to_fk_reference


if __name__ == '__main__':
    replace_nomenclature_by_foreign_key()
