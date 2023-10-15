
from createobjects import load_data_as_df
from createobjects import load_data_as_geodf
import pandas as pd
import geopandas as gpd

import unittest

class TestLoadDataAsDf(unittest.TestCase):

    # loads data from a valid .xlsx file and returns a pandas DataFrame
    def test_load_valid_xlsx_file(self):
        file_path = "./data/dataframes/resultados_cpc_2021.xlsx"
        df = load_data_as_df(file_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(len(df) > 0)

    # loads data from a valid .csv file and returns a pandas DataFrame
    def test_load_valid_csv_file(self):
        file_path = "./data/dataframes/resultados_cpc_2021.csv"
        df = load_data_as_df(file_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(len(df) > 0)

    # returns a pandas DataFrame with data when file is valid and not empty
    def test_return_dataframe_with_data(self):
        file_path = "./data/dataframes/resultados_cpc_2021.xlsx"
        df = load_data_as_df(file_path)
        self.assertTrue(len(df) > 0)

    # quits the program when FileNotFoundError or zipfile.BadZipfile is raised
    def test_quit_program_on_error(self):
        file_path = "./data/dataframes/nonexistent_file.xlsx"
        with self.assertRaises(SystemExit):
            load_data_as_df(file_path)


class TestLoadDataAsGeodf(unittest.TestCase):

    # loads data from a valid .json file and returns a geopandas geodataframe
    def test_valid_json_file(self):
        file_path = "./data/map/brasil_estados.json"
        geodf = load_data_as_geodf(file_path)
        self.assertIsInstance(geodf, gpd.GeoDataFrame)

    # loads data from a .json file with multiple features and returns a geopandas geodataframe with multiple rows
    def test_multiple_features(self):
        file_path = "./data/map/brasil_estados.json"
        geodf = load_data_as_geodf(file_path)
        self.assertGreater(len(geodf), 1)

    # quits the program when FileNotFoundError is raised
    def test_quit_program_on_error(self):
        file_path = "./data/dataframes/nonexistent_file.json"
        with self.assertRaises(SystemExit):
            load_data_as_df(file_path)



if __name__ == '__main__':
    unittest.main()