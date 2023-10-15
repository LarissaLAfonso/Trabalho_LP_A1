import createobjects as co
import data_cleaner as dc
import graphs

# specifies the data location
data_path = "./data/dataframes/resultados_cpc_2021.csv"
map_path = "./brasil_estados.json"

# specifies the directory where the graphs will be saved
graphs_path = "./data/graphs"

# import and cleans the dataframe
messy_df = co.load_data_as_df(data_path)
clean_df = dc.dataframe_cleaner(messy_df)
map_gdf = co.load_data_as_geodf(map_path)
map_gdf = dc.add_state_name_to_data(map_gdf)

# creates the dataframes that are used to create the graphs
non_attendence_df = co.create_non_attendance_df(clean_df)
average_scores_df = co.create_average_nota_by_region(clean_df)
grade_means_df = co.create_mean_of_general_grade(clean_df)
map_with_means_df = co.merge_map_data_with_means(clean_df, map_gdf)

# creates the graphs and saves the graphs as .png
non_attendence_graph = graphs.create_graph_non_attendance(non_attendence_df)
non_attendence_graph.savefig(f'{graphs_path}/non_attendence.png', dpi=300, bbox_inches='tight')

average_scores_graph = graphs.create_graph_average_scores_by_region(average_scores_df)
average_scores_graph.savefig(f'{graphs_path}/average_scores.png', dpi=300, bbox_inches='tight')

map_average_grades = graphs.create_map_plot_average_grades_by_state(map_with_means_df)
map_average_grades.savefig(f'{graphs_path}/average_grades_states.png', dpi=300, bbox_inches='tight')
