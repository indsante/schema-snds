import json
import logging
import os

from table_schema_to_markdown import convert_source

from src.constants import TABLESCHEMA_DIR, TABLES_SIDEBAR_JS_PATH


def generate_documentation_snds():
    tableschema_to_markdown()
    generate_table_sidebar()


def tableschema_to_markdown() -> None:
    logging.getLogger('table_schema_to_markdown').setLevel(logging.WARNING)
    logging.info("Convert schemas to Markdown")
    for root, dirs, files in os.walk(TABLESCHEMA_DIR):
        for file in files:
            schema_path = os.path.join(root, file)
            markdown_path = schema_path.replace('tableschema', 'byproducts/documentation_snds/markdown').replace('.json', '.md')
            os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
            with open(markdown_path, 'w', encoding='utf8') as out:
                convert_source(schema_path, out)


def generate_table_sidebar() -> None:
    logging.info("Generate 'table_sidebar.js' for VuePress documentation")
    sidebar = ['']
    for product_folder in os.listdir(TABLESCHEMA_DIR):
        table_schemas = os.listdir(os.path.join(TABLESCHEMA_DIR, product_folder))
        sidebar.append({
            'title': product_folder,
            'children': [product_folder + '/' + table[:-5] for table in table_schemas]
        })

    with open(TABLES_SIDEBAR_JS_PATH, 'w', encoding='utf8') as f:
        f.write('module.exports =')
        json.dump(sidebar, f, ensure_ascii=False, indent=4)
        f.write(';')
