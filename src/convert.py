import os
import logging

from table_schema_to_markdown import convert_source


def convert_schemas_to_markdown(tableschema_dir):
    logging.getLogger('table_schema_to_markdown').setLevel(logging.WARNING)
    logging.info("Convert schemas to Markdown")
    for root, dirs, files in os.walk(tableschema_dir):
        for file in files:
            schema_path = os.path.join(root, file)
            markdown_path = schema_path.replace('tableschema', 'markdown').replace('.json', '.md')
            os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
            with open(markdown_path, 'a', encoding='utf8') as out:
                convert_source(schema_path, out)
