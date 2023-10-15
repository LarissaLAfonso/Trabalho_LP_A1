"""
This module contains a set of functions for cleaning and preprocessing the data used to create the visualizations.
"""

import pandas as pd
import geopandas as gpd
import doctest

def dataframe_cleaner(dataframe):
    """
    Clean and preprocess a DataFrame.

    Parameters:
    dataframe (pd.DataFrame): 
        The original DataFrame to be cleaned.

    Returns:
    pd.DataFrame: A cleaned DataFrame.
    """
    
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
    """
    Clean and preprocess a DataFrame, specifically the "Área de Avaliação" column.

    Parameters:
    dataframe (pd.DataFrame): 
        The original DataFrame with the 'Área de Avaliação' column to be cleaned.

    Returns:
    pd.DataFrame: 
        A cleaned DataFrame with the "Área de Avaliação" column modified.

    Examples:

    >>> data = pd.DataFrame({'Área de Avaliação': ['Science (Physics)', 'arts (music)']})
    >>> cleaned_data = area_de_avaliacao_cleaner(data)
    >>> 'Área de Avaliação' in cleaned_data.columns
    True
    >>> cleaned_data['Área de Avaliação'].tolist()
    ['Science ', 'Arts ']
    """

    df = dataframe.copy()

    # removes all text after the first bracket, 
    df["Área de Avaliação"] = df["Área de Avaliação"].str.split("(").str.get(0)

    # capitalizes the first letter of the text
    df["Área de Avaliação"] = df["Área de Avaliação"].str.title()

    return df

def nome_da_ies_formater(dataframe):
    """
    Clean and preprocess a DataFrame, specifically the "Nome da IES" column.

    Parameters:
    dataframe (pd.DataFrame): The original DataFrame to be cleaned.

    Returns:
    pd.DataFrame: A cleaned DataFrame with the "Nome da IES" column modified.

    Examples:
    >>> data = pd.DataFrame({'Nome da IES': ['university of abc', 'escola de matemática aplicada']})
    >>> cleaned_data = nome_da_ies_formater(data)
    >>> 'Nome da IES' in cleaned_data.columns
    True
    >>> cleaned_data['Nome da IES'].tolist()
    ['University Of Abc', 'Escola De Matemática Aplicada']
    """

    df = dataframe.copy()

    # capitalizes the first letter of the text
    df["Nome da IES"] = df["Nome da IES"].str.title()

    return df

def area_de_avaliacao_long(dataframe):
    """
    Modify the names of some courses to make them shorter in a DataFrame.

    Parameters:
    df (pd.DataFrame): 
        The DataFrame used for modification.

    Returns:
    pd.DataFrame:
        A DataFrame with the changed course names.
    
    Examples:
    >>> data = pd.DataFrame({'Área de Avaliação': ['Tecnologia Em Redes De Computadores', 'Tecnologia Em Análise E Desenvolvimento De Sistemas', 'Other']})
    >>> modified_data = area_de_avaliacao_long(data)
    >>> modified_data['Área de Avaliação'].tolist()
    ['Redes De Computadores', 'Desenvolvimento De Sistemas', 'Other']
    """
    
    name_mapper = {
        "Tecnologia Em Redes De Computadores": "Redes De Computadores",
        "Tecnologia Em Análise E Desenvolvimento De Sistemas": "Desenvolvimento De Sistemas",
        "Tecnologia Em Gestão Da Tecnologia Da Informação": "Gestão De T.I."
    }

    df = dataframe.copy()

    # Change names that are too long
    df["Área de Avaliação"] = df["Área de Avaliação"].apply(lambda x: name_mapper[x] if x in name_mapper else x)

    return df

def add_state_name_to_data(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Add state names to a GeoDataFrame containing Brazil map data.

    Parameters:
    gdf (gpd.GeoDataFrame): 
        The original GeoDataFrame with unmodified Brazil map data.

    Returns:
    gpd.GeoDataFrame: 
        A GeoDataFrame with improved data and a new "Sigla da UF" column.
    
    Examples:
    >>> gdf = gpd.GeoDataFrame({'codarea': [12, 27, 16], 'geometry': [None, None, None]})
    >>> gdf_with_state = add_state_name_to_data(gdf)
    >>> 'Sigla da UF ' in gdf_with_state.columns
    True
    >>> gdf_with_state['Sigla da UF '].tolist()
    ['AC', 'AL', 'AP']
    """
    
    # Rename the column from "codarea" to "Código da UF"
    gdf.rename(columns={"codarea": "Código da UF"}, inplace=True)

    gdf.rename(columns = {"codarea": "Código da UF"}, inplace = True)
    gdf = gdf.astype({"Código da UF": int}) #no inplace option here

    # Define a dictionary to map state codes to their respective abbreviations
    uf_codes = {
        12:"AC", 27:"AL", 16:"AP", 13:"AM", 29:"BA", 23:"CE", 53:"DF", 32:"ES",
        52:"GO", 21:"MA", 51:"MT", 50:"MS", 31:"MG", 15:"PA", 25:"PB", 41:"PR",
        26:"PE", 22:"PI", 24:"RN", 43:"RS", 33:"RJ", 11:"RO", 14:"RR", 42:"SC",
        35:"SP", 28:"SE", 17:"TO"
    }

    # Define a function to map state codes to abbreviations
    def map_code(element):
        return uf_codes[element]
    
    gdf["Sigla da UF "] = gdf["Código da UF"].apply(map_code)

    return gdf


if __name__ == "__main__":
    doctest.testmod()