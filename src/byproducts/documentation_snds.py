import json
import logging
import os

from table_schema_to_markdown import convert_source

from src.constants import TABLESCHEMA_DIR, MARKDOWN_DIR, TABLES_SIDEBAR_JS_PATH
from src.utils import get_all_schema_path


def generate_documentation_snds():
    tableschema_to_markdown()
    generate_table_sidebar()


def tableschema_to_markdown() -> None:
    logging.getLogger('table_schema_to_markdown').setLevel(logging.WARNING)
    logging.info("Convert schemas to Markdown")
    for schema_path in get_all_schema_path():
        markdown_path = schema_path.replace(TABLESCHEMA_DIR, MARKDOWN_DIR).replace('.json', '.md')
        os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
        with open(markdown_path, 'w', encoding='utf8') as out:
            convert_source(schema_path, out)


def generate_table_sidebar() -> None:
    logging.info("Generate 'table_sidebar.js' for VuePress documentation")
    sidebar = ['']
    product_folders = sorted(os.listdir(TABLESCHEMA_DIR))
    for product_folder in product_folders:
        table_schema_filenames = sorted(os.listdir(os.path.join(TABLESCHEMA_DIR, product_folder)))
        children = list()
        for table_json in table_schema_filenames:
            table = table_json[:-5]
            children.append([product_folder + '/' + table, table])
        sidebar.append({
            'title': product_folder,
            'children': children
        })

    with open(TABLES_SIDEBAR_JS_PATH, 'w', encoding='utf8') as f:
        f.write('module.exports =')
        json.dump(sidebar, f, ensure_ascii=False, indent=4)
        f.write(';')


if __name__ == '__main__':
    tableschema_to_markdown()
