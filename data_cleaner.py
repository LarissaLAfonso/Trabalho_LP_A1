import pandas as pd

def area_de_avaliacao_cleaner(dataframe):

    df = dataframe.copy()

    # removes all text after the first bracket, 
    df["Área de Avaliação"] = df["Área de Avaliação"].str.split("(").str.get(0)

    # capitalizes the first letter of the text
    df["Área de Avaliação"] = df["Área de Avaliação"].str.title()

    return df