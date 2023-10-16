import pandas as pd
from graphs import *

import unittest


class TestCreateGraphNonAttendance(unittest.TestCase):

    # Creates a horizontal bar graph with non-attendance rate of each course
    def test_create_graph_non_attendance(self):
        data = {'Área de Avaliação': ['Course A', 'Course B', 'Course C'],
                'Taxa de Desistência Média': [5.2, 3.8, 7.1]}
        df = pd.DataFrame(data)
        plot = create_graph_non_attendance(df)
        self.assertEqual(plot.__class__.__name__, "module")


class TestCreateGraphAverageScoresByRegion(unittest.TestCase):

    # Test with a dataframe containing data for all regions and categories
    def test_create_graph_average_scores(self):
        data = {'Region': ['North', 'South', 'East'],
                'Category': ['Category A', 'Category B', 'Category C'],
                'Average Score': [4.2, 3.8, 4.1]}
        df = pd.DataFrame(data)
        plot = create_graph_average_scores_by_region(df)
        self.assertEqual(plot.__class__.__name__, "module")


class TestCreateMapPlotAverageScoreByState(unittest.TestCase):

    def test_create_map_average(self):

        data = {'Region': ['North', 'South', 'East'],
                'Average Score': [4.2, 3.8, 4.1]}

        df = pd.DataFrame(data)

        plot = create_map_plot_average_score_by_state(df)
        self.assertEqual(plot.__class__.__name__, "module")


if __name__ == "__main__":
    unittest.main()
