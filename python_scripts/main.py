import createobjects as co
import data_cleaner as dc
import graphs
import downloads
import pandas as pd

# downloads the geojson
downloads.download_brazil_geojson()

# specifies the data location
data_path = "./data/dataframes/resultados_cpc_2021.csv"
map_path = "./data/map/brasil_estados.json"

# specifies the directory where the graphs will be saved
graphs_path = "./data/graphs"

try:
    # import and cleans the dataframe
    messy_df = co.load_data_as_df(data_path)
    clean_df = dc.dataframe_cleaner(messy_df)
    map_gdf = co.load_data_as_geodf(map_path)
    map_gdf = dc.add_state_name_to_data(map_gdf)

    # creates the dataframes that are used to create the graphs
    non_attendance_df = co.create_non_attendance_df(clean_df)
    average_scores_df = co.create_average_nota_by_region(clean_df)
    score_means_df = co.create_mean_of_general_score(clean_df)
    map_with_means_df = pd.merge(
        map_gdf, clean_df, how="left", on="Sigla da UF ")

    # creates the graphs and saves the graphs as .png
    non_attendance_graph = graphs.create_graph_non_attendance(
        non_attendance_df)
    non_attendance_graph.savefig(
        f'{graphs_path}/non_attendance.png', dpi=300, bbox_inches='tight')

    average_scores_graph = graphs.create_graph_average_scores_by_region(
        average_scores_df)
    average_scores_graph.savefig(
        f'{graphs_path}/average_scores.png', dpi=300, bbox_inches='tight')

    map_average_score = graphs.create_map_plot_average_score_by_state(
        map_with_means_df)
    map_average_score.savefig(
        f'{graphs_path}/average_score_states.png', dpi=300, bbox_inches='tight')

except FileNotFoundError:
    print("The filepath passed does not exist")
