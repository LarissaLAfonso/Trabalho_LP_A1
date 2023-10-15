"""
Contains functions that load the Excel file and create the pd.DataFrame objects used in the project.
"""

import pandas as pd
import geopandas as gpd
import openpyxl
import zipfile
import data_cleaner as dc

# openpyxl is used by pandas when calling the `read_excel` function. It was
# imported here so the script can ensure the user have it installed before
# trying to run anything.

def load_data_as_df(file_path:str) -> pd.DataFrame:
    """Loads the data from a .xlsx file and return a pandas dataframe.
    Parameters
    ----------
    file_path: str
        The path to where the file with data is located.

    Returns
    -------
    pd.DataFrame
        A pandas dataframe with the data contained in the excel file
    """
    try:
        if file_path.endswith(".xlsx"):
            dataframe = pd.read_excel(file_path)
        else:
            dataframe = pd.read_csv(file_path)
            
    except FileNotFoundError:
        print("The file path passed is invalid.")
        quit()
    except zipfile.BadZipfile:
        print("the file could not be read. It is probably corrupted. Consider replacing it.")
        quit()

    return dataframe

def load_data_as_geodf(file_path:str) -> gpd.GeoDataFrame:
    """Loads the map data from a .json file and return a geopandas geodataframe.
    Parameters
    ----------
    file_path: str
        The path to where the file with data is located.

    Returns
    -------
    gpd.GeoDataFrame
        A geopandas geodataframe with the map data for plotting.
    """
    try:
        geodataframe = gpd.read_file(file_path)
    except FileNotFoundError:
        print("The file path passed is invalid.")
        quit()

    return geodataframe

def create_non_attendance_df(df:pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dataframe with the non attendance mean of each course

    Parameters
    ----------__
    df: pd.DataFrame
        Dataframe used for manipulation.
        
    Returns
    -------
    pd.DataFrame
        A pandas dataframe with the data of the average non attendance rate for each course
    """
    # Create new dataframe with only the columns we need
    df_1 = df[['Área de Avaliação', ' Nº de Concluintes Inscritos', ' Nº de Concluintes Participantes']]

    # Drop missing values
    df_1["Área de Avaliação"].dropna(inplace=True)

    # Remove everything after '(', leaving only the course name
    # Capitalize the first letter of each word
    df_1 = dc.area_de_avaliacao_cleaner(df_1)

    # Create new column with the ration between the difference between enrolled and participants divided by enrolled
    df_1["Taxa de Desistência"] = (df_1[" Nº de Concluintes Inscritos"] - df_1[" Nº de Concluintes Participantes"])/df_1[" Nº de Concluintes Inscritos"]

    # Get the mean in "Taxa de Desistência" for each course
    grouped = df_1.groupby('Área de Avaliação')['Taxa de Desistência'].mean().reset_index()

    # Merge the two dataframes
    df_1 = df_1.merge(grouped, on='Área de Avaliação', suffixes=('', ' Média'))

    # Rename the columns
    df_1.rename(columns={'D_Mean': 'Mean'}, inplace=True)

    # Get final dataframe with the non attendance mean of each course
    df_desist = df_1.groupby('Área de Avaliação')['Taxa de Desistência Média'].first().reset_index()
    df_desist.sort_values(by=['Taxa de Desistência Média'], inplace=True, ascending=False)

    df_desist = dc.area_de_avaliacao_long(df_desist)
    
    return df_desist


def create_region_column_df(df, uf_column) -> pd.DataFrame:

    region_mapper = {
        'AC': 'Norte',
        'AL': 'Nordeste',
        'AP': 'Norte',
        'AM': 'Norte',
        'BA': 'Nordeste',
        'CE': 'Nordeste',
        'DF': 'Centro-Oeste',
        'ES': 'Sudeste',
        'GO': 'Centro-Oeste',
        'MA': 'Nordeste',
        'MT': 'Centro-Oeste',
        'MS': 'Centro-Oeste',
        'MG': 'Sudeste',
        'PA': 'Norte',
        'PB': 'Nordeste',
        'PR': 'Sul',
        'PE': 'Nordeste',
        'PI': 'Nordeste',
        'RJ': 'Sudeste',
        'RN': 'Nordeste',
        'RS': 'Sul',
        'RO': 'Norte',
        'RR': 'Norte',
        'SC': 'Sul',
        'SP': 'Sudeste',
        'SE': 'Nordeste',
        'TO': 'Norte'
    }

    try:
        region_series = df[uf_column].map(region_mapper)
        return region_series
    
    except KeyError:
        print("The column does not exist")
        

def create_average_nota_by_region(dataframe: pd.DataFrame) -> pd.DataFrame:

    df = dataframe.copy()
    
    df["Região"] = create_region_column_df(df, "Sigla da UF ")

    nota_columns = [" Nota Padronizada - Organização Didático-Pedagógica",
                " Nota Padronizada - Infraestrutura e Instalações Físicas",
                " Nota Padronizada - Oportunidade de Ampliação da Formação",
                " Nota Padronizada - Regime de Trabalho"]

    average_nota_df = df.groupby(["Região"])[nota_columns].mean()

    return average_nota_df

