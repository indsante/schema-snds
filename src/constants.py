from collections import defaultdict
from os import getcwd
from os.path import join as pjoin

# Table schema extra keys
OBSERVATION = "observation"
CHAMP = "champ"
TYPE_CSV = 'type'
TYPE_ORACLE = 'type_oracle'

REGLE_GESTION = "regle_gestion"
NOMENCLATURE = 'nomenclature'

HISTORY = "history"
DATE_CREATED = 'dateCreated'
DATE_DELETED = 'dateDeleted'
DATE_MISSING = 'dateMissing'

TRUE_VALUES = "trueValues"
FALSE_VALUES = "falseValues"

# Product groups
PMSI = 'PMSI'

PRODUCT_TO_GROUP = defaultdict(str)
PRODUCT_TO_GROUP['PMSI MCO'] = PMSI
PRODUCT_TO_GROUP['PMSI HAD'] = PMSI
PRODUCT_TO_GROUP['PMSI RIM-P'] = PMSI
PRODUCT_TO_GROUP['PMSI SSR'] = PMSI

TESTS_DIR = 'tests'
ROOT_DIR = getcwd()

DATA = 'data'
BYPRODUCT_REPOSITORIES_DIR = pjoin(DATA, 'byproducts_repositories')

SCHEMAS_DIR = 'schemas'
NOMENCLATURES_DIR = 'nomenclatures'
TEMPLATES_DIR = 'templates'

BYPRODUCTS_DIR = pjoin(DATA, 'byproducts')
SCHEMAS_MD_DIR = pjoin(BYPRODUCTS_DIR, 'documentation-snds', 'schemas-md')
DICO_SNDS_DIR = pjoin(BYPRODUCTS_DIR, 'dico-snds')
SCHEMAS_DOCUMENTATION_SNDS_DIR = pjoin(BYPRODUCTS_DIR, 'documentation-snds', 'schemas')

NO_NOMENCLATURE = '-'
IGNORED_DATE_NOMENCLATURE = 'IR_DTE_V'

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
