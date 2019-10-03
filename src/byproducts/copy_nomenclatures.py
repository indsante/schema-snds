import logging
import os
from shutil import copyfile

from src.constants import NOMENCLATURES_DICO_SNDS, ROOTED_NOMENCLATURES_DIR


def cp_nomenclatures():
    logging.info("Copy the csv in {} subdirectories into {}".format(
        ROOTED_NOMENCLATURES_DIR,
        NOMENCLATURES_DICO_SNDS
    ))
    os.makedirs(NOMENCLATURES_DICO_SNDS)
    for root, dirs, files in os.walk(ROOTED_NOMENCLATURES_DIR):
        for file in files:
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(NOMENCLATURES_DICO_SNDS, file)
            if source_file_path.endswith('.csv'):
                copyfile(source_file_path, target_file_path)
