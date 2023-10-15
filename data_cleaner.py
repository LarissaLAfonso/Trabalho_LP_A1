import pandas as pd
import geopandas as gpd

def dataframe_cleaner(dataframe):

    # creates a copy of the original dataset
    df = dataframe.copy()

    # remove useless columns
    df = df.drop(["Ano", "Observação", "Código da Área", "Código da IES*", "Código do Curso**", "Código do Município***", "Observação"], axis=1)

    # remove asterisks from the column names
    df.columns = df.columns.str.replace("*", "")

    # drop useless rows
    df = df.iloc[:7997]
    df = df[df[" CPC (Faixa)"] != "SC"]

    return df

def area_de_avaliacao_cleaner(dataframe):

    df = dataframe.copy()

    # removes all text after the first bracket, 
    df["Área de Avaliação"] = df["Área de Avaliação"].str.split("(").str.get(0)

    # capitalizes the first letter of the text
    df["Área de Avaliação"] = df["Área de Avaliação"].str.title()

    return df

def nome_da_ies_formater(dataframe):

    df = dataframe.copy()

    # capitalizes the first letter of the text
    df["Nome da IES"] = df["Nome da IES"].str.title()

    return df

def area_de_avaliacao_long(df):
    """
    Changes the names of some courses to make them shorter.

    Parameters 
    ----------
    df: pd.DataFrame
        Dataframe used for manipulation.

    Returns
    -------
    df: pd.DataFrame
        Dataframe with the changed names.
    
    """

    dictionary = {
        "Tecnologia Em Redes De Computadores": "Redes De Computadores",
        "Tecnologia Em Análise E Desenvolvimento De Sistemas": "Desenvolvimento De Sistemas",
        "Tecnologia Em Gestão Da Tecnologia Da Informação": "Gestão De T.I."
    }

    # Change names that are too long
    df["Área de Avaliação"] = df["Área de Avaliação"].apply(lambda x: dictionary[x] if x in dictionary else x)

    return df

def add_state_name_to_data(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf.rename(columns = {"codarea": "Código da UF"}, inplace = True)
    gdf = gdf.astype({"Código da UF": int}) #no inplace option here

    uf_codes = {
        12:"AC", 27:"AL", 16:"AP", 13:"AM", 29:"BA", 23:"CE", 53:"DF", 32:"ES",
        52:"GO", 21:"MA", 51:"MT", 50:"MS", 31:"MG", 15:"PA", 25:"PB", 41:"PR",
        26:"PE", 22:"PI", 24:"RN", 43:"RS", 33:"RJ", 11:"RO", 14:"RR", 42:"SC",
        35:"SP", 28:"SE", 17:"TO"
    }
    def map_code(element):
        return uf_codes[element]
    gdf["Sigla da UF"] = gdf["Código da UF"].apply(map_code)

    return gdf
