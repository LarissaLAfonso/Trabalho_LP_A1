import createobjects as co
import data_cleaner as dc

path = "./dataframes/resultados_cpc_2021.xlsx"

messy_df = co.load_data_as_df(path)

df = dc.dataframe_cleaner(messy_df)

print(df)