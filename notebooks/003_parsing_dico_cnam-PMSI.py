# -*- coding: utf-8 -*-
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

import os
os.chdir("..")

# # Préparation 

# ## Imports

from pprint import pprint

# +
import pandas as pd

pd.options.display.max_columns = 100
pd.options.display.max_colwidth = 200
# -

from src.utils import get_all_schema_path
from tableschema import Schema

# ## Lecture et mise en forme

csv_files = [
    "Tables_PMSI_HAD_181214170821.csv",
"Tables_PMSI_MCO_181214170820.csv",
"Tables_PMSI_PSY_181214170823.csv",
"Tables_PMSI_SSR_181214170822.csv"
]

# +
df_list = []
for csv_name in csv_files:
    df = pd.read_csv("notebooks/Envoi_Dico Alimentation/" + csv_name, 
                 encoding="latin1", sep=';', dtype='str')
    columns = list(df.columns)
    df["produit"] = csv_name[7:15]
    
    df = df[["produit"] + columns]
    df_list.append(df)

df_table = pd.concat(df_list)
# -

df_table.columns = ['produit', 
              'name_table', 
                    'type_table',
              'title_table', 
              "date_created_table",
              "date_deleted_table",
                    "variable_jointure",
                    "champ",
                    "observation",
                    "regle_gestion",
                    "concept"
             ]

csv_files = [
    "Variables_PMSI_HAD_181214170822.csv",
"Variables_PMSI_MCO_181214170820.csv",
"Variables_PMSI_PSY_181214170824.csv",
"Variables_PMSI_SSR_181214170823.csv"
]

# +
df_list = []
for csv_name in csv_files:
    df = pd.read_csv("notebooks/Envoi_Dico Alimentation/" + csv_name, 
                 encoding="latin1", sep=';', dtype='str')
    columns = list(df.columns)
    df["produit"] = csv_name[10:18]
    
    df = df[["produit"] + columns]
    df_list.append(df)

df = pd.concat(df_list)
# -

df.columns = ['produit', 
              'name_table', 
              'title_table', 
              'name', 
              'type', 
              'length',
              'description',
              "variable_jointure",
              "dateCreated",
              "dateDeleted",
              "observation_variable",
              'regle_gestion', 
              'famille_concept', 
              "date_created_table",
              "date_deleted_table",
              "sensible_ou_medicale"
             ]

df.head(2)

df.duplicated().sum()

df = df.drop_duplicates()

# ## Standardize values

def map_with_mapping(s):
    if s in mapping:
        return mapping[s]
    return s

# ### fillna et strip
#

df = df.fillna("")

df_table = df_table.fillna("")

for column in df.columns:
    df[column] = df[column].str.strip()

for column in df_table.columns:
    df_table[column] = df_table[column].str.strip()

# ### name_table

df.name_table = df.name_table.str.upper()

df.name_table = df.name_table.str[:5] + 'aa_nn' + df.name_table.str[7:]

df_table.name_table = df_table.name_table.str[:5] + 'aa_nn' + df_table.name_table.str[7:]

df.loc[df.name_table == "T_MCOaa_nnLACT", "name_table"] = "T_MCOaa_nnSUP_LACT"

# ### description

df.description = df.description.str.replace("", "’")

df.description = df.description.str.replace("", "œ")

# ### produit

df.produit.value_counts()

mapping = {
    'PMSI_MCO': 'PMSI MCO',
    'PMSI_SSR' : 'PMSI SSR',
    "PMSI_HAD" : "PMSI HAD",
    "PMSI_PSY" : "PMSI RIM-P"
}
df.produit = df.produit.map(lambda s: mapping[s] if s in mapping else s)
df.produit.value_counts()

# ## name

df[df.name != df.name.str.strip()]

# ### type

df.type.value_counts()

df[df.type == "FAUX"]

df.loc[df.name == "ETA_NUM_JUR", "type"] = 'string' # Numero finess

df.loc[df.name == "ETA_NUM_PMSI", "type"] = 'string' # Numero finess e-pmsi

df.loc[df.name == "ENT_AM", "type"] = "date" # date ou string dans les autres tables

df.loc[df.name == "SOR_AM", "type"] = "date" # date ou string dans les autres tables

df.loc[df.name == "UCD_NBR_ETH", "type"] = "number"
df.loc[df.name == "UCD_NBR_TOT", "type"] = "number"

df.loc[df.name == "ANN_IVG_PREC", "type"] = "string" # on conserve l'ancienne valeur et la même pour totue les tables

df.loc[df.name == "ACH_PRI_DER", "type"] = "number" # prix
df.loc[df.name == "MOY_PRI", "type"] = "number" # prix

df[df.name == "ANN_IVG_PREC"] 

# +
mapping = {
    "Numérique": "number",
    "Caractère": "string",
    "Date": "date",
    "numérique": "number",
    "caractère": "string",
    "VARCHAR2": "string",
    "Varchar": "string",
    "date": "date",
    "FAUX": "datetime"
}
df.type = df.type.map(lambda s: mapping[s] if s in mapping else s)

df.type.value_counts()
# -
# ### lenght

mask = (df.length.str.contains('\.') | df.length.str.contains('\,'))
df[mask].head(2)

df.loc[(df.name == "nbligne") & (df.length == "20"), "length"] = "10"

df.loc[(df.length == "0"), "length"] = None

df.loc[(df.length == ""), "length"] = None

df.length = df.length.str.replace('.', ',').str.strip(',')

df.loc[df.length.str.contains(",") & (df.type == "string"), "type"] = "number"

# ### TODO (?) : Empilement des tables MCOaa_nnGV

mask = df.name_table.str.contains("nnGV")
df[mask].name_table.value_counts()

for name_table in df[mask].name_table.unique():
    print(name_table)
    print(df[df.name_table == name_table].dateDeleted.nunique())

df[mask].name.value_counts()

list(df.columns)

df.loc[mask & (df.name == "ETA_NUM")]

var_columns = ['name', 'type', 'length', 'description', 'variable_jointure', 'observation_variable', 
           'regle_gestion', 'famille_concept', 'sensible_ou_medicale']

for name in df[mask].name.unique():
    print("\n# ", name)
    print(df.loc[mask & (df.name == name), var_columns].replace("", pd.np.nan).nunique())

# ## Create descriptor

def get_field_descriptor(df, name, columns):
    return (df[df.name.str.upper() == name.upper()][columns]
            .to_dict(orient="records")[0])

df_table.head(2)

list(df_table.observation.unique())

list(df_table.champ.unique())

list(df_table.regle_gestion.unique())

for i, (produit, name_table) in df[["produit", 'name_table']].drop_duplicates().iterrows():
    # Restriction table
    sdf = df[(df.produit == produit) & (df.name_table == name_table)]
    
    assert sdf.title_table.nunique() == 1
    title = sdf.title_table.unique()[0]
    
    assert sdf.date_created_table.nunique() == 1
    date_created_table = sdf.date_created_table.unique()[0]

    assert sdf.date_deleted_table.nunique() == 1
    date_deleted_table = sdf.date_deleted_table.unique()[0]

    sdf_table = df_table[df_table.name_table == name_table]
    # print(name_table)
    assert len(sdf_table) == 1
    
    title = sdf_table.title_table.unique()[0]
    date_created_table = sdf_table.date_created_table.unique()[0]
    date_deleted_table = sdf_table.date_deleted_table.unique()[0]

    observation = sdf_table.observation.unique()[0]
    champ = sdf_table.champ.unique()[0]
    regle_gestion = sdf_table.regle_gestion.unique()[0]
    
    
    table_descriptor = {
        "name": name_table, 
        "title": title, 
        "produit": produit,
        "history": {
            "dateCreated": date_created_table,
            "dateDeleted": date_deleted_table,
        }
    }
    
   
    schema_path = "schemas/PMSI/{}/{}.json".format(produit, name_table)
    #print()
    #print(produit, name_table, title) 
    assert os.path.exists(schema_path)
#    if not os.path.exists(schema_path):
#        print("- Creating schema")
#        table_descriptor["history"]["dateMissing"] = []
#        table_descriptor["description"] = ""
#        schema = Schema(table_descriptor)
#    else :
    schema = Schema(schema_path)
    table_descriptor["history"]["dateMissing"] = schema.descriptor["history"]["dateMissing"]
    
    description = schema.descriptor.pop("description", "")
    if len(description):
        assert description.startswith("Champ")
        
        old_champ = description[8:]
    
    champ = old_champ if not len(champ) else champ
    
    schema.descriptor["champ"] = champ
    
    schema.descriptor.update(table_descriptor)

    
    
    # Différences d'ensembles de variables
    schema_names = set([name.upper() for name in schema.field_names]) 
    dico_names = set(sdf.name.str.upper())
    set_dico_schema = dico_names - schema_names

    if set_dico_schema:
        for field in set_dico_schema:
            print("- Variable absente dans le schéma et ajoutée automatiquement", field)
            columns_to_use = ['name', 'description', 'type', 'length', 
                              'dateCreated', 'dateDeleted']
            field_descriptor = get_field_descriptor(sdf, field, columns_to_use)
            field_descriptor["nomenclature"] = "-"
            field_descriptor["dateMissing"] = []
            schema.add_field(field_descriptor)
    
            
    # MAJ variables
    for field in schema.descriptor['fields']:
        name = field['name']
        if not name.upper() in dico_names:
            #print(";".join([produit, name_table, name])) #, field["description"]]))
            #print('- Variable absente dans le dico cnam', name)
            continue

        columns_to_update = ['description', 'type', 'length', "dateCreated", 'dateDeleted']
        #columns_to_update = ['dateCreated']
        field_descriptor = get_field_descriptor(sdf, name, columns_to_update)
        for key in columns_to_update:
            if field_descriptor[key] == "" or field_descriptor[key] is None:
                field_descriptor.pop(key)
        field.update(field_descriptor)
    
    try:
        schema.commit(strict=True)
    except Exception as e:
        print(e.errors)
        raise e
    
    schema.save(schema_path, ensure_ascii=False)

1


