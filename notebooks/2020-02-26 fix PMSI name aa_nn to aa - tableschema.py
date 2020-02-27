# -*- coding: utf-8 -*-
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

# # Changement des noms des tables du PMSI dans les schéma json
#
# Ce code a une **erreur**, il le modifie pas les clés étrangères 
# non corrigé car on utilise le code de Lorien qui manipule les json

# cd schema-snds/

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
    schema.save(schema_path.replace("aa_nn", 'aa'), ensure_ascii=False)



# -

# # Changement des noms des tables du PMSI dans les fichiers markdown de documentation

import os

# cd ../inds/Documentation-SNDS/

for dir_path, dir_names, file_names in os.walk('tables/'):
    for file in file_names:
        if file.endswith('.md') and 'aa_nn' in file:
            file_path = os.path.join(dir_path, file)
            with open(file_path, 'r') as f:
                content = f.read()
            assert 'aa_nn' in content
            os.remove(file_path)
            
            content = content.replace('aa_nn', 'aa')
            with open(file_path.replace('aa_nn', 'aa'), 'w') as f:
                f.write(content)


