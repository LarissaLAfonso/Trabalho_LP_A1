"""
Contains functions that create and save plots in png format.
"""

import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize
import numpy as np
import pandas as pd
import createobjects as co
import textwrap

def create_graph_non_attendance(df:pd.DataFrame) -> plt:
    """
    Creates a horizontal bar graph with the non attendance rate of each course

    Parameters
    ---------- 
    df: pd.DataFrame

    Returns
    -------
    None
    """

    # Define data for each axis of the bar graph
    courses = df['Área de Avaliação'].tolist()
    non_attendance = df['Taxa de Desistência Média'].tolist()

    # Define upper and lower bounds to the colorbar
    norm = Normalize(vmin=df["Taxa de Desistência Média"].min(), vmax=df["Taxa de Desistência Média"].max())

    # Choose a colormap (sequential)
    cmap = get_cmap('coolwarm')

    # Create a horizontal bar plot with a color gradient
    fig, ax = plt.subplots(figsize=(20, 15), constrained_layout=False)

    # Separate the labels into multiple lines
    wrapped_labels = [textwrap.wrap(label, width=16) for label in courses]
    wrapped_labels = ["\n".join(wrapped_label) for wrapped_label in wrapped_labels]

    # Define the positions of the bars
    positions = np.arange(len(wrapped_labels)) 

    # Create the bar graph
    bars = ax.barh(positions, width=non_attendance, height=0.8, color=cmap(norm(non_attendance)))

    # Labeling and customization
    plt.xlabel("Cursos", fontsize=10)
    plt.ylabel("Taxa de desistência média")
    plt.yticks(positions, wrapped_labels, fontsize=6)
    plt.title("Taxa de Desistência Média por Curso")

    return plt


def create_graph_average_scores_by_region(dataframe: pd.DataFrame) -> plt:

    colors = ["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe", "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7"]
    
    dataframe.plot.bar(color=colors)

    legend_labels = ["Organização Didático-Pedagógica", "Infraestrutura e Instalações Físicas", "Oportunidade de Ampliação da Formação", "Regime de Trabalho"]

    plt.legend(labels = legend_labels, title = "Categoria", title_fontsize = 14, fontsize = 12)

    plt.tick_params(rotation = 0, labelsize = 16)
    plt.xlabel("Regiões", fontsize=18)
    plt.ylabel("Nota média padronizada", fontsize = 18)
    plt.ylim(top = 5.9)
    plt.title("Notas médias por Região", fontsize=24)

    plt.gcf().set_size_inches(20, 14)

    return plt
