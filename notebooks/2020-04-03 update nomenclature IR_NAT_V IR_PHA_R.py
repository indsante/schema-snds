
# Code associated to MR "Mise a jour des nomenclatures IR_NAT_V, IR_PHA_R, CCAM"


# modules ---------------------------------
import pandas as pd
import csv
import json
import numpy as np

# IR_NAT_V --------------------------------
# Parameters -----------------------
new_nom = "./data/IR_NAT_V_V2.csv"
prev_nom = "./data/IR_NAT_V.csv"

# Beginning of code ----------------
df = pd.read_csv(new_nom, sep=";")
prev_df = pd.read_csv(prev_nom, sep=";")

# Clean and transform into csv ----
df = df.sort_values(by=["PRS_NAT"])
prev_df = prev_df.sort_values(by=["PRS_NAT"])

df.to_csv("data/IR_NAT_V_v2_ord.csv", encoding="utf-8", sep=";", index=False)
prev_df.to_csv("data/IR_NAT_V_ord.csv", encoding="utf-8", sep=";", index=False)
# premier commit : remplacer IR_NAT_V par IR_NAT_V_ord
# deuxieme commit : remplacer IR_NAT_V_ord par IR_NAT_V_v2_ord

# IR_PHA_R ----------------------------------------

# Parameters -----------------------
new_nom = "./data/IR_PHA_R_V2.csv"
prev_nom = "./data/IR_PHA_R.csv"

# Beginning of code ----------------
df = pd.read_csv(new_nom, sep=";", dtype=str)
prev_df = pd.read_csv(prev_nom, sep=";", dtype=str)

len(df.columns)  # 69
len(prev_df.columns)  # 68
df.columns.difference(prev_df.columns)
# Index(['PHA_AST_TOP', 'PHA_CAR_TOP', 'PHA_DAT_OPP', 'PHA_DIA_TOP',
#        'PHA_GRD_CND', 'PHA_HDD_SPE', 'PHA_PRD_UND', 'PHA_PRD_UNI'],
#       dtype='object')
prev_df.columns.difference(df.columns)
# Index(['PHA_ATC_CLA', 'PHA_ATC_LIB', 'PHA_DOS_UNI', 'PHA_EPH_CLA',
#       'PHA_EPH_LIB', 'PHA_SUB_DOS', 'PHA_UPC_NBR'],
#      dtype='object')
# new columns in df that were not in prev_df, and deleted columns

# check primary key unique
print(len(df.loc[:, "PHA_CIP_C13"].unique()) == len(df))
# True
# reorder df to put same column order as prev_df
cols_to_order = list(prev_df.columns & df.columns)
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df = df[new_columns]

# order PHA_CIP_C13 both df and prev_df
df = df.sort_values(by=["PHA_CIP_C13"])
prev_df = prev_df.sort_values(by=["PHA_CIP_C13"])
df.head()
prev_df.head()

# merge with deleted variables to as to keep info from prev_df
missing_cols = list(prev_df.columns.difference(df.columns))
df = pd.merge(df, prev_df.loc[:, ["PHA_CIP_C13"]+missing_cols], on="PHA_CIP_C13", how="left")
prev_df.columns.difference(df.columns)
# all deleted columns were undeleted in new nomenclature
# new columns were added to json

new_cols = df.columns.difference(prev_df.columns)
info_json = df.loc[:, new_cols]
info_json.info()

# check deleted rows, new rows, both in table
df_merge = pd.merge(df.loc[:, ["PHA_CIP_C13"]], prev_df, on="PHA_CIP_C13", how="outer", indicator=True)
df_merge["_merge"].value_counts()
# both          19517
# left_only      6903
# right_only        0
# 0 deleted rows from right table

# export clean csv for schema
df.to_csv("data/IR_PHA_R_v2_ord.csv", encoding="utf-8", sep=";", index=False, quoting=csv.QUOTE_ALL, quotechar='"')
prev_df.to_csv("data/IR_PHA_R_ord.csv", encoding="utf-8", sep=";", index=False, quoting=csv.QUOTE_ALL, quotechar='"')


# Re export this consolidated nomenclature with correct types -------------------------
with open('data/IR_PHA_R.json') as json_file:
    data = json.load(json_file)
data = data["fields"]
data = pd.json_normalize(data)
data.type.value_counts()
# We transform the json types into readable types by pandas (note the capital
# letter on Int64 which allows for nan in integer dtype (not possible with int64)
data.loc[:, "type_py"] = np.select(
    [data["type"] == "integer",
     data["type"] == "string",
     data["type"] == "number"],
    ["Int64",
     "str",
     "float64"]
)
dict_type = pd.Series(data.type_py.values, index=data.name).to_dict()
df = pd.read_csv("data/IR_PHA_R_v2_ord.csv", encoding="utf-8", sep=";", dtype=dict_type)
# Export clean csv with correct dtypes
df.to_csv("data/IR_PHA_R_v2_ord.csv", na_rep="NA", encoding="utf-8", sep=";", index=False,
          quoting=csv.QUOTE_NONNUMERIC, quotechar='"')
