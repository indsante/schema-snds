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

import pandas as pd

# cd ../data/byproducts/synthetic-snds/schemas/DCIR/

df1 = pd.read_csv("ER_PHA_F.csv", sep=',')

df2 = pd.read_csv("ER_PRS_F.csv", sep=',')

keys = [
        "DCT_ORD_NUM",
        "FLX_DIS_DTD",
        "FLX_EMT_NUM",
        "FLX_EMT_ORD",
        "FLX_EMT_TYP",
        "FLX_TRT_DTD",
        "ORG_CLE_NUM",
        "PRS_ORD_NUM",
        "REM_TYP_AFF"
    ]

df2[keys].sort_values(by="DCT_ORD_NUM")

df1[keys].sort_values(by="DCT_ORD_NUM")



df1["DCT_ORD_NUM"]
