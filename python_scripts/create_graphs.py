"""
Contains functions that create and save plots in png format.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import Normalize
import numpy as np
import pandas as pd
import geopandas as gpd
import textwrap
import doctest


def create_graph_non_attendance(dataframe: pd.DataFrame) -> plt:
    """
    Creates a horizontal bar graph with the non-attendance rate of each course

    Parameters
    ----------
    dataframe: pd.DataFrame

    Returns
    -------
    plt
        The graph plot object

    Example
    -------
    >>> import pandas as pd
    >>> data = {'Área de Avaliação': ['Course A', 'Course B', 'Course C'],
    ...         'Taxa de Desistência Média': [5.2, 3.8, 7.1]}
    >>> df = pd.DataFrame(data)
    >>> plot = create_graph_non_attendance(df)
    >>> plot.__class__.__name__ == "module"
    True
    """

    # Define data for each axis of the bar graph
    courses = dataframe['Área de Avaliação'].tolist()
    non_attendance = dataframe['Taxa de Desistência Média'].tolist()

    # Define upper and lower bounds to the colorbar
    norm = Normalize(vmin=dataframe["Taxa de Desistência Média"].min(
    ), vmax=dataframe["Taxa de Desistência Média"].max())

    # Choose a colormap (sequential)
    cmap = mpl.colormaps["coolwarm"]

    # Create a horizontal bar plot with a color gradient
    fig, ax = plt.subplots(figsize=(20, 15), constrained_layout=False)

    # Separate the labels into multiple lines
    wrapped_labels = [textwrap.wrap(label, width=16) for label in courses]
    wrapped_labels = ["\n".join(wrapped_label)
                      for wrapped_label in wrapped_labels]

    # Define the positions of the bars
    positions = np.arange(len(wrapped_labels))

    # Create the bar graph
    bars = ax.barh(positions, width=non_attendance, height=0.8,
                   color=cmap(norm(non_attendance)))

    # Labeling and customization
    plt.ylabel("Cursos", fontsize=18)
    plt.xlabel("Taxa de desistência média", fontsize=18)
    plt.yticks(positions, wrapped_labels, fontsize=8)
    plt.title("Taxa de Desistência Média por Curso", fontsize=24)

    return plt


def create_graph_average_scores_by_region(dataframe: pd.DataFrame) -> plt:
    """
    Creates a grouped bar graph with the average scores by region

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe with the needed data, the data must be preprocessed

    Returns
    -------
    plt
        The graph plot object

    Example
    -------
    >>> import pandas as pd
    >>> data = {'Region': ['North', 'South', 'East'],
    ...         'Category': ['Category A', 'Category B', 'Category C'],
    ...         'Average Score': [4.2, 3.8, 4.1]}
    >>> df = pd.DataFrame(data)
    >>> plot = create_graph_average_scores_by_region(df)
    >>> plot.__class__.__name__ == "module"
    True
    """

    # creates the colors list
    colors = ["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe",
              "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7"]

    dataframe.plot.bar(color=colors)

    # format the legend labels
    legend_labels = ["Organização Didático-Pedagógica", "Infraestrutura e Instalações Físicas",
                     "Oportunidade de Ampliação da Formação", "Regime de Trabalho"]
    plt.legend(labels=legend_labels, title="Categoria",
               title_fontsize=14, fontsize=12)

    # format the texts of the plot
    plt.xlabel("Regiões", fontsize=18)
    plt.ylabel("Nota média padronizada", fontsize=18)
    plt.title("Notas médias por Região", fontsize=24)

    # adjust the graph axis
    plt.ylim(top=5.9)
    plt.tick_params(rotation=0, labelsize=16)

    # adjust the size of the figure
    plt.gcf().set_size_inches(20, 14)

    return plt


def create_map_plot_average_score_by_state(geodataframe: gpd.GeoDataFrame) -> plt:
    """
    Creates a map containing average Enade scores of each state

    Parameters
    ----------
    geodataframe: gpd.GeoDataFrame
        The map data with needed information

    Returns
    -------
    plt
        The graph plot object
    """

    # Plot the map with shades of green representing the average score
    geodataframe.plot(column=" Conceito Enade (Contínuo)",
                      cmap="Greens", legend=True)

    # hide the axis numbers since they represent latitude and longitude, and
    # have no meaning to the viz
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Add title
    plt.title("Média do Conceito Enade dos cursos de cada estado, "
              "para instituições públicas", fontsize=10)

    plt.gcf().set_size_inches(10, 6)

    return plt


if __name__ == "__main__":
    doctest.testmod()
