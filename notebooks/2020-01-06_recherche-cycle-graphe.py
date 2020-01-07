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

# # Recherche de cycle dans le graphe

! pip install networkx

import os
os.chdir("..")

import networkx as nx

G = nx.read_edgelist("data/byproducts/dico-snds/snds_links.csv", delimiter=',', data=False, create_using=nx.DiGraph)

G.number_of_nodes()

G.number_of_edges()

G.is_directed()

for c in nx.simple_cycles(G):
    print(c)


