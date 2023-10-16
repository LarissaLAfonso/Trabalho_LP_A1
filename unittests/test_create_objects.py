import pandas as pd
import geopandas as gpd
from create_objects import *

import unittest


class TestLoadDataAsDf(unittest.TestCase):

    # loads data from a valid .xlsx file and returns a pandas DataFrame
    def test_load_valid_xlsx_file(self):
        file_path = "./dataframes/resultados_cpc_2021.xlsx"
        df = load_data_as_df(file_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(len(df) > 0)

    # loads data from a valid .csv file and returns a pandas DataFrame
    def test_load_valid_csv_file(self):
        file_path = "./dataframes/resultados_cpc_2021.csv"
        df = load_data_as_df(file_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(len(df) > 0)

    # returns a pandas DataFrame with data when file is valid and not empty
    def test_return_dataframe_with_data(self):
        file_path = "./dataframes/resultados_cpc_2021.xlsx"
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
        file_path = "./dataframes/brasil_estados.json"
        geodf = load_data_as_geodf(file_path)
        self.assertIsInstance(geodf, gpd.GeoDataFrame)

    # loads data from a .json file with multiple features and returns a geopandas geodataframe with multiple rows
    def test_multiple_features(self):
        file_path = "./dataframes/brasil_estados.json"
        geodf = load_data_as_geodf(file_path)
        self.assertGreater(len(geodf), 1)

    # quits the program when FileNotFoundError is raised
    def test_quit_program_on_error(self):
        file_path = "./data/dataframes/nonexistent_file.json"
        with self.assertRaises(SystemExit):
            load_data_as_df(file_path)


class TestCreateNonAttendanceDf(unittest.TestCase):

    # test with a dataframe containing missing values in 'Área de Avaliação' column
    def test_missing_values_area_avaliacao(self):
        # create sample dataframe with missing values in 'Área de Avaliação' column
        sample_data = pd.DataFrame({
            'Área de Avaliação': [None, 'Course B', 'Course A', 'Course C'],
            ' Nº de Concluintes Inscritos': [100, 120, 90, 80],
            ' Nº de Concluintes Participantes': [80, 110, 70, 70]
        })

        result = create_non_attendance_df(sample_data)

        # check if the 'Taxa de Desistência Média' column is present in the result
        self.assertIn('Taxa de Desistência Média', result.columns)

        # check if the result dataframe has more than 0 rows
        self.assertTrue(len(result) > 0)

    # test with a dataframe containing missing values in some columns
    def test_missing_values_other_columns(self):
        # create sample dataframe with missing values in other columns
        sample_data = pd.DataFrame({
            'Área de Avaliação': ['Course A', 'Course B', None, 'Course C'],
            ' Nº de Concluintes Inscritos': [100, None, 90, 80],
            ' Nº de Concluintes Participantes': [80, 110, 70, None]
        })

        result = create_non_attendance_df(sample_data)

        # check if the 'Taxa de Desistência Média' column is present in the result
        self.assertIn('Taxa de Desistência Média', result.columns)

        # check if the result dataframe has more than 0 rows
        self.assertTrue(len(result) > 0)


class TestCreateRegionColumnDf(unittest.TestCase):

    # Test if the function provide the correct outputs
    def test_region_column_added_to_dataframe(self):

        sample_data = pd.DataFrame({
            'UF': ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
        })

        expected_region_list = ['Norte', 'Nordeste', 'Norte', 'Norte', 'Nordeste', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Centro-Oeste', 'Nordeste', 'Centro-Oeste',
                                'Centro-Oeste', 'Sudeste', 'Norte', 'Nordeste', 'Sul', 'Nordeste', 'Nordeste', 'Sudeste', 'Nordeste', 'Sul', 'Norte', 'Norte', 'Sul', 'Sudeste', 'Nordeste', 'Norte']

        region_series = create_region_column_df(sample_data, 'UF')

        region_list = region_series.to_list()

        # check if the 'Region' column is present in the result
        self.assertEqual(region_list, expected_region_list)


class TestCreateAverageNotaByRegion(unittest.TestCase):

    # Test if the function raises a KeyError when the input DataFrame doesn't have all needed columns
    def test_raises_key_error_when_missing_columns(self):

        sample_data = pd.DataFrame({
            'Sigla da UF ': ['SP', 'RJ', 'MG', 'BA', 'AM', 'PA'],
            ' Nota Padronizada - Organização Didático-Pedagógica': [8.5, 7.2, 6.8, 8.0, 7.5, 6.2],
            ' Nota Padronizada - Infraestrutura e Instalações Físicas': [7.8, 7.5, 6.4, 8.2, 6.9, 6.1],
            ' Nota Padronizada - Oportunidade de Ampliação da Formação': [7.2, 7.0, 6.3, 7.9, 6.5, 5.9]
        })

        # quits the program when the dataframe passed is missing a column
        with self.assertRaises(SystemExit):
            create_average_nota_by_region(sample_data)


class TestCreateMeanOfGeneralScore(unittest.TestCase):

    # Test with a dataframe containing only public universities
    def test_only_public_universities(self):
        sample_data = pd.DataFrame({
            'Sigla da UF ': ['SP', 'RJ', 'MG'],
            'Categoria Administrativa': ['Pública Federal', 'Pública Estadual', 'Pública Federal'],
            ' Conceito Enade (Contínuo)': [4.5, 4.5, 5]
        })

        mean_score_df = create_mean_of_general_score(sample_data)

        mean_score_dict = mean_score_df.to_dict()
        expected_mean_score_dict = {'Sigla da UF ': {
            0: 'MG', 1: 'RJ', 2: 'SP'}, ' Conceito Enade (Contínuo)': {0: 5.0, 1: 4.5, 2: 4.5}}

        self.assertEqual(mean_score_dict, expected_mean_score_dict)

    # Test with a dataframe containing only private universities
    def test_only_private_universities(self):
        sample_data = pd.DataFrame({
            'Sigla da UF ': ['SP', 'RJ', 'MG'],
            'Categoria Administrativa': ['Privada', 'Privada', 'Privada'],
            ' Conceito Enade (Contínuo)': [4.5, 4.5, 5]
        })

        mean_score_df = create_mean_of_general_score(sample_data)

        mean_score_dict = mean_score_df.to_dict()
        expected_mean_score_dict = {
            'Sigla da UF ': {}, ' Conceito Enade (Contínuo)': {}}

        self.assertEqual(mean_score_dict, expected_mean_score_dict)


class TestDataFrames(unittest.TestCase):

    # test if the dataframe objects are in fact instances of pd.DataFrame
    def test_if_df_pddf(self):

        self.assertIsInstance(load_data_as_df(
            "./dataframes/resultados_cpc_2021.csv"), pd.DataFrame)
        self.assertIsInstance(load_data_as_df(
            "./dataframes/resultados_cpc_2021.xlsx"), pd.DataFrame)
        self.assertIsInstance(load_data_as_geodf(
            "./dataframes/brasil_estados.json"), gpd.GeoDataFrame)
        dataframe = load_data_as_df(
            "./dataframes/resultados_cpc_2021.csv")
        df_non_attendance = create_non_attendance_df(dataframe)
        self.assertIsInstance(df_non_attendance, pd.DataFrame)

    # checks the dataframes' columns.
    def test_check_columns(self):

        dataframe = load_data_as_df(
            "./dataframes/resultados_cpc_2021.csv")
        self.assertEqual(dataframe.columns.tolist(), ['Ano', 'Código da Área',
                                                      'Área de Avaliação', 'Grau acadêmico',
                                                      'Código da IES*', 'Nome da IES*', 'Sigla da IES*',
                                                      'Organização Acadêmica*', 'Categoria Administrativa*', 'Código do Curso**',
                                                      'Modalidade de Ensino***', 'Código do Município***', 'Município do Curso***',
                                                      'Sigla da UF** ', ' Nº de Concluintes Inscritos', ' Nº de Concluintes Participantes',
                                                      ' Nota Bruta - FG', ' Nota Padronizada - FG', ' Nota Bruta - CE', ' Nota Padronizada - CE',
                                                      ' Conceito Enade (Contínuo)', ' Concluintes participantes com nota no Enem', ' Proporção de concluintes participantes com nota no Enem',
                                                      ' Nota Bruta - IDD', ' Nota Padronizada - IDD', ' Nota Bruta – Organização Didático-Pedagógica', ' Nota Padronizada - Organização Didático-Pedagógica',
                                                      ' Nota Bruta – Infraestrutura e Instalações Físicas', ' Nota Padronizada - Infraestrutura e Instalações Físicas', ' Nota Bruta – Oportunidade de Ampliação da Formação',
                                                      ' Nota Padronizada - Oportunidade de Ampliação da Formação', ' Nota Bruta - Mestres', ' Nota Padronizada - Mestres', ' Nota Bruta - Doutores', ' Nota Padronizada - Doutores',
                                                      ' Nota Bruta – Regime de Trabalho', ' Nota Padronizada - Regime de Trabalho', ' CPC (Contínuo)', ' CPC (Faixa)', 'Observação'])
        df_non_attendance = create_non_attendance_df(dataframe)
        self.assertEqual(df_non_attendance.columns.tolist(), [
                         'Área de Avaliação', 'Taxa de Desistência Média'])


if __name__ == '__main__':
    unittest.main()
