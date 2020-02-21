import os
from os.path import join as pjoin

import pandas as pd

from src.byproducts.dico_snds import table_schema_to_snds_graph, DICO_EDGES_CSV, DICO_NODES_CSV
from src.constants import DICO_SNDS_DIR, ROOT_DIR


def test_no_isolated_table():
    os.makedirs(DICO_SNDS_DIR, exist_ok=True)
    table_schema_to_snds_graph(ROOT_DIR, products=None)

    df_edges = pd.read_csv(pjoin(DICO_SNDS_DIR, DICO_EDGES_CSV))
    df_nodes = pd.read_csv(pjoin(DICO_SNDS_DIR, DICO_NODES_CSV))

    connected_tables = set(df_edges["source"]).union(set(df_edges["target"]))

    print("Tables non connectées : \n{}"
          .format(df_nodes.loc[~df_nodes["index"].isin(connected_tables), ['name', 'description']]))

    assert len(connected_tables) == len(df_nodes)
