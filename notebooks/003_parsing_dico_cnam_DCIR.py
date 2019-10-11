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

# +
import pandas as pd

pd.options.display.max_columns = 100
# -

from src.utils import get_all_schema_path
from tableschema import Schema

# ## Lecture et mise en forme

df_table = pd.read_csv("notebooks/Envoi_Dico Alimentation/Table_Modele_181214170700.csv", encoding="latin1", sep=';')

df_table = df_table.drop(columns=["Unnamed: 8"])

df_table.columns = [
              'name_table', 
              'title_table',
              'description_table',
    'produit', 
              'mode_acces',
              'univers', 
              'renvoi_libelle', 
              'renvoi_description', 
]

df_table.sample(10)

df = pd.read_csv("notebooks/Envoi_Dico Alimentation/Table_Variable_Modele_181214170701.csv", 
                 encoding="latin1", sep=';')
df = df.drop(columns=['Chemin', 'Unnamed: 21', 'Unnamed: 22'])

df.columns = ['produit', 
              'name_table', 
              'title_table', 
              'name', 
              'description',
              'famille_concept', 
              'length', 
              'type', 
              'nomenclature', 
              'elementaire_ou_calculee', 
              'classe_donnee', 
              'regle_gestion', 
              'observation_variable',
              'sensible_ou_medicale', 
              'type_objet', 
              'mode_acces',
              'observation_produit_variable', 
              'liaison', 
              'observation_cumul', 
              'referentiel']

df.head(2)

df.duplicated().sum()

df = df.drop_duplicates()

# ## Signification variable Liaison
# combinaison du nom de table et variable, ou produit et …

mask = ((df.name_table + df.name != df.liaison) & 
        (df.produit + df.name != df.liaison) & 
        (df.produit + df.name_table != df.liaison)
       )
df[mask].liaison.str[:4].value_counts()

# ## Nomenclatures

# +
from src.utils import get_all_nomenclatures_csv_schema_path

nomenclatures_set = set(csv_path.split("/")[-1][:-4] for csv_path, _ in get_all_nomenclatures_csv_schema_path())
# -

# ## Standardize values

def map_with_mapping(s):
    if s in mapping:
        return mapping[s]
    return s

# ### fillna et strip
#

df = df.fillna("")

for column in df.columns:
    df[column] = df[column].str.strip()

# ### name_table

df.name_table = df.name_table.str.upper()

df[df.name_table == "DA_PRA_R"]

# ### produit

mapping = {
    'CMDC': 'Causes de décès',
    'CARTO' : 'CARTOGRAPHIE_PATHOLOGIES',
    "IR_BEN_R" : "BENEFICIAIRE",
    "IR_IBA_R" : "BENEFICIAIRE",
    "IR_IMB_R" : "DCIR_DCIRS",
    "IR_ORC_R" : "DCIR_DCIRS",
    "IR_ETM_R" : "DCIR_DCIRS",
    "IR_ACS_R" : "DCIR_DCIRS",
    "IR_MAT_R" : "DCIR_DCIRS",
    "IR_MTT_R" : "DCIR_DCIRS"
}
df.produit = df.produit.map(lambda s: mapping[s] if s in mapping else s)
df.produit.value_counts()

mapping = {
    'Référentiel médicalisé du SNIIRAM-SNDS': 'Référentiel médicalisé des bénéficiaires (ALD)',
    'Dépenses des 57 millions dassurés sélectionnés': "Table dépenses de la cartographie des pathologies pour l'année AAAA et l'algorithme N",
    'Identifiants des 57 millions dassurés sélectionnés de lannée yyyy': "Table individus de la cartographie des pathologies pour l'année AAAA et l'algorithme N",
    'Caractérisation des 57 M dassurés pr 56 grp de pathologies': "Table pathologies de la cartographie des pathologies pour l'année AAAA et l'algorithme N",    
}
df.title_table = df.title_table.map(lambda s: mapping[s] if s in mapping else s)

# #### Carto

# +
# => Vérification que toutes les tables sont identiques en fonction des années pour la carto

for table in ['DEP', 'IDE', 'IND']:
    for year1, year2 in [('2013', '2014'), ('2014', '2015')]:
        table1 = 'CT_{}_{}_G4'.format(table, year1)
        table2 = 'CT_{}_{}_G4'.format(table, year2)
        df1 = df[df.name_table == table1].reset_index(drop=True).drop(columns="name_table")
        df2 = df[df.name_table == table2].reset_index(drop=True).drop(columns="name_table")
        assert df1.equals(df2)
# -

# Remise en forme du nom des tables
mask = df.name_table.str.startswith("CT_")
df.name_table[mask] = df[mask].name_table.str[:7] + 'AAAA_GN'
df = df.drop_duplicates()

# #### name

df.name = df.name.str.rstrip("\xa0")

# ### referentiel

mapping = {
    'IR_IBA_R': 'IR_IBA_R',
    'référentiel des bénéficiaires du SNIIRAM IR_BEN_R' : 'IR_BEN_R',
    'DA_PRA_R': 'DA_PRA_R',
    'T_NMED - Référentiel des Médicaments': 'T_NMED',
    'RG_AR_DET_FT - DA_PRA_R': 'RG_AR_DET_FT - DA_PRA_R',
    'SNDA': 'SNDA',
    'Fichier National des Professionnels de Santé (FNPS)': 'FNPS',
}
df.referentiel = df.referentiel.map(map_with_mapping)
df.referentiel.value_counts()

# ### elementaire

mapping = {
    'Elémentaire': 'Élémentaire', 
    'Calculée': 'Calculée', 
    'Calculé': 'Calculée', 
    'Élémentaire': 'Élémentaire'
}
df.elementaire_ou_calculee = df.elementaire_ou_calculee.map(map_with_mapping)
df.elementaire_ou_calculee.value_counts()

# ### type

# +
mapping = {
    "Numérique": "number",
    "Caractère": "string",
    "Date": "date",
    "numérique": "number",
    "caractère": "string",
    "VARCHAR2": "string",
    "Varchar": "string",
    "date": "date"
}
df.type = df.type.map(lambda s: mapping[s] if s in mapping else s)

df.type.value_counts()
# -

df.loc[df.name == "IND_RNM_BEN", "description"] = "Top RNIAM"
df.loc[df.name == "IND_RNM_BEN", "type"] = "string"
df.loc[df.name == "IND_RNM_BEN", "length"] = "1"

df[df.type == ""]

# ### lenght

df.loc[df.name == "ARO_THE_TAU", "length"] = "5"

mask = (df.length.str.contains('\.') | df.length.str.contains('\,'))
df[mask].head(2)

df.length = df.length.str.replace('.', ',').str.strip(',')

# ### nomenclatures

# DONE
# - X ne pas prendre les nouveaux ir_pha_r dans er_pha_r et ns_pha_r
# - X ER_TIP_F/NS_PRS_F : TIP_ACT_PRU -> pas IR_DTE_V (prix)
# - X ER_TIP_F/NS_PRS_F : TIP_PUB_PRX -> pas IR_PRF_V (prix)
# - X IR_IMB_R : INS_DTE -> pas IR_IMB_R
# - X NS_BIO_F : BIO_ACT_QSN -> pas IR_BIO_R (quantité)
# - X NS_PHA_F : PHA_ACT_PRU -> pas IR_PHA_R
# - X dans dcir simplifié remplacer partout IR_ACT_V, IR_SPE_V par IR_SPA_D
# - CT_IND_AAAA_GN : beaucoup d'erreurs a priori
# - problème nomenclatures multiples
# - BE_IDE_R à traiter (on l'a pas, la récupérer ?)

# ##### DONE
#
#

# +
mask = df.nomenclature.str.contains(',')

df.loc[mask,["name_table", "name", "nomenclature"]]
# -

df.loc[mask, 'nomenclature'] = ''

mask = (df.nomenclature.isin(["BE_IDE_R"]))
df.loc[mask,["produit", "name_table", "name", "nomenclature"]]
df.loc[mask, 'nomenclature'] = ''

df.nomenclature = (df.nomenclature
                   .replace('IR_ACT_V, IR_SPE_V', "IR_SPA_D")
                   .replace('IR_IMB_R', '')
                  )

mask = df.name.isin(['PHA_ACT_PRU', 'BIO_ACT_QSN', 'INS_DTE', 'TIP_PUB_PRX', 'TIP_ACT_PRU'])
df.loc[mask, 'nomenclature'] = ''

mask = (df.nomenclature == "IR_PHA_R") & df.name_table.isin(['ER_PHA_F', 'NS_PHA_F'])
df.loc[mask, 'nomenclature'] = ''

mask = (df.name_table.isin(['CT_IND_AAAA_GN']) & df.nomenclature.isin(['IR_PRF_V', "IR_PHA_R", "IR_DTE_V"]))
df.loc[mask, 'nomenclature'] = ''

mask = (df.name_table.isin(['ER_DCT_F']) & df.nomenclature.isin(["IR_PMC_V"]))
df.loc[mask, 'nomenclature'] = ''

mask = df.name.isin(['INS_DTE'])
df[mask]

# ### description

df[df.description.str.contains("EPK")].description

# +
for abbrev, nom in [
    ("Cpt", "comptable"),
    ("Regul", "régulation"),
    ("Dcpte", "décompte"),
    ("Prs", "Prestation"),
    ("Pharma", "pharmacie"),
    ("EPK","Entente Préalable kinésithérapie")

]:
    df.description = df.description.str.replace(abbrev, nom)
# -

mapping = {
    "anomalie": "",
}
df.description = df.description.map(lambda s: mapping[s] if s in mapping else s)

# ## Préparation produits

# +
produit_a_garder = [
    'CARTOGRAPHIE_PATHOLOGIES',
 'DCIR',
 'DCIRS',
 'Causes de décès',
 'DCIR_DCIRS',
 'BENEFICIAIRE',
 ]

df = df[df.produit.isin(produit_a_garder)]
# -

df.regle_gestion.nunique()

df.head()

# ## Create descriptor

def get_field_descriptor(df, name, columns):
    return (df[df.name.str.upper() == name.upper()][columns]
            .to_dict(orient="records")[0])

for i, (produit, name_table) in df[["produit", 'name_table']].drop_duplicates().iterrows():
    # Restriction table
    sdf = df[(df.produit == produit) & (df.name_table == name_table)]
    
    assert sdf.title_table.nunique() == 1
    title = sdf.title_table.unique()[0]

   
    # Lecture schema
    schema_path = "schemas/{}/{}.json".format(produit, name_table)
    assert os.path.exists(schema_path)
    schema = Schema(schema_path)

    
    # MAJ table
    schema.descriptor.update({
        "name": name_table, 
        "title": title, 
        "produit": produit
    })
        
    # Différences d'ensembles de variables
    schema_names = set([name.upper() for name in schema.field_names]) 
    dico_names = set(sdf.name)
    set_schema_dico = schema_names - dico_names
    set_dico_schema = dico_names - schema_names
      

    if set_dico_schema:
        for field in set_dico_schema:
            print("- Variable absente dans le schéma et ajoutée automatiquement", field)
            columns_to_use = ['name', 'description', 'type', 'length', 'nomenclature']
            field_descriptor = get_field_descriptor(sdf, field, columns_to_use)
            field_descriptor["dateCreated"] = ""
            field_descriptor["dateDeleted"] = ""
            field_descriptor["dateMissing"] = []
            field_descriptor["nomenclature"] = "-" if field_descriptor["nomenclature"] == "" else field_descriptor["nomenclature"]
            print(field_descriptor)
            schema.add_field(field_descriptor)   
            
    
    # MAJ variables
    for field in schema.descriptor['fields']:
        #print()
        #print(produit, name_table, title) 

        name = field['name']
        if not name.upper() in dico_names:
            
            #print('- Variable absente dans le dico cnam', name)
            print(";".join([produit, name_table, name]))

            continue
        
        columns_to_update = ['description', 'type', 'nomenclature', 'length']
        columns_to_update = ['nomenclature']
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


