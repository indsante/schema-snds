import argparse

from src.build_tableschema.add_keys import add_primary_and_foreign_keys_to_tableschema
from src.build_tableschema.reformat_snds_dico import build_tableschema_from_dico_snds
from src.byproducts.dico_snds import generate_dico_snds
from src.byproducts.documentation_snds import generate_documentation_snds
from src.byproducts.relational_diagram import generate_relational_diagram
from src.gitlab_ci.synchronize_byproducts_repositories import synchronize_all_byproducts
from src.utils import reset_data_directory

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Création du schéma du SNDS et de produits dérivés')
    parser.add_argument('--erd', dest='generate_erd',
                        action='store_const', const=True, default=False,
                        help="Générer un diagramme d'entité relationnelle (ERD), "
                             "en utilisant PostgreSQL et schema-crawler (nécessite Docker)")
    parser.add_argument('--synchronize_byproducts', dest='synchronize_byproducts', action='store_const',
                        const=True, default=False,
                        help="Synchronizer les modifications dans les produits dérivés. "
                             "Cette action n'est déclenchée que par GitLab-CI")

    args = parser.parse_args()

    if args.synchronize_byproducts:
        synchronize_all_byproducts()
        exit()

    reset_data_directory()

    # Building tableschema
    build_tableschema_from_dico_snds()
    add_primary_and_foreign_keys_to_tableschema()

    # Generating tableschema byproducts
    generate_documentation_snds()
    generate_dico_snds()

    if args.generate_erd:
        generate_relational_diagram()
