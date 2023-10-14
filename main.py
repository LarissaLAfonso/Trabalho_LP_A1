import createobjects as co
import data_cleaner as dc
import graphs

data_path = "./dataframes/resultados_cpc_2021.csv"

messy_df = co.load_data_as_df(data_path)
clean_df = dc.dataframe_cleaner(messy_df)

non_attendence_df = co.create_non_attendance_df(clean_df)
average_scores_df = co.create_average_nota_by_region(clean_df)


non_attendence_graph = graphs.create_graph_non_attendance(non_attendence_df)
average_scores_graph = graphs.create_graph_average_scores_by_region(average_scores_df)


average_scores_graph.savefig('average_scores.png', dpi=300, bbox_inches='tight')
non_attendence_graph.savefig('non_attendence.png', dpi=300, bbox_inches='tight')