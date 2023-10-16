"""
This module contains a set of functions for cleaning and preprocessing the data used to create the visualizations.
"""

import pandas as pd
import geopandas as gpd
import doctest


def dataframe_cleaner(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the 'resultados_cpc' DataFrame.

    This functions checks if the dataframe have all needed columns to the analysis and graph making process, it also removes all the useless rows.

    Parameters
    ----------
    input: dataframe (pandas.DataFrame)
        Index:
            RangeIndex
        Columns:
            Name: 'Área de Avaliação', dtype: object
            Name: 'Sigla da UF** ', dtype: object
            Name: ' Nº de Concluintes Inscritos', dtype: int64
            Name: ' Nº de Concluintes Participantes', dtype: int64
            Name: ' Nota Padronizada - FG', dtype: float64
            Name: ' Nota Padronizada - CE', dtype: float64
            Name: ' Nota Padronizada - Organização Didático-Pedagógica', dtype: float64
            Name: ' Nota Padronizada - Infraestrutura e Instalações Físicas', dtype: float64
            Name: ' Nota Padronizada - Oportunidade de Ampliação da Formação', dtype: float64
            Name: ' CPC (Faixa)', dtype: object

    Returns
    -------
    pd.DataFrame: A cleaned DataFrame.

    Examples
    --------
    >>> data = pd.DataFrame({'Ano': [2021, 2022, 2023], 'Value': [10, 20, 30], ' CPC (Faixa)': ['SC', 'A', 'B']})
    >>> cleaned_data = dataframe_cleaner(data)
    >>> cleaned_data.columns
    Index(['Value', ' CPC (Faixa)'], dtype='object')
    """

    # creates a copy of the original dataset
    df = dataframe.copy()

    # remove rows that represent courses with less than 3 students
    df = df[df[" CPC (Faixa)"] != "SC"]

    useful_columns = ["Área de Avaliação", "Sigla da UF** ", "Categoria Administrativa*", " Nº de Concluintes Inscritos", " Nº de Concluintes Participantes",
                      " Conceito Enade (Contínuo)", " Nota Padronizada - Organização Didático-Pedagógica", " Nota Padronizada - Infraestrutura e Instalações Físicas", " Nota Padronizada - Oportunidade de Ampliação da Formação", " Nota Padronizada - Regime de Trabalho"]

    try:
        useful_df = df[useful_columns]
    except KeyError:
        print(
            f"The given dataframe doesn't have all needeed columns, consider replacing it.")
        quit()
    else:
        # remove asterisks from the column names
        useful_df.columns = useful_df.columns.str.replace("*", "")

        # remove useless rows
        useful_df = useful_df.iloc[:7997]

        return useful_df


def area_de_avaliacao_cleaner(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess a DataFrame, specifically the "Área de Avaliação" column.

    Parameters
    ----------
    input: dataframe (pd.DataFrame): The original DataFrame with the 'Área de Avaliação' column to be cleaned.

        Index:
            RangeIndex
        Columns:
            Name: 'Área de Avaliação', dtype: object

    Returns
    -------
    pandas.DataFrame: 
        A cleaned DataFrame with the "Área de Avaliação" column modified.

    Examples
    --------
    >>> data = pd.DataFrame({'Área de Avaliação': ['Science (Physics)', 'arts (music)']})
    >>> cleaned_data = area_de_avaliacao_cleaner(data)
    >>> 'Área de Avaliação' in cleaned_data.columns
    True
    >>> cleaned_data['Área de Avaliação'].tolist()
    ['Science ', 'Arts ']
    """

    df = dataframe.copy()
    try:
        # removes all text after the first bracket,
        df["Área de Avaliação"] = df["Área de Avaliação"].str.split(
            "(").str.get(0)

        # capitalizes the first letter of the text
        df["Área de Avaliação"] = df["Área de Avaliação"].str.title()
    except KeyError:
        print(
            f"The given dataframe has no column 'Área de Avaliação', consider replacing it.")
        quit()

    else:
        return df


def nome_da_ies_formater(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess a DataFrame, specifically the "Nome da IES" column.

    Parameters
    ----------
    dataframe (pd.DataFrame): The original DataFrame to be cleaned.
        Index:
            RangeIndex
        Columns:
            Name: 'Área de Avaliação', dtype: object
    Returns
    -------
    pd.DataFrame: A cleaned DataFrame with the "Nome da IES" column modified.


    Examples
    --------
    >>> data = pd.DataFrame({'Nome da IES': ['university of abc', 'escola de matemática aplicada']})
    >>> cleaned_data = nome_da_ies_formater(data)
    >>> 'Nome da IES' in cleaned_data.columns
    True
    >>> cleaned_data['Nome da IES'].tolist()
    ['University Of Abc', 'Escola De Matemática Aplicada']
    """

    df = dataframe.copy()

    # capitalizes the first letter of the text
    try:
        df["Nome da IES"] = df["Nome da IES"].str.title()
    except KeyError:
        print(f"The given dataframe has no column 'Nome da IES', consider replacing it.")
        quit()
    else:
        return df


def area_de_avaliacao_long(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Modify the names of some courses to make them shorter in a DataFrame.

    Parameters
    ----------
    df (pd.DataFrame): 
        The DataFrame used for modification.

    Returns
    -------
    pd.DataFrame:
        A DataFrame with the changed course names.

    Examples
    --------
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
    try:
        df["Área de Avaliação"] = df["Área de Avaliação"].apply(
            lambda x: name_mapper[x] if x in name_mapper else x)
    except KeyError:
        print(
            f"The given dataframe has no column 'Área de Avaliação', consider replacing it.")

    return df


def add_state_name_to_data(geodataframe: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Add state names to a GeoDataFrame containing Brazil map data.

    Parameters
    ----------
    geodataframe (gpd.GeoDataFrame): 
        The original GeoDataFrame with unmodified Brazil map data.

    Returns
    -------
    gpd.GeoDataFrame: 
        A GeoDataFrame with improved data and a new "Sigla da UF" column.

    Examples
    --------
    >>> gdf = gpd.GeoDataFrame({'codarea': [12, 27, 16], 'geometry': [None, None, None]})
    >>> gdf_with_state = add_state_name_to_data(gdf)
    >>> 'Sigla da UF ' in gdf_with_state.columns
    True
    >>> gdf_with_state['Sigla da UF '].tolist()
    ['AC', 'AL', 'AP']
    """

    # Define a dictionary to map state codes to their respective abbreviations
    uf_codes = {
        12: "AC", 27: "AL", 16: "AP", 13: "AM", 29: "BA", 23: "CE", 53: "DF", 32: "ES",
        52: "GO", 21: "MA", 51: "MT", 50: "MS", 31: "MG", 15: "PA", 25: "PB", 41: "PR",
        26: "PE", 22: "PI", 24: "RN", 43: "RS", 33: "RJ", 11: "RO", 14: "RR", 42: "SC",
        35: "SP", 28: "SE", 17: "TO"
    }

    # Rename the column from "codarea" to "Código da UF"
    geodataframe.rename(columns={"codarea": "Código da UF"}, inplace=True)
    geodataframe = geodataframe.astype(
        {"Código da UF": int})  # no inplace option here

    # Define a function to map state codes to abbreviations
    def map_code(element):
        return uf_codes[element]

    try:
        geodataframe["Sigla da UF "] = geodataframe["Código da UF"].map(
            map_code)
    except KeyError:
        print("Invalid State Code, please revise the provided dataset")
        quit()
    else:
        return geodataframe


if __name__ == "__main__":
    doctest.testmod()
