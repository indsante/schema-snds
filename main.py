#!/usr/bin/env python
# coding: utf-8
import argparse
import logging

from src.byproducts.main import generate_byproducts
from src.byproducts.update_byproducts_repositories import update_all_byproducts
from src.constants import ROOT_DIR
from src.utils import get_logging_level_value, check_products_list, get_all_products

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Création de produits dérivés depuis les schémas du SNDS')
    parser.add_argument('-p', '--products', dest='products', nargs='*', action='store', default=None,
                        help="Se restreindre à certains sous-produits")
    parser.add_argument('-d', '--erd', dest='generate_erd',
                        action='store_const', const=True, default=False,
                        help="Générer un diagramme d'entité relationnelle (ERD), "
                             "en utilisant PostgreSQL et schema-crawler (nécessite Docker)")
    parser.add_argument('-u', '--update', dest='update', action='store_const',
                        const=True, default=False,
                        help="Propagation des modifications du schéma dans les dépôts des produits dérivés. "
                             "Cette action n'est déclenchée que par GitLab-CI")
    parser.add_argument('-l', '--local', dest='local', action='store_const',
                        const=True, default=False,
                        help="Tester un update des produits dérivés en local, sans mettre à jour le remote.")
    parser.add_argument('--log', dest='logging_level', action='store', default="INFO",
                        help="Choisir le niveau de log.")

    args = parser.parse_args()
    logging.basicConfig(level=get_logging_level_value(args.logging_level),
                        format='%(asctime)s :: %(levelname)s :: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        )

    check_products_list(args.products)
    args.products = args.products or get_all_products()

    generate_byproducts(args.generate_erd, ROOT_DIR, args.products)

    if args.update or args.local:
        update_all_byproducts(args.local, ROOT_DIR)
