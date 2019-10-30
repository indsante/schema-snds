# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # ajout d'un double champ type

import os
os.chdir("..")

from src.utils import get_all_schema_path
from tableschema import Schema

for schema_path in get_all_schema_path():
    schema = Schema(schema_path)
    name = schema.descriptor["name"]
    for field in schema.descriptor['fields']:
        field.update({"type_oracle": field['type']})
    
    try:
        schema.commit(strict=True)
    except Exception as e:
        print(e.errors)
        raise e
    
    schema.save(schema_path, ensure_ascii=False)

for schema_path in get_all_schema_path("tests/schemas"):
    schema = Schema(schema_path)
    name = schema.descriptor["name"]
    for field in schema.descriptor['fields']:
        field.update({"type_oracle": field['type']})
    
    try:
        schema.commit(strict=True)
    except Exception as e:
        print(e.errors)
        raise e
    
    schema.save(schema_path, ensure_ascii=False)


