#!/usr/bin/env python
import argparse

from src.byproducts.main import generate_byproducts
from src.byproducts.synchronize_repositories import synchronize_all_byproducts

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Création de produits dérivés depuis les schémas du SNDS')
    parser.add_argument('--erd', dest='generate_erd',
                        action='store_const', const=True, default=False,
                        help="Générer un diagramme d'entité relationnelle (ERD), "
                             "en utilisant PostgreSQL et schema-crawler (nécessite Docker)")
    parser.add_argument('--synchronize', dest='synchronize', action='store_const',
                        const=True, default=False,
                        help="Synchronizer les modifications dans les dépôts des produits dérivés. "
                             "Cette action n'est déclenchée que par GitLab-CI")

    args = parser.parse_args()

    generate_byproducts(args.generate_erd)

    if args.synchronize:
        synchronize_all_byproducts()
