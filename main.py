from src.reformat_snds_dico import get_dico_snds_variables, write_all_schema
from src.add_keys import add_dcirs_keys

dico_snds_path = '../dico-snds'
df = get_dico_snds_variables(dico_snds_path)
df.to_csv('data/variables.csv', index=False)
write_all_schema(df, 'data/tableschema')
add_dcirs_keys()
