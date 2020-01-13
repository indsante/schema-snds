import pandas as pd
import numpy as np
import re
import os

import sys
sys.path.append('../')
from src.utils import get_all_schema
from tableschema import Schema

from typing import List

path2schemas = '../'


def change_field(
        schemas_dir: str,
        var_name_regex: str,
        replaced_field_name: str,
        replacing_field_content: str,
        filtered_in_produits: List[str] = [],
        verbose: int = 1,
        save: bool = True) -> List[Schema]:
    """
    Description: Change all fields in given filtered products when variables names match a given regex
    """
    new_schemas = []
    schemas = get_all_schema(schemas_dir)

    for schema in schemas:
        table_name = schema.descriptor['name']
        table_produit = schema.descriptor['produit']
        table_variables = schema.descriptor['fields']
        # print(table_produit)
        if (table_produit in filtered_in_produits) | (filtered_in_produits == []):
            if verbose >= 2:
                print(table_name)
            for var in table_variables:
                if re.search(var_name_regex, var['name']) is not None:
                    if verbose >= 1:
                        print(table_name + '__' + var['name'])
                    replacing_field = {replaced_field_name: replacing_field_content}
                    schema.update_field(var['name'], replacing_field)
                    schema.commit()
        new_schemas.append(schema)
        if save:
            if re.search('PMSI', table_produit) is not None:
                save_path = os.path.join(schemas_dir, 'schemas', 'PMSI', table_produit, table_name) + '.json'
            else:
                save_path = os.path.join(schemas_dir, 'schemas', table_produit, table_name) + '.json'
            schema.save(save_path, ensure_ascii=False)
    return new_schemas

schemas_dir = path2schemas

filtered_in_produits = ['PMSI MCO', 'PMSI HAD', 'PMSI SSR', 'PMSI RIM-P']
var_name_regex = '_RET$'
replacing_field_content = '1' #'boolean'
replaced_field_name = 'length' #'type'

schemas_w_good_ret = change_field(
    schemas_dir=schemas_dir,
    var_name_regex=var_name_regex,
    replacing_field_content=replacing_field_content,
    replaced_field_name=replaced_field_name,
    filtered_in_produits=filtered_in_produits,
    save=False)

# check for MCO_C
schemas_w_good_ret[100].descriptor


