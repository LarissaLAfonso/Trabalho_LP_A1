"""
Contains functions that load the Excel file and create the pd.DataFrame objects used in the project.
"""

import pandas as pd
import geopandas as gpd
import openpyxl
import zipfile
import data_cleaner as dc
import doctest

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

    Examples
    --------
    >>> sample_file_xlsx = "./data/dataframes/resultados_cpc_2021.xlsx"
    >>> df_xlsx = load_data_as_df(sample_file_xlsx)
    >>> isinstance(df_xlsx, pd.DataFrame)
    True
    >>> len(df_xlsx) > 0
    True

    >>> sample_file_csv = "./data/dataframes/resultados_cpc_2021.csv"
    >>> df_csv = load_data_as_df(sample_file_csv)
    >>> isinstance(df_csv, pd.DataFrame)
    True
    >>> len(df_csv) > 0
    True
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
    else:
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
        
    Examples
    --------
    >>> sample_geojson_file = "./data/map/brasil_estados.json"
    >>> geodf = load_data_as_geodf(sample_geojson_file)
    >>> isinstance(geodf, gpd.GeoDataFrame)
    True
    >>> len(geodf) > 0
    True
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
    Examples:
    >>> sample_data = pd.DataFrame({
    ...     'Área de Avaliação': ['Course A', 'Course B', 'Course A', 'Course C'],
    ...     ' Nº de Concluintes Inscritos': [100, 120, 90, 80],
    ...     ' Nº de Concluintes Participantes': [80, 110, 70, 70]
    ... })
    >>> df_desist = create_non_attendance_df(sample_data)
    >>> isinstance(df_desist, pd.DataFrame)
    True
    >>> 'Taxa de Desistência Média' in df_desist.columns
    True
    >>> len(df_desist) > 0
    True
    """

    # Create new dataframe with only the columns we need
    df_slice = df[['Área de Avaliação', ' Nº de Concluintes Inscritos', ' Nº de Concluintes Participantes']]
    try:
        df_1 = df[['Área de Avaliação', ' Nº de Concluintes Inscritos', ' Nº de Concluintes Participantes']]
    except KeyError:
        print("""That dataframe is not supposed to be as an argument for that function. 
              It should be obtained from the 'resultados_cpc_2021.xlsx' file.""")
        quit()

    # Drop missing values
    df_clean = df_slice.dropna(subset=['Área de Avaliação'])

    # Remove everything after '(', leaving only the course name
    # Capitalize the first letter of each word
    df_clean = dc.area_de_avaliacao_cleaner(df_clean)

    # Create new column with the ration between the difference between enrolled and participants divided by enrolled
    df_clean["Taxa de Desistência"] = (df_clean[" Nº de Concluintes Inscritos"] - df_clean[" Nº de Concluintes Participantes"])/df_clean[" Nº de Concluintes Inscritos"]

    # Get the mean in "Taxa de Desistência" for each course
    grouped_df = df_clean.groupby('Área de Avaliação')['Taxa de Desistência'].mean().reset_index()

    # Merge the two dataframes
    df_clean = df_clean.merge(grouped_df, on='Área de Avaliação', suffixes=('', ' Média'))

    # Rename the columns
    df_clean.rename(columns={'D_Mean': 'Mean'}, inplace=True)

    # Get final dataframe with the non attendance mean of each course
    df_desist = df_clean.groupby('Área de Avaliação')['Taxa de Desistência Média'].first().reset_index()
    df_desist.sort_values(by=['Taxa de Desistência Média'], inplace=True, ascending=False)

    df_desist = dc.area_de_avaliacao_long(df_desist)
    
    return df_desist


def create_region_column_df(df: pd.DataFrame, uf_column: str) -> pd.Series:
    """
    Creates a new series that maps state abbreviations to regions and adds it to the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame containing state data.
    uf_column: str
        The name of the column in the DataFrame that contains state abbreviations.

    Returns
    -------
    pd.Series
        A new Pandas Series with region names corresponding to each state abbreviation.

    Examples:
    >>> sample_data = pd.DataFrame({
    ...     'State Abbreviation': ['SP', 'RJ', 'MG'],
    ...     'Number': [45500, 17500, 21300]
    ... })
    >>> region_series = create_region_column_df(sample_data, 'State Abbreviation')
    >>> isinstance(region_series, pd.Series)
    True
    >>> len(region_series) == len(sample_data)
    True
    >>> 'Region' in sample_data.columns
    True
    >>> region_series.tolist()
    ['Sudeste', 'Sudeste', 'Sudeste']
    """

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
        # Map state abbreviations to regions
        region_series = df[uf_column].map(region_mapper)
        # Add the resulting series to the DataFrame
        df['Region'] = region_series
    except KeyError:
        print("The column does not exist")
    else:
        return region_series
        

def create_average_nota_by_region(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the average evaluation scores (nota) by region and returns a DataFrame.

    Parameters
    ----------
    dataframe: pd.DataFrame
        The DataFrame containing evaluation scores and state information.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the average evaluation scores by region.

    Examples:
    >>> sample_data = pd.DataFrame({
    ...     'Sigla da UF ': ['SP', 'RJ', 'MG', 'BA', 'AM', 'PA'],
    ...     ' Nota Padronizada - Organização Didático-Pedagógica': [8.5, 7.2, 6.8, 8.0, 7.5, 6.2],
    ...     ' Nota Padronizada - Infraestrutura e Instalações Físicas': [7.8, 7.5, 6.4, 8.2, 6.9, 6.1],
    ...     ' Nota Padronizada - Oportunidade de Ampliação da Formação': [7.2, 7.0, 6.3, 7.9, 6.5, 5.9],
    ...     ' Nota Padronizada - Regime de Trabalho': [8.1, 7.8, 7.0, 8.3, 7.1, 6.4]
    ... })
    >>> avg_nota_df = create_average_nota_by_region(sample_data)
    >>> isinstance(avg_nota_df, pd.DataFrame)
    True
    >>> len(avg_nota_df) > 0
    True
    >>> ' Nota Padronizada - Organização Didático-Pedagógica' in avg_nota_df.columns
    True
    """

    df = dataframe.copy()

    # Create a 'Região' column based on state abbreviations
    df["Região"] = create_region_column_df(df, "Sigla da UF ")

    try:
        nota_columns = [
            " Nota Padronizada - Organização Didático-Pedagógica",
            " Nota Padronizada - Infraestrutura e Instalações Físicas",
            " Nota Padronizada - Oportunidade de Ampliação da Formação",
            " Nota Padronizada - Regime de Trabalho"
        ]

        # Calculate the average nota by region
        average_nota_df = df.groupby(["Região"])[nota_columns].mean()
    except KeyError:
        print(f"The given dataframe doesn't have all needeed columns, consider replacing it.")

    else:
        return average_nota_df


def create_mean_of_general_grade(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame with the mean Enade grade for each state, only for public universities.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame containing Enade grade data and university information.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the mean Enade grade for each state.

    Examples:
    >>> sample_data = pd.DataFrame({
    ...     'Sigla da UF ': ['SP', 'RJ', 'MG', 'BA', 'AM', 'PA'],
    ...     'Categoria Administrativa': ['Pública Federal', 'Pública Estadual', 'Privada', 'Pública Municipal', 'Pública Federal', 'Pública Estadual'],
    ...     ' Conceito Enade (Contínuo)': [3.5, 4.0, 3.2, 4.5, 3.9, 4.2]
    ... })
    >>> mean_grade_df = create_mean_of_general_grade(sample_data)
    >>> isinstance(mean_grade_df, pd.DataFrame)
    True
    >>> mean_grade_df.to_dict()
    {'Sigla da UF ': {0: 'AM', 1: 'BA', 2: 'PA', 3: 'RJ', 4: 'SP'}, ' Conceito Enade (Contínuo)': {0: 3.9, 1: 4.5, 2: 4.2, 3: 4.0, 4: 3.5}}
    """

    # Filter for public universities only
    data_filter = ((df["Categoria Administrativa"] == "Pública Federal") |
                  (df["Categoria Administrativa"] == "Pública Estadual") |
                  (df["Categoria Administrativa"] == "Pública Municipal"))
    df = df[data_filter]

    # Group the DataFrame by state to calculate the mean Enade grade for each one
    df = df.groupby("Sigla da UF ")
    means = df[" Conceito Enade (Contínuo)"].mean()

    # Create a new DataFrame with the calculated means
    means_df = pd.DataFrame(means).reset_index()  # Reset index for merge

    return means_df

if __name__ == "__main__":
    doctest.testmod()