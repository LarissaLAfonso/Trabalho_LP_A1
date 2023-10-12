import pandas as pd
import openpyxl
import zipfile
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
        dataframe = pd.read_excel(file_path)
    except FileNotFoundError:
        print("The file path passed is invalid.")
        quit()
    except zipfile.BadZipfile:
        print("the file could not be read. It is probably corrupted. Consider replacing it.")
        quit()
    return dataframe

df = load_data_as_df(r'Trabalho_LP_A1/resultados_cpc_2021.xlsx')

def create_non_attendance_df(df):
    """
    Create a dataframe with the non attendance mean of each course

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe used for manipulation.
        
    Returns
    -------
    pd.DataFrame
        A pandas dataframe with the data of the average non attendance rate for each course
    """
    #Create new dataframe with only the columns we need
    df_1 = df[['Área de Avaliação', ' Nº de Concluintes Inscritos', ' Nº de Concluintes Participantes']]

    #Drop missing values
    df_1["Área de Avaliação"].dropna(inplace=True)

    #Remove everything after '(', leaving only the course name
    df_1['Área de Avaliação'] = df_1['Área de Avaliação'].apply(lambda x: x.split('(')[0].strip() if isinstance(x, str) else x)

    #Create new column with the ration between the difference between enrolled and participants divided by enrolled
    df_1["Taxa de Desistência"] = (df_1[" Nº de Concluintes Inscritos"] - df_1[" Nº de Concluintes Participantes"])/df_1[" Nº de Concluintes Inscritos"]

    #Get the mean in "Taxa de Desistência" for each course
    grouped = df_1.groupby('Área de Avaliação')['Taxa de Desistência'].mean().reset_index()

    #Merge the two dataframes
    df_1 = df_1.merge(grouped, on='Área de Avaliação', suffixes=('', ' Média'))

    #Rename the columns
    df_1.rename(columns={'D_Mean': 'Mean'}, inplace=True)

    #Get final dataframe with the non attendance mean of each course
    df_desist = df_1.groupby('Área de Avaliação')['Taxa de Desistência Média'].first().reset_index()

    return df_desist
