import logging
import os
from typing import Union, List

from tableschema import Schema

from src.constants import DCIRS_SCHMEMA_DIR, DCIR_SCHMEMA_DIR, DCIR_DCIRS_SCHEMA_DIR, BENEFICIARY_SCHEMA_DIR, \
    DECES_SCHEMA_DIR, CARTO_PATHO_SCHEMA_DIR, PMSI_MCO_SCHEMA_DIR, PMSI_HAD_SCHEMA_DIR, PMSI_RIMP_SCHEMA_DIR, \
    PMSI_SSR_SCHEMA_DIR

DCIRS_CENTRAL_TABLE = 'NS_PRS_F'
DCIRS_JOIN_KEY = ['CLE_DCI_JNT']

DCIR_CENTRAL_TABLE = 'ER_PRS_F'
DCIR_JOIN_KEY = [
    'DCT_ORD_NUM',
    'FLX_DIS_DTD',
    'FLX_EMT_NUM',
    'FLX_EMT_ORD',
    'FLX_EMT_TYP',
    'FLX_TRT_DTD',
    'ORG_CLE_NUM',
    'PRS_ORD_NUM',
    'REM_TYP_AFF',
]

BENEFICIARY_CENTRAL_TABLE_DCIR = 'IR_BEN_R'
BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY = [
    'BEN_NIR_PSA',
    'BEN_RNG_GEM',
]
BENEFICIARY_DCIR_EXCLUDED_TABLES = 'DA_PRA_R.json'
BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY_LOWERCASE = [x.lower() for x in BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY]

BENEFICIARY_CENTRAL_TABLE_DCIRS = 'IR_IBA_R'
BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY = ['BEN_IDT_ANO']
BENEFICIARY_DCIRS_EXCLUDED_TABLES = [
    'DA_PRA_R.json',
    'IR_IMB_R.json',
]

DECES_JOIN_KEY = ['BEN_IDT_ANO']

PS_JOIN_KEY = 'PFS_PFS_NUM'
PS_CHAMP_DCIR_DCIRS = [
    'PFS_EXE_NUM',
    'PFS_PRE_NUM',
    'PRS_MTT_NUM',
]

CARTO_PATHO_CENTRAL_TABLE = 'CT_IDE_AAAA_GN'
CARTO_PATHO_JOIN_KEY = "id_carto"

PMSI_MCO_CENTRAL_TABLE = 'T_MCOaa_nnC'
PMSI_MCO_JOIN_KEY = [
    'ETA_NUM',
    'RSA_NUM',
]

PMSI_HAD_CENTRAL_TABLE = 'T_HADaa_nnC'
PMSI_HAD_JOIN_KEY = [
    'ETA_NUM_EPMSI',
    'RHAD_NUM',
]

PMSI_RIMP_CENTRAL_TABLE = 'T_RIPaa_nnC'
PMSI_RIMP_JOIN_KEY = [
    'ETA_NUM_EPMSI',
    'RIP_NUM',
]

PMSI_SSR_CENTRAL_TABLE = 'T_SSRaa_nnC'
PMSI_SSR_JOIN_KEY = [
    'ETA_NUM',
    'RSA_NUM',
]

def add_primary_key(schema: Schema, primary_key: Union[str, List[str]]) -> None:
    schema.descriptor['primaryKey'] = primary_key
    schema.commit()


def add_foreign_key(schema: Schema, fields: Union[str, List[str]], referenced_table: str,
                    referenced_fields: Union[str, List[str]]) -> None:
    if 'foreignKeys' not in schema.descriptor:
        schema.descriptor['foreignKeys'] = list()

    foreign_key_descriptor = {
        'fields': fields,
        'reference': {
            'resource': referenced_table,
            'fields': referenced_fields
        }
    }
    schema.descriptor['foreignKeys'].append(foreign_key_descriptor)
    schema.commit(strict=True)


def add_dcirs_keys() -> None:
    """ Ajout des liens entre la table centrale prestation du DCIRS et ses tables associées

    1) Ajout des clefs primaires et étrangères liant les tables du DCIRS entre elles.
    2) Ajout du lien entre la table centrale du DCIRS (NS_PRS_F) et la table des professionnels de santé DA_PRA_R
    """
    logging.info("Ajout des liens entre la table centrale prestation du DCIRS et ses tables associées"
                 " dans le table schema")
    for tableschema_filename in os.listdir(DCIRS_SCHMEMA_DIR):
        path = os.path.join(DCIRS_SCHMEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == DCIRS_CENTRAL_TABLE + '.json':
            add_primary_key(schema, DCIRS_JOIN_KEY)
        else:
            add_foreign_key(schema, DCIRS_JOIN_KEY, DCIRS_CENTRAL_TABLE, DCIRS_JOIN_KEY)
        schema.save(path, ensure_ascii=False)
    path_dcirs = os.path.join(DCIRS_SCHMEMA_DIR, 'NS_PRS_F.json')
    schema_dcirs = Schema(path_dcirs)
    add_da_pra_r_foreign_keys(schema_dcirs, path_dcirs)


def add_dcir_keys() -> None:
    """ Ajout des liens entre la table centrale prestation du DCIR et ses tables associées

    1) Ajout des clefs primaires et étrangères liant les tables du DCIR entre elles.
    2) Ajout de la clef étrangère entre la table prestation du DCIR et la table centrale de la cartographie des
    pathologies
    3) Ajout du lien entre la table centrale du DCIR (ES_PRS_F) et la table des professionnels de santé DA_PRA_R
    """
    logging.info("Ajout des liens entre la table centrale prestation du DCIR et ses tables associées"
                 " dans le table schema")
    for tableschema_filename in os.listdir(DCIR_SCHMEMA_DIR):
        path = os.path.join(DCIR_SCHMEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == DCIR_CENTRAL_TABLE + '.json':
            add_primary_key(schema, DCIR_JOIN_KEY)
            add_foreign_key(schema, BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY, CARTO_PATHO_CENTRAL_TABLE,
                            BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY_LOWERCASE)
        else:
            add_foreign_key(schema, DCIR_JOIN_KEY, DCIR_CENTRAL_TABLE, DCIR_JOIN_KEY)
        schema.save(path, ensure_ascii=False)
    path_dcir = os.path.join(DCIR_SCHMEMA_DIR, 'ER_PRS_F.json')
    schema_dcir = Schema(path_dcir)
    add_da_pra_r_foreign_keys(schema_dcir, path_dcir)


def update_descriptor_field(schema: Schema, field_name: str, update_dict: dict) -> bool:
    fields = schema.descriptor['fields']
    for field in fields:
        if field['name'] == field_name:
            field.update(update_dict)
            schema.commit()
            return True
    return False


def add_beneficiary_central_table_DCIR_keys() -> None:
    """
    Ajout des liens entre la table réferentiel beneficiaire du DCIR (IR_BEN_R) et les tables associées beneficiaires

    Toutes les tables DCIR_DCIRS sont des tables associées aux bénéficiaires sauf la table DA_PRA_R qui concerne
    les Professionnels de Santé.
    1) Liens entre la table référentiel bénéficiaire et ses tables associées
    2) Liens entre la table centrale beneficiaire DCIR et les tables de décès
    """
    logging.info("Ajout des liens entre la table réferentiel beneficiaire du DCIR IR_BEN_R et "
                 "ses tables associés beneficiaires dans le table schema")
    path_beneficiary_dcir = os.path.join(BENEFICIARY_SCHEMA_DIR, BENEFICIARY_CENTRAL_TABLE_DCIR + '.json')
    schema_beneficiary_dcir = Schema(path_beneficiary_dcir)
    update_descriptor_field(schema_beneficiary_dcir, 'BEN_IDT_ANO', {"constraints": {"unique": True}})
    add_primary_key(schema_beneficiary_dcir, BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY)
    add_foreign_key(schema_beneficiary_dcir, BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY, BENEFICIARY_CENTRAL_TABLE_DCIRS,
                    BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY)
    schema_beneficiary_dcir.save(path_beneficiary_dcir, ensure_ascii=False)
    add_associated_beneficiary_tables_foreign_keys(BENEFICIARY_CENTRAL_TABLE_DCIR,
                                                   BENEFICIARY_DCIR_EXCLUDED_TABLES,
                                                   BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY
                                                   )
    add_deces_foreign_keys_with_beneficiary(BENEFICIARY_CENTRAL_TABLE_DCIR)


def add_beneficiary_central_table_DCIRS_keys() -> None:
    """
    Ajout des liens entre la table réferentiel beneficiaire du DCIRS (IR_IBA_R) et les tables associées beneficiaires

    Toutes les tables DCIR_DCIRS sont des tables associées aux bénéficiaires sauf la table DA_PRA_R qui concerne
    les Professionnels de Santé.
    La table IR_IMB_R (Référentiel médicalisé - historique des exonérations) ne peut pas être reliée au DCIRS car elle
    n'a pas la clé de jointure (BEN_IDT_ANO)
    """
    logging.info("Ajout des liens entre la table réferentiel beneficiaire du DCIRS IR_IBA_R et ses tables associés "
                 "beneficiaires dans le table schema")
    path_beneficiary_dcirs = os.path.join(BENEFICIARY_SCHEMA_DIR, BENEFICIARY_CENTRAL_TABLE_DCIRS + '.json')
    schema_beneficiary_dcirs = Schema(path_beneficiary_dcirs)
    add_primary_key(schema_beneficiary_dcirs, BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY)
    schema_beneficiary_dcirs.save(path_beneficiary_dcirs, ensure_ascii=False)
    add_associated_beneficiary_tables_foreign_keys(BENEFICIARY_CENTRAL_TABLE_DCIRS,
                                                   BENEFICIARY_DCIRS_EXCLUDED_TABLES,
                                                   BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY
                                                   )
    add_deces_foreign_keys_with_beneficiary(BENEFICIARY_CENTRAL_TABLE_DCIRS)


def add_associated_beneficiary_tables_foreign_keys(beneficiary_central_table: str,
                                                   dcirs_dcir_excluded_tables: Union[str, List[str]],
                                                   beneficiary_central_table_join_key: Union[str, List[str]]) -> None:
    """
    Ajout des clefs étrangères entre les tables associées bénéficaires et une des tables réferentiel beneficiaire

    Les tables référentiel bénéficiaires sont le DCIR (IR_BEN_R) ou DCIRS (IR_IBA_R).
    Utilisation de la clef de jointure propre à chacune des tables référentiels beneficiaires.
    Exclusion de tables à ne pas considérer dans le dossier DCIR/DCIRS pour des raisons expliquées le cas échéant
    """
    for tableschema_filename in os.listdir(DCIR_DCIRS_SCHEMA_DIR):
        path = os.path.join(DCIR_DCIRS_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename not in dcirs_dcir_excluded_tables:
            add_foreign_key(schema, beneficiary_central_table_join_key, beneficiary_central_table,
                            beneficiary_central_table_join_key)
        schema.save(path, ensure_ascii=False)


def add_deces_foreign_keys_with_beneficiary(beneficiary_central_table: str) -> None:
    """
    Ajout des liens entre une des tables beneficiaires et les tables dates et causes de décés.

    Une seule clef de jointure possible pour l'ensemble des tables bénéficiaires
    """
    for tableschema_filename in os.listdir(DECES_SCHEMA_DIR):
        path = os.path.join(DECES_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        add_foreign_key(schema, DECES_JOIN_KEY, beneficiary_central_table, DECES_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_DCIR_beneficiary_link() -> None:
    """
    Ajout des liens entre les tables bénéficiaires et les tables de prestations

    """
    logging.info("Ajout des liens entre la table bénéficiaire du DCIR et les tables de prestations")
    path = os.path.join(DCIR_SCHMEMA_DIR, DCIR_CENTRAL_TABLE + ".json")
    schema = Schema(path)
    add_foreign_key(schema, BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY, BENEFICIARY_CENTRAL_TABLE_DCIR,
                    BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY)
    schema.save(path, ensure_ascii=False)


def add_DCIRS_beneficiary_link() -> None:
    """
    Ajout des liens entre les tables bénéficiaires et les tables de prestations

    """
    logging.info("Ajout des liens entre la table bénéficiaire du DCIRS et les tables de prestations")
    path = os.path.join(DCIRS_SCHMEMA_DIR, DCIRS_CENTRAL_TABLE + ".json")
    schema = Schema(path)
    add_foreign_key(schema, BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY, BENEFICIARY_CENTRAL_TABLE_DCIRS,
                    BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY)
    schema.save(path, ensure_ascii=False)


def add_DA_PRA_R_keys() -> None:
    """
    Ajout des clefs primaires à la table des professionels de santé DA_PRA_R
    """
    logging.info("Ajout des clefs primaires à la table des professionels de santé DA_PRA_R")
    path = os.path.join(DCIR_DCIRS_SCHEMA_DIR, "DA_PRA_R.json")
    schema = Schema(path)
    add_primary_key(schema, PS_JOIN_KEY)
    schema.save(path, ensure_ascii=False)


def add_da_pra_r_foreign_keys(schema: Schema, path: Union[bytes, str]) -> None:
    """
    Ajout des clefs étrangères aux tables des prestations pointant vers la table des professionnels de santé DA_PRA_R

    Fonction appelée dans la génération des clefs du DCIR et du DCIRS. Pour les trois champs possibles (PFS_EXE_NUM,
    PFS_PRE_NUM, PRS_MTT_NUM) on crée une clef étrangère pointant la clef principale du DA_PRA_R : PFS_PFS_NUM
    """
    for ps_join_foreign_key in PS_CHAMP_DCIR_DCIRS:
        add_foreign_key(schema, ps_join_foreign_key, 'DA_PRA_R', PS_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_cartographie_pathologies_dcir_dircs_foreign_keys() -> None:
    """
    Ajout du lien entre les tables associées bénéficiaires et celles de la cartographie des pathologies

    On considère l'ensemble des tables du dossier DCIR_DCIRS sauf celles des professionnels de santé DA_PRA_R.
    On fait le choix de dire que ce sont les tables associées bénéficiaires qui sont référencés pour la table des
    individus de la cartographie des pathologies CT_IDE_AAAA_GN (et pas l'inverse) - ce choix est à arbitrer.
    """
    for tableschema_filename in os.listdir(DCIR_DCIRS_SCHEMA_DIR):
        path = os.path.join(DCIR_DCIRS_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename not in 'DA_PRA_R.json':
            add_foreign_key(schema, BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY, CARTO_PATHO_CENTRAL_TABLE,
                            BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY_LOWERCASE)
        schema.save(path, ensure_ascii=False)


def add_cartographie_pathologies_foreign_keys() -> None:
    """
    Ajout des clefs étrangères aux tables des prestations pointant vers la table des professionnels de santé DA_PRA_R

    Les champs sont en minuscules dans la table principale carto des pathologies.
    1) On lie la table principale de la cartographie des pathologies (CT_IDE_AAAA_GN) aux tables associés carto à l'aide
    de la clef unique id_carto
    2) Déclaration en clefs primaires [ben_nir_psa,ben_rng_gem] afin d'assurer la contrainte d'unicité lorsque les
    tables DCIR_DCIRS pointent vers la table centrale carto des pathologies.
    3) Lien avec la table centrales du DCIR benéficiaires (IR_BEN_R)
    4) On lie la table CT_IDE_AAAA_GN aux tables associées bénéficiaires
    """
    for tableschema_filename in os.listdir(CARTO_PATHO_SCHEMA_DIR):
        path = os.path.join(CARTO_PATHO_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == CARTO_PATHO_CENTRAL_TABLE + '.json':
            schema.update_field('id_carto', {"constraints": {"unique": True}})
            add_primary_key(schema, BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY_LOWERCASE)
            add_foreign_key(schema, BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY_LOWERCASE, BENEFICIARY_CENTRAL_TABLE_DCIR,
                            BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY)
        else:
            add_foreign_key(schema, CARTO_PATHO_JOIN_KEY, CARTO_PATHO_CENTRAL_TABLE, CARTO_PATHO_JOIN_KEY)
        schema.save(path, ensure_ascii=False)
    add_cartographie_pathologies_dcir_dircs_foreign_keys()


def add_pmsi_mco_keys() -> None:
    """ Ajout du PMSI MCO

    """
    logging.info("Ajout des liens entre les tables du PMSI MCO")
    for tableschema_filename in os.listdir(PMSI_MCO_SCHEMA_DIR):
        path = os.path.join(PMSI_MCO_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == PMSI_MCO_CENTRAL_TABLE + '.json':
            add_primary_key(schema, PMSI_MCO_JOIN_KEY)
        else:
            add_foreign_key(schema, PMSI_MCO_JOIN_KEY, PMSI_MCO_CENTRAL_TABLE, PMSI_MCO_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_pmsi_had_keys() -> None:
    """ Ajout du PMSI MCO

    """
    logging.info("Ajout des liens entre les tables du PMSI HAD")
    for tableschema_filename in os.listdir(PMSI_HAD_SCHEMA_DIR):
        path = os.path.join(PMSI_HAD_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == PMSI_HAD_CENTRAL_TABLE + '.json':
            add_primary_key(schema, PMSI_HAD_JOIN_KEY)
        else:
            add_foreign_key(schema, PMSI_HAD_JOIN_KEY, PMSI_HAD_CENTRAL_TABLE, PMSI_HAD_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_pmsi_rimp_keys() -> None:
    """ Ajout du PMSI MCO

    """
    logging.info("Ajout des liens entre les tables du PMSI RIM-P")
    for tableschema_filename in os.listdir(PMSI_RIMP_SCHEMA_DIR):
        path = os.path.join(PMSI_RIMP_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == PMSI_RIMP_CENTRAL_TABLE + '.json':
            add_primary_key(schema, PMSI_RIMP_JOIN_KEY)
        else:
            add_foreign_key(schema, PMSI_RIMP_JOIN_KEY, PMSI_RIMP_CENTRAL_TABLE, PMSI_RIMP_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_pmsi_ssr_keys() -> None:
    """ Ajout du PMSI MCO

    """
    logging.info("Ajout des liens entre les tables du PMSI RIM-P")
    for tableschema_filename in os.listdir(PMSI_SSR_SCHEMA_DIR):
        path = os.path.join(PMSI_SSR_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == PMSI_SSR_CENTRAL_TABLE + '.json':
            add_primary_key(schema, PMSI_SSR_JOIN_KEY)
        else:
            add_foreign_key(schema, PMSI_SSR_JOIN_KEY, PMSI_SSR_CENTRAL_TABLE, PMSI_SSR_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_pmsi_dcir_link() -> None:
    """ Ajout du lien entre la table beneficiaire DCIR et les tables beneficiaires des PMSI

    """
    for tableschema_filename in [PMSI_HAD_CENTRAL_TABLE,PMSI_MCO_CENTRAL_TABLE,PMSI_RIMP_CENTRAL_TABLE,
                                 PMSI_SSR_CENTRAL_TABLE]:
        path = os.path.join()