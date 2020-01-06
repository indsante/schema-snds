import logging
import os

import table_schema_to_markdown

from src.constants import WORKING_DIR, SCHEMAS_DIR, MARKDOWN_DIR
from src.utils import get_all_schema_path


def generate_documentation_snds(work_dir=WORKING_DIR) -> None:
    logging.info("Génération des fichiers markdown pour la documentation VuePress")
    logging.getLogger('table_schema_to_markdown').setLevel(logging.WARNING)
    for schema_path in get_all_schema_path(work_dir):
        markdown_path = schema_path.replace(SCHEMAS_DIR, MARKDOWN_DIR).replace('.json', '.md')
        os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
        with open(markdown_path, 'w', encoding='utf8') as out:
            table_schema_to_markdown.convert_source(schema_path, out)


if __name__ == '__main__':
    generate_documentation_snds()
