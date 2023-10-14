import pandas as pd


def dataframe_cleaner(dataframe):
    
    # drop useless columns
    df = dataframe.drop(["Ano", "Observação", "Código da Área", "Código da IES*", "Código do Curso**", "Código do Município***", "Observação"], axis=1)

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
    df["Nome da IES*"] = df["Nome da IES*"].str.title()

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
