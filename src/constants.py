from collections import defaultdict
from os import getcwd
from os.path import join

from src.settings import RUNNING_TEST

# Table schema extra keys
NOMENCLATURE = 'nomenclature'

HISTORY = "history"
DATE_CREATED = 'dateCreated'
DATE_DELETED = 'dateDeleted'
DATE_MISSING = 'dateMissing'

# Product groups
PMSI = 'PMSI'

PRODUCT_TO_GROUP = defaultdict(str)
PRODUCT_TO_GROUP['PMSI MCO'] = PMSI
PRODUCT_TO_GROUP['PMSI HAD'] = PMSI
PRODUCT_TO_GROUP['PMSI RIM-P'] = PMSI
PRODUCT_TO_GROUP['PMSI SSR'] = PMSI

TESTS_DIR = 'tests'

# Root directory is used to read schemas and generate them in TESTS_DIR while running tests
ROOT_DIR = getcwd()
if RUNNING_TEST:
    ROOT_DIR = TESTS_DIR

DATA = 'data'
BYPRODUCT_REPOSITORIES_DIR = join(ROOT_DIR, DATA, 'byproducts_repositories')

SCHEMAS = 'schemas'
ROOTED_SCHEMAS_DIR = join(ROOT_DIR, SCHEMAS)

BYPRODUCTS_DIR = join(DATA, 'byproducts')
ROOTED_BYPRODUCTS_DIR = join(ROOT_DIR, BYPRODUCTS_DIR)
DICO_SNDS_DIR = join(ROOTED_BYPRODUCTS_DIR, 'dico-snds')
MARKDOWN_DIR = join(ROOTED_BYPRODUCTS_DIR, 'documentation-snds', 'markdown')
ROOTED_TSFAKER_DIR = join(ROOTED_BYPRODUCTS_DIR, "tsfaker")
TSFAKER_DIR = join(DATA, 'byproducts', "tsfaker")

NOMENCLATURES_DIR = 'nomenclatures'
ROOTED_NOMENCLATURES_DIR = join(ROOT_DIR, NOMENCLATURES_DIR)
PRODUIT_NOMENCLATURES = join(DICO_SNDS_DIR, NOMENCLATURES_DIR)

NO_NOMENCLATURE = '-'

# https://frictionlessdata.io/specs/table-schema/#types-and-formats
STRING = 'string'
NUMBER = 'number'
INTEGER = 'integer'
BOOLEAN = 'boolean'
OBJECT = 'object'
ARRAY = 'array'
DATE = 'date'
TIME = 'time'
DATETIME = 'datetime'
YEAR = 'year'
YEARMONTH = 'yearmonth'
DURATION = 'duration'
GEOPOINT = 'geopoint'
GEOJSON = 'geojson'
ANY = 'any'
