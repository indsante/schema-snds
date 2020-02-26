# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# cd ..

from tableschema import Schema
import os

from src.utils import *

# +
for schema_path in get_all_schema_path('.', ['PMSI']):
    schema = Schema(schema_path)
    name = schema.descriptor['name']
    if 'aa_nn' not in name:
        raise ValueError(name)
    schema.descriptor['name'] = name.replace("aa_nn", 'aa')
    schema.commit()
    
    os.remove(schema_path)
    schema.save(schema_path.replace("aa_nn", 'aa'))
    
        
        
