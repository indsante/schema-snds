from collections import defaultdict
from os.path import join

# Product groups
PMSI = 'PMSI'

PRODUCT_TO_GROUP = defaultdict(str)
PRODUCT_TO_GROUP['PMSI MCO'] = PMSI
PRODUCT_TO_GROUP['PMSI HAD'] = PMSI
PRODUCT_TO_GROUP['PMSI RIM-P'] = PMSI
PRODUCT_TO_GROUP['PMSI SSR'] = PMSI

# Data directories
SOURCES_DICO_SNDS_DIR = 'data/sources'

TABLESCHEMA_DIR = 'data/tableschema'

DCIRS_SCHMEMA_DIR = join(TABLESCHEMA_DIR, 'DCIRS')
DCIR_SCHMEMA_DIR = join(TABLESCHEMA_DIR, 'DCIR')
DCIR_DCIRS_SCHEMA_DIR = join(TABLESCHEMA_DIR, 'DCIR_DCIRS')

BENEFICIARY_SCHEMA_DIR = join(TABLESCHEMA_DIR, 'BENEFICIAIRE')
DECES_SCHEMA_DIR = join(TABLESCHEMA_DIR, 'Causes de décès')
CARTO_PATHO_SCHEMA_DIR = join(TABLESCHEMA_DIR, 'CARTOGRAPHIE_PATHOLOGIES')

PMSI_SCHEMA_DIR = join(TABLESCHEMA_DIR, PMSI)
PMSI_MCO_SCHEMA_DIR = join(PMSI_SCHEMA_DIR, 'PMSI MCO')
PMSI_HAD_SCHEMA_DIR = join(PMSI_SCHEMA_DIR, 'PMSI HAD')
PMSI_RIMP_SCHEMA_DIR = join(PMSI_SCHEMA_DIR, 'PMSI RIM-P')
PMSI_SSR_SCHEMA_DIR = join(PMSI_SCHEMA_DIR, 'PMSI SSR')

BYPRODUCTS_DIR = 'data/byproducts'
DICO_SNDS_DIR = join(BYPRODUCTS_DIR, 'dico_snds')
MARKDOWN_DIR = join(BYPRODUCTS_DIR, 'documentation_snds/markdown')
TABLES_SIDEBAR_JS_PATH = join(BYPRODUCTS_DIR, 'documentation_snds/tables_sidebar.js')


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
