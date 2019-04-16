import logging
import os
from typing import Union, List

from tableschema import Schema

from src.constants import DCIRS_SCHMEMA_DIR, DCIR_SCHMEMA_DIR, DCIR_DCIRS_SCHEMA_DIR, BENEFICIARY_SCHEMA_DIR, \
    DECES_SCHEMA_DIR, CARTO_PATHO_SCHEMA_DIR, PMSI_MCO_SCHEMA_DIR, PMSI_HAD_SCHEMA_DIR, PMSI_RIMP_SCHEMA_DIR, \
    PMSI_SSR_SCHEMA_DIR

BIDIRECTIONNELLE = 'Bidirectionnel'

NS_PRS_F = 'NS_PRS_F'
CLE_DCI_JNT = ['CLE_DCI_JNT']

ER_PRS_F = 'ER_PRS_F'
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

IR_BEN_R = 'IR_BEN_R'
DCIR_BENEFICIARY_JOIN_KEY = [
    'BEN_NIR_PSA',
    'BEN_RNG_GEM',
]
DCIR_BENEFICIARY_JOIN_KEY_lowercase = [x.lower() for x in DCIR_BENEFICIARY_JOIN_KEY]

DA_PRA_R_json = 'DA_PRA_R.json'

IR_IBA_R = 'IR_IBA_R'
BEN_IDT_ANO = ['BEN_IDT_ANO']

DECES_JOIN_KEY = ['BEN_IDT_ANO']

PFS_PFS_NUM = 'PFS_PFS_NUM'

CARTO_PATHO_CENTRAL_TABLE = 'CT_IDE_AAAA_GN'
CARTO_PATHO_JOIN_KEY = "id_carto"

PMSI_MCO_B_TABLE = 'T_MCOaa_nnB'
PMSI_MCO_C_TABLE = 'T_MCOaa_nnC'
PMSI_MCO_EXT_B_TABLE = 'T_MCOaa_nnFBSTC'
PMSI_MCO_EXT_C_TABLE = 'T_MCOaa_nnCSTC'

PMSI_MCO_JOIN_KEY = [
    'ETA_NUM',
    'RSA_NUM',
]
PMSI_MCO_EXT_JOIN_KEY = [
    'ETA_NUM',
    'SEQ_NUM'
]

PMSI_HAD_B_TABLE = 'T_HADaa_nnB'
PMSI_HAD_C_TABLE = 'T_HADaa_nnC'
PMSI_HAD_JOIN_KEY = [
    'ETA_NUM_EPMSI',
    'RHAD_NUM',
]

PMSI_RIMP_B_TABLE = 'T_RIPaa_nnFB'
PMSI_RIMP_C_TABLE = 'T_RIPaa_nnC'
PMSI_RIMP_JOIN_KEY = [
    'ETA_NUM_EPMSI',
    'RIP_NUM',
]

PMSI_SSR_B_TABLE = 'T_SSRaa_nnB'
PMSI_SSR_C_TABLE = 'T_SSRaa_nnC'
PMSI_SSR_JOIN_KEY = [
    'ETA_NUM',
    'RHA_NUM',
]

PMSI_SSR_EXT_B_TABLE = 'T_SSRaa_nnFBSTC'
PMSI_SSR_EXT_C_TABLE = 'T_SSRaa_nnCSTC'
PMSI_SSR_EXT_JOIN_KEY = [
    'ETA_NUM',
    'SEQ_NUM'
]

PMSI_ETAB_TABLES = [
    'T_MCOaa_nnE.json',
    'T_SSRaa_nnE.json',
    'T_RIPaa_nnE.json',
    'T_HADaa_nnE.json'
]

PMSI_TABLES_LINKED_TO_SNIIRAM = [
    [PMSI_MCO_C_TABLE + ".json", PMSI_MCO_SCHEMA_DIR],
    [PMSI_MCO_EXT_C_TABLE + ".json", PMSI_MCO_SCHEMA_DIR],
    [PMSI_RIMP_C_TABLE + ".json", PMSI_RIMP_SCHEMA_DIR],
    [PMSI_SSR_C_TABLE + ".json", PMSI_SSR_SCHEMA_DIR],
    [PMSI_SSR_EXT_C_TABLE + ".json", PMSI_SSR_SCHEMA_DIR],
    [PMSI_HAD_C_TABLE + ".json", PMSI_HAD_SCHEMA_DIR]
]


def add_primary_key(schema: Schema, primary_key: Union[str, List[str]]) -> None:
    schema.descriptor['primaryKey'] = primary_key
    schema.commit()


def add_foreign_key(schema: Schema, fields: Union[str, List[str]], referenced_table: str,
                    referenced_fields: Union[str, List[str]], description: str = None) -> None:
    if 'foreignKeys' not in schema.descriptor:
        schema.descriptor['foreignKeys'] = list()

    foreign_key_descriptor = {
        'fields': fields,
        'reference': {
            'resource': referenced_table,
            'fields': referenced_fields
        },
    }
    if description:
        foreign_key_descriptor['description'] = description
    schema.descriptor['foreignKeys'].append(foreign_key_descriptor)
    schema.commit(strict=True)


def add_dcirs_keys() -> None:
    """ Ajout des liens entre la table centrale prestation du DCIRS et ses tables associées

    1) Ajout des clefs primaires et étrangères liant les tables du DCIRS entre elles
    2) Lien entre la table référentiel beneficiaire IR_IBA_R et les tables affinées du DCIRS
    3) Ajout du lien entre la table centrale du DCIRS (NS_PRS_F) et la table des professionnels de santé DA_PRA_R
    """
    logging.info("Ajout des liens entre la table centrale prestation du DCIRS et ses tables associées"
                 " dans le table schema")
    for tableschema_filename in os.listdir(DCIRS_SCHMEMA_DIR):
        path = os.path.join(DCIRS_SCHMEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == NS_PRS_F + '.json':
            add_primary_key(schema, CLE_DCI_JNT)
        else:
            add_foreign_key(schema, CLE_DCI_JNT, NS_PRS_F, CLE_DCI_JNT)
            add_foreign_key(schema, BEN_IDT_ANO, IR_IBA_R, BEN_IDT_ANO)
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
        if tableschema_filename == ER_PRS_F + '.json':
            add_primary_key(schema, DCIR_JOIN_KEY)
            add_foreign_key(schema, DCIR_BENEFICIARY_JOIN_KEY, CARTO_PATHO_CENTRAL_TABLE,
                            DCIR_BENEFICIARY_JOIN_KEY_lowercase, BIDIRECTIONNELLE)
        else:
            add_foreign_key(schema, DCIR_JOIN_KEY, ER_PRS_F, DCIR_JOIN_KEY)
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
    1) Ajout du lien entre la table référentiel bénéficiaire du DCIR et celle du DCIRS
    3) Liens entre la table référentiel bénéficiaire et ses tables associées
    3) Liens entre la table centrale beneficiaire DCIR et les tables de décès
    """
    logging.info("Ajout des liens entre la table réferentiel beneficiaire du DCIR IR_BEN_R et "
                 "ses tables associés beneficiaires dans le table schema")
    path_beneficiary_dcir = os.path.join(BENEFICIARY_SCHEMA_DIR, IR_BEN_R + '.json')
    schema_beneficiary_dcir = Schema(path_beneficiary_dcir)
    update_descriptor_field(schema_beneficiary_dcir, 'BEN_IDT_ANO', {"constraints": {"unique": True}})
    add_primary_key(schema_beneficiary_dcir, DCIR_BENEFICIARY_JOIN_KEY)
    schema_beneficiary_dcir.save(path_beneficiary_dcir, ensure_ascii=False)
    add_associated_beneficiary_tables_foreign_keys(IR_BEN_R,
                                                   DA_PRA_R_json,
                                                   DCIR_BENEFICIARY_JOIN_KEY
                                                   )
    add_deces_foreign_keys_with_beneficiary(IR_BEN_R)


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
    path_beneficiary_dcirs = os.path.join(BENEFICIARY_SCHEMA_DIR, IR_IBA_R + '.json')
    schema_beneficiary_dcirs = Schema(path_beneficiary_dcirs)
    add_primary_key(schema_beneficiary_dcirs, BEN_IDT_ANO)
    add_foreign_key(schema_beneficiary_dcirs, BEN_IDT_ANO, IR_BEN_R, BEN_IDT_ANO, BIDIRECTIONNELLE)
    schema_beneficiary_dcirs.save(path_beneficiary_dcirs, ensure_ascii=False)
    add_associated_beneficiary_tables_foreign_keys(IR_IBA_R,
                                                   ['DA_PRA_R.json', 'IR_IMB_R.json'],
                                                   BEN_IDT_ANO
                                                   )
    add_deces_foreign_keys_with_beneficiary(IR_IBA_R)


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
    Ajout des liens entre la table bénéficiaire DCIR et les tables de prestations DCIR et DCIRS

    """
    logging.info("Ajout des liens entre la table bénéficiaire du DCIR et les tables de prestations")
    path_dcir = os.path.join(DCIR_SCHMEMA_DIR, ER_PRS_F + ".json")
    schema_dcir = Schema(path_dcir)
    add_foreign_key(schema_dcir, DCIR_BENEFICIARY_JOIN_KEY, IR_BEN_R,
                    DCIR_BENEFICIARY_JOIN_KEY)
    schema_dcir.save(path_dcir, ensure_ascii=False)
    path_dcirs = os.path.join(DCIRS_SCHMEMA_DIR, NS_PRS_F + ".json")
    schema_dcirs = Schema(path_dcirs)
    add_foreign_key(schema_dcirs, BEN_IDT_ANO, IR_BEN_R,
                    BEN_IDT_ANO)
    schema_dcirs.save(path_dcirs, ensure_ascii=False)


def add_DCIRS_beneficiary_link() -> None:
    """
    Ajout des liens entre les tables bénéficiaires et les tables de prestations

    """
    logging.info("Ajout des liens entre la table bénéficiaire du DCIRS et les tables de prestations")
    path = os.path.join(DCIRS_SCHMEMA_DIR, NS_PRS_F + ".json")
    schema = Schema(path)
    add_foreign_key(schema, BEN_IDT_ANO, IR_IBA_R,
                    BEN_IDT_ANO)
    schema.save(path, ensure_ascii=False)


def add_DA_PRA_R_keys() -> None:
    """
    Ajout des clefs primaires à la table des professionels de santé DA_PRA_R
    """
    logging.info("Ajout des clefs primaires à la table des professionels de santé DA_PRA_R")
    path = os.path.join(DCIR_DCIRS_SCHEMA_DIR, "DA_PRA_R.json")
    schema = Schema(path)
    add_primary_key(schema, PFS_PFS_NUM)
    schema.save(path, ensure_ascii=False)


def add_da_pra_r_foreign_keys(schema: Schema, path: Union[bytes, str]) -> None:
    """
    Ajout des clefs étrangères aux tables des prestations pointant vers la table des professionnels de santé DA_PRA_R

    Fonction appelée dans la génération des clefs du DCIR et du DCIRS. Pour les trois champs possibles (PFS_EXE_NUM,
    PFS_PRE_NUM, PRS_MTT_NUM) on crée une clef étrangère pointant la clef principale du DA_PRA_R : PFS_PFS_NUM
    """
    for ps_join_foreign_key in ['PFS_EXE_NUM', 'PFS_PRE_NUM', 'PRS_MTT_NUM']:
        add_foreign_key(schema, ps_join_foreign_key, 'DA_PRA_R', PFS_PFS_NUM)
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
            add_primary_key(schema, DCIR_BENEFICIARY_JOIN_KEY_lowercase)
            add_foreign_key(schema, DCIR_BENEFICIARY_JOIN_KEY_lowercase, IR_BEN_R,
                            DCIR_BENEFICIARY_JOIN_KEY)
        else:
            add_foreign_key(schema, CARTO_PATHO_JOIN_KEY, CARTO_PATHO_CENTRAL_TABLE, CARTO_PATHO_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_pmsi_mco_keys() -> None:
    """ Generation des liens entre la table de chainage principale C du PMSI MCO.

    On dissocie les tables se terminant en STC qui correspondent aux actes et consultations externes.
    On dissocie la table E qui correspond à la table établissement et qui est indépendante du séjour.
    """
    logging.info("Ajout des liens entre les tables du PMSI MCO")
    for tableschema_filename in os.listdir(PMSI_MCO_SCHEMA_DIR):
        path = os.path.join(PMSI_MCO_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename[:-5] == PMSI_MCO_B_TABLE:
            add_primary_key(schema, PMSI_MCO_JOIN_KEY)
        elif tableschema_filename[:-5] == PMSI_MCO_C_TABLE:
            add_primary_key(schema, PMSI_MCO_JOIN_KEY)
            add_foreign_key(schema, PMSI_MCO_JOIN_KEY, PMSI_MCO_B_TABLE, PMSI_MCO_JOIN_KEY, BIDIRECTIONNELLE)
        elif tableschema_filename not in ['T_MCOaa_nnCSTC.json', 'T_MCOaa_nnE.json', 'T_MCOaa_nnFASTC.json',
                                          'T_MCOaa_nnFBSTC.json', 'T_MCOaa_nnFCSTC.json', 'T_MCOaa_nnFHSTC.json',
                                          'T_MCOaa_nnFLSTC.json', 'T_MCOaa_nnFMSTC.json', 'T_MCOaa_nnFPSTC.json',
                                          'T_MCOaa_nnVALOACE.json']:
            add_foreign_key(schema, PMSI_MCO_JOIN_KEY, PMSI_MCO_B_TABLE, PMSI_MCO_JOIN_KEY)
        schema.save(path, ensure_ascii=False)
    add_pmsi_mco_actes_ext_keys()
    add_pmsi_mco_etablissement_keys()


def add_pmsi_mco_etablissement_keys() -> None:
    """ Gestion de la table etablissement E du PMSI MCO

    Lien avec les deux tables de chainage C et CSTC
    """
    path_etab = os.path.join(PMSI_MCO_SCHEMA_DIR, 'T_MCOaa_nnE.json')
    schema_etab = Schema(path_etab)
    add_primary_key(schema_etab, 'ETA_NUM')
    schema_etab.save(path_etab, ensure_ascii=False)
    for tableschema_filename in [PMSI_MCO_B_TABLE + '.json', PMSI_MCO_EXT_B_TABLE + '.json']:
        path = os.path.join(PMSI_MCO_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        add_foreign_key(schema, 'ETA_NUM', 'T_MCOaa_nnE', 'ETA_NUM')
        schema.save(path, ensure_ascii=False)


def add_pmsi_mco_actes_ext_keys() -> None:
    """ Ajout des liens pour les tables d'actes et consultations externes du PMSI MCO
    """
    for tableschema_filename in ['T_MCOaa_nnVALOACE.json', 'T_MCOaa_nnCSTC.json', 'T_MCOaa_nnFASTC.json',
                                 'T_MCOaa_nnFBSTC.json', 'T_MCOaa_nnFCSTC.json', 'T_MCOaa_nnFHSTC.json',
                                 'T_MCOaa_nnFLSTC.json', 'T_MCOaa_nnFMSTC.json', 'T_MCOaa_nnFPSTC.json']:
        path = os.path.join(PMSI_MCO_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename[:-5] == PMSI_MCO_EXT_B_TABLE:
            add_primary_key(schema, PMSI_MCO_EXT_JOIN_KEY)
        elif tableschema_filename[:-5] == PMSI_MCO_EXT_C_TABLE:
            add_primary_key(schema, PMSI_MCO_EXT_JOIN_KEY)
            add_foreign_key(schema, PMSI_MCO_EXT_JOIN_KEY, PMSI_MCO_EXT_B_TABLE, PMSI_MCO_EXT_JOIN_KEY,
                            BIDIRECTIONNELLE)
        else:
            add_foreign_key(schema, PMSI_MCO_EXT_JOIN_KEY, PMSI_MCO_EXT_B_TABLE, PMSI_MCO_EXT_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_pmsi_had_keys() -> None:
    """ Generation des liens entre la table de chainage principale C du PMSI HAD.

    Le champ ETA_NUM_EPMSI est nommé ETA_NUM_ePMSI dans la table centrale de chainage du HAD.
    Modification du fichier SNDS_vars réalisée directement.
    On ne prends pas en compte les deux tables correspondant à des tables établissements indépendantes du séjour :
    E et EHPA.
    """
    logging.info("Ajout des liens entre les tables du PMSI HAD")
    for tableschema_filename in os.listdir(PMSI_HAD_SCHEMA_DIR):
        path = os.path.join(PMSI_HAD_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename[:-5] == PMSI_HAD_B_TABLE:
            add_primary_key(schema, PMSI_HAD_JOIN_KEY)
        elif tableschema_filename[:-5] == PMSI_HAD_C_TABLE:
            add_primary_key(schema, PMSI_HAD_JOIN_KEY)
            add_foreign_key(schema, PMSI_HAD_JOIN_KEY, PMSI_HAD_B_TABLE, PMSI_HAD_JOIN_KEY, BIDIRECTIONNELLE)
        elif tableschema_filename not in ['T_HADaa_nnE.json', 'T_HADaa_nnEHPA.json']:
            add_foreign_key(schema, PMSI_HAD_JOIN_KEY, PMSI_HAD_B_TABLE, PMSI_HAD_JOIN_KEY)
        schema.save(path, ensure_ascii=False)
    add_pmsi_had_etablissement_keys()


def add_pmsi_had_etablissement_keys() -> None:
    """ Gestion des tables etablissement E et EHPA du PMSI HAD

    Lien avec la table de chainage C et les deux tables établissements avec leurs clefs qui leurs sont propres pour
    se référer à l'ID Finess de l'établissement.
    """
    for tableschema_keys_etab_had in [['T_HADaa_nnE', 'ETA_NUM'],
                                      ['T_HADaa_nnEHPA', 'ETA_NUM_EPMSI']]:
        path_etab = os.path.join(PMSI_HAD_SCHEMA_DIR, tableschema_keys_etab_had[0] + '.json')
        schema_etab = Schema(path_etab)
        add_primary_key(schema_etab, tableschema_keys_etab_had[1])
        schema_etab.save(path_etab, ensure_ascii=False)
        path = os.path.join(PMSI_HAD_SCHEMA_DIR, PMSI_HAD_B_TABLE + '.json')
        schema = Schema(path)
        add_foreign_key(schema, 'ETA_NUM_EPMSI', tableschema_keys_etab_had[0], tableschema_keys_etab_had[1])
        schema.save(path, ensure_ascii=False)


def add_pmsi_rimp_keys() -> None:
    """ AGeneration des liens entre la table de chainage principale C du PMSI RIM-P.

    On ne prend pas en compte la table établissement ni la table R3AD (ambulatoire) qui est difficilement reliable à
    ce jour.
    """
    logging.info("Ajout des liens entre les tables du PMSI RIM-P")
    for tableschema_filename in os.listdir(PMSI_RIMP_SCHEMA_DIR):
        path = os.path.join(PMSI_RIMP_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename[:-5] == PMSI_RIMP_B_TABLE:
            add_primary_key(schema, PMSI_RIMP_JOIN_KEY)
        elif tableschema_filename[:-5] == PMSI_RIMP_C_TABLE:
            add_primary_key(schema, PMSI_RIMP_JOIN_KEY)
            add_foreign_key(schema, PMSI_RIMP_JOIN_KEY, PMSI_RIMP_B_TABLE, PMSI_RIMP_JOIN_KEY, BIDIRECTIONNELLE)
        elif tableschema_filename not in ['T_RIPaa_nnE.json', 'T_RIPaa_nnR3A.json', 'T_RIPaa_nnR3AD.json']:
            add_foreign_key(schema, PMSI_RIMP_JOIN_KEY, PMSI_RIMP_B_TABLE, PMSI_RIMP_JOIN_KEY)
        schema.save(path, ensure_ascii=False)
    add_pmsi_rimp_etablissement_keys()


def add_pmsi_rimp_etablissement_keys() -> None:
    """ Gestion de la table etablissement E du PMSI RIMP

    Lien de la table établissement avec la table de chainage C du PMSI RIM-P
    """
    path_etab = os.path.join(PMSI_RIMP_SCHEMA_DIR, 'T_RIPaa_nnE.json')
    schema_etab = Schema(path_etab)
    add_primary_key(schema_etab, 'ETA_NUM')
    schema_etab.save(path_etab, ensure_ascii=False)
    path = os.path.join(PMSI_RIMP_SCHEMA_DIR, PMSI_RIMP_B_TABLE + '.json')
    schema = Schema(path)
    add_foreign_key(schema, 'ETA_NUM_EPMSI', 'T_RIPaa_nnE', 'ETA_NUM')
    schema.save(path, ensure_ascii=False)


def add_pmsi_ssr_actes_ext_keys() -> None:
    """ Ajout des liens pour les tables d'actes et consultations externes du PMSI SSR

    La table de chainage centrale avec le DCIR est la CSTC, les autres sont reliés à celle-ci.
    """
    for tableschema_filename in ['T_SSRaa_nnCSTC.json', 'T_SSRaa_nnFASTC.json',
                                 'T_SSRaa_nnFBSTC.json', 'T_SSRaa_nnFCSTC.json', 'T_SSRaa_nnFLSTC.json',
                                 'T_SSRaa_nnFMSTC.json']:
        path = os.path.join(PMSI_SSR_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename[:-5] == PMSI_SSR_EXT_B_TABLE:
            add_primary_key(schema, PMSI_SSR_EXT_JOIN_KEY)
        elif tableschema_filename[:-5] == PMSI_SSR_EXT_C_TABLE:
            add_primary_key(schema, PMSI_SSR_EXT_JOIN_KEY)
            add_foreign_key(schema, PMSI_SSR_EXT_JOIN_KEY, PMSI_SSR_EXT_B_TABLE, PMSI_SSR_EXT_JOIN_KEY,
                            BIDIRECTIONNELLE)
        else:
            add_foreign_key(schema, PMSI_SSR_EXT_JOIN_KEY, PMSI_SSR_EXT_B_TABLE, PMSI_SSR_EXT_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_pmsi_ssr_keys() -> None:
    """ Ajout du PMSI SSR

    Generation des liens entre la table de chainage principale C du PMSI SSR.
    On dissocie les tables se terminant en STC qui correspondent aux actes et consultations externes.
    On dissocie la table E qui correspond à la table établissement et qui est indépendante du séjour.
    """
    logging.info("Ajout des liens entre les tables du PMSI SSR")
    for tableschema_filename in os.listdir(PMSI_SSR_SCHEMA_DIR):
        path = os.path.join(PMSI_SSR_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename[:-5] == PMSI_SSR_B_TABLE:
            add_primary_key(schema, PMSI_SSR_JOIN_KEY)
        elif tableschema_filename[:-5] == PMSI_SSR_C_TABLE:
            add_primary_key(schema, PMSI_SSR_JOIN_KEY)
            add_foreign_key(schema, PMSI_SSR_JOIN_KEY, PMSI_SSR_B_TABLE, PMSI_SSR_JOIN_KEY, BIDIRECTIONNELLE)
        elif tableschema_filename not in ['T_SSRaa_nnCSTC.json', 'T_SSRaa_nnB.json',
                                          'T_SSRaa_nnE.json', 'T_SSRaa_nnFASTC.json', 'T_SSRaa_nnFBSTC.json',
                                          'T_SSRaa_nnFCSTC.json', 'T_SSRaa_nnFLSTC.json', 'T_SSRaa_nnFMSTC.json']:
            add_foreign_key(schema, PMSI_SSR_JOIN_KEY, PMSI_SSR_B_TABLE, PMSI_SSR_JOIN_KEY)
        schema.save(path, ensure_ascii=False)
    add_pmsi_ssr_actes_ext_keys()
    add_pmsi_ssr_etablissement_keys()


def add_pmsi_ssr_etablissement_keys() -> None:
    """ Gestion de la table etablissement E du PMSI MCO

    Lien avec les deux tables de chainage C et CSTC
    """
    path_etab = os.path.join(PMSI_SSR_SCHEMA_DIR, 'T_SSRaa_nnE.json')
    schema_etab = Schema(path_etab)
    add_primary_key(schema_etab, 'ETA_NUM')
    schema_etab.save(path_etab, ensure_ascii=False)
    for tableschema_filename in [PMSI_SSR_B_TABLE + '.json', PMSI_SSR_EXT_B_TABLE + '.json']:
        path = os.path.join(PMSI_SSR_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        add_foreign_key(schema, 'ETA_NUM', 'T_SSRaa_nnE', 'ETA_NUM')
        schema.save(path, ensure_ascii=False)


def add_unicity_constraint_DCIR() -> None:
    """ Ajout de la contrainte d'unicité au champ BEN_NIR_PSA dans IR_BEN_R

    Nécessité d'ajouter cette unicité pour pouvoir faire le chainage entre le DCIR et les tables du PMSI.
    Utilisation de cette fonction dans la fonction add_pmsi_dcir_link suivante.
    Cette contrainte d'unicité est obligatoire pour le lien avec postgres ne se vérifie pas dans les faits.
    Le PMSI n'a pas le rang gemelaire et ne permet donc pas de différencier 2 personnes jumelles de même sexe.
    """
    path = os.path.join(BENEFICIARY_SCHEMA_DIR, IR_BEN_R + ".json")
    schema = Schema(path)
    update_descriptor_field(schema, 'BEN_NIR_PSA',
                            {"constraints": {
                                "unique": True,
                                "description": "Unicité fausse sans le rang gémellaire. "
                                               "Contrainte nécessaire pour les clés étrangère du PMSI, "
                                               "qui n'a pas le rang gémellaire"
                            }})
    schema.save(path, ensure_ascii=False)


def add_pmsi_dcir_link() -> None:
    """ Ajout du lien entre les tables beneficiaire et prestation du DCIR et les tables beneficiaires des PMSI

    Contrainte d'unicité pour BEN_NIR_PSA à rajouter alors que c'est faux ?
    Generation du lien entre les différentes tables centrales de chainage beneficiaires PMSI avec la table beneficiaire
    du DCIR et la table prestation du DCIR
    """
    logging.info("Ajout des liens entre les tables du PMSI et les tables du DCIR")
    add_unicity_constraint_DCIR()
    for tableschema_filename_dir_list in PMSI_TABLES_LINKED_TO_SNIIRAM:
        path = os.path.join(tableschema_filename_dir_list[1], tableschema_filename_dir_list[0])
        schema = Schema(path)
        add_foreign_key(schema, 'NIR_ANO_17', IR_BEN_R, 'BEN_NIR_PSA')
        schema.save(path, ensure_ascii=False)


def add_pmsi_keys_to_tableschema() -> None:
    """ Ajout des clefs associées aux PMSI
    """
    add_pmsi_mco_keys()
    add_pmsi_had_keys()
    add_pmsi_rimp_keys()
    add_pmsi_ssr_keys()
    add_pmsi_dcir_link()


def add_primary_and_foreign_keys_to_tableschema() -> None:
    """ Fonctions regroupant l'ajout de toutes les clefs primaires et étrangères du SNDS (SNIIRAM + PMSI)
    """
    logging.info("Ajout des clefs primaires et étrangères au tableschema")
    add_DA_PRA_R_keys()
    add_dcirs_keys()
    add_dcir_keys()
    add_beneficiary_central_table_DCIR_keys()
    add_beneficiary_central_table_DCIRS_keys()
    add_DCIR_beneficiary_link()
    add_DCIRS_beneficiary_link()
    add_cartographie_pathologies_foreign_keys()
    add_pmsi_keys_to_tableschema()
