# UPDATING LPP

# Modules ------------------------
import pandas as pd
import os
from dbfread import DBF
print(os.getcwd())

# Parameters -----------------------
new_nom = "./data/NT_LPP_V2.csv"  # nomenclature cnam actuelle
prev_nom = "./data/NT_LPP.csv"  # nomenclature presente schema

# Beginning of code ----------------
df = pd.read_csv(new_nom, sep=";", dtype=str)
prev_df = pd.read_csv(prev_nom, sep=";", dtype=str)
print(df.columns == prev_df.columns)

# Clean and transform into csv ----
df = df.sort_values(by=["LPP_PRS_IDE"])
prev_df = prev_df.sort_values(by=["LPP_PRS_IDE"])

if len(df.LPP_PRS_IDE.unique()) == df.shape[0]:
    print("Primary key unique")
# ok

# Difference with previous nomenclature -------------------------------------
diff = pd.merge(df, prev_df, on="LPP_PRS_IDE", how="outer", indicator=True)
diff["_merge"].value_counts()
# left_only     13335
# both           6276
# right_only        0
appeared_codes = diff.loc[diff["_merge"] == "left_only", :]
print(appeared_codes.shape)
# il manque tout l'optique dans lpp, tout le 100 % santé

# Comparison with dbf CNAM file --------------------------------------
# file dbf http://www.codage.ext.cnamts.fr/codif/tips//telecharge/index_tele.php?p_site=AMELI
table = DBF('./data/lpp_fiche_tot577.dbf', encoding="cp850")
frame = pd.DataFrame(iter(table))
print(frame.head())
print(frame.columns)

frame = frame.rename(columns={"CODE_TIPS": "LPP_PRS_IDE",
                              "NOM_COURT": "LPP_RED_LIB",
                              "AGE_MAX": "LPP_MAX_AGE",
                              "TYPE_PREST": "LPP_PRS_TYP",
                              "DATE_FIN": "LPP_VAL_DTF"})
frame = frame.loc[:, ['LPP_PRS_IDE', 'LPP_RED_LIB', 'LPP_MAX_AGE', 'LPP_PRS_TYP', 'LPP_VAL_DTF']]
print(frame.shape)  # (19717, 5)
print(len(frame.LPP_PRS_IDE.unique()) == frame.shape[0])  # ok primary key unique

compare_dbf = pd.merge(df, frame, on='LPP_PRS_IDE', indicator=True, how="outer")
compare_dbf["_merge"].value_counts()
# both          19610
# right_only      107
# left_only         1
right_only_codes = compare_dbf.loc[compare_dbf["_merge"] == "right_only", :]
# ok on va ajouter ces codes à la nomenclature
left_only_codes = compare_dbf.loc[compare_dbf["_merge"] == "left_only", :]
# 1 code erreur, sur la recherche par code cnam aucun code n'est associé à ceci
# il faut donc faire un left join de frame par rapport à df
# et exporter ceci comme la nomenclature correcte


new_df = pd.merge(frame["LPP_PRS_IDE"], df, on='LPP_PRS_IDE',
                  how="left", indicator=True)
new_df["_merge"].value_counts()
# both          19610
# left_only       107
# right_only        0

# Divide into both and left, and fill left_only columns with values from `frame` columns
left_only = new_df.loc[new_df["_merge"] == "left_only", :]
both = new_df.loc[new_df["_merge"] == "both", :]

temp = left_only.loc[:, left_only.columns.isin(['LPP_RED_LIB', 'LPP_MAX_AGE', 'LPP_PRS_TYP', 'LPP_VAL_DTF']) == False]
left_only = pd.merge(temp.drop(columns="_merge"), frame, on="LPP_PRS_IDE", how="left")

new_df = pd.concat([both.drop(columns="_merge"), left_only])
print(new_df.shape)  # (19717, 18)
print(new_df.columns == df.columns)
print(new_df.columns == prev_df.columns)
if len(new_df.LPP_PRS_IDE.unique()) == new_df.shape[0]:
    print("Primary Key unique")

# Now comparing consolidated nomenclature with previous nomenclature ------------------
diff = pd.merge(new_df, prev_df, on="LPP_PRS_IDE", how="outer", indicator=True)
diff["_merge"].value_counts()
# left_only     13441
# both           6276
# right_only        0
appeared_codes = diff.loc[diff["_merge"] == "left_only", :]

# Export to CSV ordered by LPP_PRS_IDE ---------------------
new_df = new_df.sort_values("LPP_PRS_IDE")
new_df.to_csv("data/NT_LPP_V2_ord.csv", encoding="utf-8", sep=";", index=False)
prev_df.to_csv("data/NT_LPP_ord.csv", encoding="utf-8", sep=";", index=False)
