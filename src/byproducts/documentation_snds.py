import json
import logging
import os

import table_schema_to_markdown

from src.constants import TABLESCHEMA_DIR, MARKDOWN_DIR, TABLES_SIDEBAR_JS_PATH
from src.utils import get_all_schema_path


def generate_documentation_snds():
    logging.info("Génération de la documentation VuePress")
    generate_markdown()
    generate_table_sidebar()


def generate_markdown() -> None:
    logging.getLogger('table_schema_to_markdown').setLevel(logging.WARNING)
    logging.info("Conversion des schémas en fichier texte Markdown")
    for schema_path in get_all_schema_path():
        markdown_path = schema_path.replace(TABLESCHEMA_DIR, MARKDOWN_DIR).replace('.json', '.md')
        os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
        with open(markdown_path, 'w', encoding='utf8') as out:
            table_schema_to_markdown.convert_source(schema_path, out)


def generate_table_sidebar() -> None:
    logging.info("Genération de la barre de navigation 'table_sidebar.js'")
    sidebar = []
    for product in sorted(os.listdir(TABLESCHEMA_DIR)):
        if product == 'PMSI':
            children = list()
            for subproduct in sorted(os.listdir(os.path.join(TABLESCHEMA_DIR, product))):
                subproduct_path = product + '/' + subproduct
                subchildren = generate_product_directory_children(subproduct_path)
                children.append({
                    'title': subproduct,
                    'children': subchildren
                })
            sidebar.append({
                'title': product,
                'children': children
            })
        else:
            children = generate_product_directory_children(product)
            sidebar.append({
                'title': product,
                'children': children
            })

    with open(TABLES_SIDEBAR_JS_PATH, 'w', encoding='utf8') as f:
        f.write('module.exports =')
        json.dump(sidebar, f, ensure_ascii=False, indent=4)
        f.write(';')


def generate_product_directory_children(product_directory_rel_path):
    product_directory_abs_path = os.path.join(TABLESCHEMA_DIR, product_directory_rel_path)
    table_schema_filenames = sorted(os.listdir(product_directory_abs_path))
    children = list()
    for table_json in table_schema_filenames:
        table = table_json[:-5]
        children.append(['tables/' + product_directory_rel_path + '/' + table, table])
    return children


if __name__ == '__main__':
    generate_documentation_snds()
