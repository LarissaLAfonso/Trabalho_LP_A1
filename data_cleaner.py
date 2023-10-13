import pandas as pd

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
