import pandas as pd
import numpy as np
from data_cleaner import *

import unittest


class TestDataframeCleaner(unittest.TestCase):

    # Test the function with a dataframe containing all the needed columns.
    def test_all_columns_present(self):
        data = pd.DataFrame({'Área de Avaliação': ['A', 'B', 'C'],
                             'Sigla da UF** ': ['AA', 'BB', 'CC'],
                             'Categoria Administrativa*': ["A", "B", "C"],
                             ' Conceito Enade (Contínuo)': [10, 10, 10],
                             ' Nota Padronizada - Regime de Trabalho': [9, 9, 9],
                             ' Nº de Concluintes Inscritos': [100, 200, 300],
                             ' Nº de Concluintes Participantes': [90, 180, 270],
                             ' Nota Padronizada - FG': [7.5, 8.0, 8.5],
                             ' Nota Padronizada - CE': [7.0, 7.5, 8.0],
                             ' Nota Padronizada - Organização Didático-Pedagógica': [8.5, 9.0, 9.5],
                             ' Nota Padronizada - Infraestrutura e Instalações Físicas': [8.0, 8.5, 9.0],
                             ' Nota Padronizada - Oportunidade de Ampliação da Formação': [9.0, 9.5, 10.0],
                             ' CPC (Faixa)': [4, 4, 4]})

        cleaned_data = dataframe_cleaner(data)

        expected_columns = ["Área de Avaliação", "Sigla da UF ", "Categoria Administrativa", " Nº de Concluintes Inscritos", " Nº de Concluintes Participantes",
                            " Conceito Enade (Contínuo)", " Nota Padronizada - Organização Didático-Pedagógica", " Nota Padronizada - Infraestrutura e Instalações Físicas", " Nota Padronizada - Oportunidade de Ampliação da Formação", " Nota Padronizada - Regime de Trabalho"]

        self.assertEqual(cleaned_data.columns.tolist(), expected_columns)

    # Test the function with a dataframe containing more columns than needed.

    def test_extra_columns_present(self):
        data = pd.DataFrame({'Área de Avaliação': ['A', 'B', 'C'],
                             'Sigla da UF** ': ['AA', 'BB', 'CC'],
                             'Categoria Administrativa*': ["A", "B", "C"],
                             ' Conceito Enade (Contínuo)': [10, 10, 10],
                             ' Nota Padronizada - Regime de Trabalho': [9, 9, 9],
                             ' Nº de Concluintes Inscritos': [100, 200, 300],
                             ' Nº de Concluintes Participantes': [90, 180, 270],
                             ' Nota Padronizada - FG': [7.5, 8.0, 8.5],
                             ' Nota Padronizada - CE': [7.0, 7.5, 8.0],
                             ' Nota Padronizada - Organização Didático-Pedagógica': [8.5, 9.0, 9.5],
                             ' Nota Padronizada - Infraestrutura e Instalações Físicas': [8.0, 8.5, 9.0],
                             ' Nota Padronizada - Oportunidade de Ampliação da Formação': [9.0, 9.5, 10.0],
                             ' CPC (Faixa)': [4, 4, 4],
                             'Extra Column': ['X', 'Y', 'Z']})

        cleaned_data = dataframe_cleaner(data)

        expected_columns = ["Área de Avaliação", "Sigla da UF ", "Categoria Administrativa", " Nº de Concluintes Inscritos", " Nº de Concluintes Participantes",
                            " Conceito Enade (Contínuo)", " Nota Padronizada - Organização Didático-Pedagógica", " Nota Padronizada - Infraestrutura e Instalações Físicas", " Nota Padronizada - Oportunidade de Ampliação da Formação", " Nota Padronizada - Regime de Trabalho"]

        self.assertEqual(cleaned_data.columns.tolist(), expected_columns)

    # Test the function with a dataframe that doesn't have the needed columns

    def test_columns_with_different_names(self):
        data = pd.DataFrame({'Area': ['A', 'B', 'C'],
                             'State': ['AA', 'BB', 'CC'],
                             ' CPC (Faixa)': [4, 4, 4]})

        with self.assertRaises(SystemExit):
            dataframe_cleaner(data)


class TestAreaDeAvaliacaoCleaner(unittest.TestCase):

    # should quit the program, since a needed column is missing
    def test_no_area_de_avaliacao_column(self):

        data = pd.DataFrame({'Other Column': ['Value 1', 'Value 2']})

        with self.assertRaises(SystemExit):
            area_de_avaliacao_cleaner(data)


class TestNomeDaIesFormater(unittest.TestCase):

    # Test with a dataframe containing a single row with a string in the 'Nome da IES' column.
    def test_single_row_with_string(self):
        data = pd.DataFrame({'Nome da IES': ['university of abc']})
        cleaned_data = nome_da_ies_formater(data)
        self.assertTrue('Nome da IES' in cleaned_data.columns)
        self.assertEqual(cleaned_data['Nome da IES'].tolist(), [
                         'University Of Abc'])

    # Test with a dataframe containing multiple rows with strings in the 'Nome da IES' column.
    def test_multiple_rows_with_strings(self):
        data = pd.DataFrame(
            {'Nome da IES': ['university of abc', 'escola de matemática aplicada']})
        cleaned_data = nome_da_ies_formater(data)
        self.assertTrue('Nome da IES' in cleaned_data.columns)
        self.assertEqual(cleaned_data['Nome da IES'].tolist(), [
                         'University Of Abc', 'Escola De Matemática Aplicada'])

    # Test with a dataframe containing a single row with an empty string in the 'Nome da IES' column.
    def test_single_row_with_empty_string(self):
        data = pd.DataFrame({'Nome da IES': ['']})
        cleaned_data = nome_da_ies_formater(data)
        self.assertTrue('Nome da IES' in cleaned_data.columns)
        self.assertEqual(cleaned_data['Nome da IES'].tolist(), [''])

    # Test with a dataframe containing no 'Nome da IES' column.
    def test_no_nome_da_ies_column(self):
        data = pd.DataFrame({'Other Column': ['value']})

        with self.assertRaises(SystemExit):
            nome_da_ies_formater(data)


class TestAreaDeAvaliacaoLong(unittest.TestCase):

    # Test with a dataframe containing both names that need to be modified and names that do not need to be modified.
    def test_mixed_names(self):
        data = pd.DataFrame({'Área de Avaliação': [
                            'Tecnologia Em Redes De Computadores', 'Other', 'Tecnologia Em Análise E Desenvolvimento De Sistemas', 'Another']})
        expected_data = pd.DataFrame({'Área de Avaliação': [
                                     'Redes De Computadores', 'Other', 'Desenvolvimento De Sistemas', 'Another']})
        modified_data = area_de_avaliacao_long(data)
        self.assertEqual(modified_data['Área de Avaliação'].tolist(
        ), expected_data['Área de Avaliação'].tolist())

    # Test with an empty dataframe.
    def test_empty_dataframe(self):
        data = pd.DataFrame({'Área de Avaliação': []})
        expected_data = pd.DataFrame({'Área de Avaliação': []})
        modified_data = area_de_avaliacao_long(data)
        self.assertEqual(modified_data['Área de Avaliação'].tolist(
        ), expected_data['Área de Avaliação'].tolist())


class TestAddStateNameToData(unittest.TestCase):

    # Test with a GeoDataFrame containing Brazil map data with all state codes
    def test_all_state_codes(self):
        # Create a GeoDataFrame with all state codes
        gdf = gpd.GeoDataFrame({'codarea': [12, 27, 16, 13, 29, 23, 53, 32, 52, 21, 51, 50, 31,
                               15, 25, 41, 26, 22, 24, 43, 33, 11, 14, 42, 35, 28, 17], 'geometry': [None] * 27})

        # Call the function under test
        gdf_with_state = add_state_name_to_data(gdf)

        # Check if the "Sigla da UF" column is present
        self.assertTrue('Sigla da UF ' in gdf_with_state.columns)

        # Check if the state abbreviations are correct
        self.assertEqual(gdf_with_state['Sigla da UF '].tolist(), ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
                         'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RN', 'RS', 'RJ', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'])

    # Test with a GeoDataFrame containing Brazil map data with invalid state codes

    def test_valid_state_codes(self):
        # Create a GeoDataFrame with valid state codes
        gdf = gpd.GeoDataFrame(
            {'codarea': [30, 30, 30], 'geometry': [None, None, None]})

        with self.assertRaises(SystemExit):
            add_state_name_to_data(gdf)


if __name__ == "__main__":
    unittest.main()
