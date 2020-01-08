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

# # Travail sur le fichier d'annotation de données synthétiques

import os
os.chdir("..")

import pandas as pd

! wget https://docs.google.com/spreadsheets/d/1NdNcJ2qRvvimplX6WavupJAJ_VtriiEgOJr8F8IEmac/export?format=csv -O data/retour_synthetic_snds.csv

df_retour = pd.read_csv('data/retour_synthetic_snds.csv')
df_retour.head()

df_snds_var = pd.read_csv('data/byproducts/dico-snds/snds_vars.csv')
df_snds_var.head()

df_retour = df_retour[["table", "var", "Commentaire modification", "Relecteur", "Relu"]]

df_snds_var = df_snds_var[["table", "var","format", "description", "nomenclature"]]

df_snds_var.merge(df_retour, 
                  on=["table", "var"],
                  how="left"
                 ).to_csv("data/retour_synthetic_snds-updated.csv", index=False)


