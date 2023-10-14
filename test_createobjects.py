"""
Contains unit tests for objects in the createobjects module.
"""

import unittest
import pandas as pd
import createobjects as co

class TestDataFrames(unittest.TestCase):
    def test_if_df_pddf(self):
        """
        Test if the dataframe objects are in fact instances of pd.DataFrame
        """
        self.assertIsInstance(co.df, pd.DataFrame)
        self.assertIsInstance(co.df_non_attendance, pd.DataFrame)
        
    def test_check_columns(self):
        """
        Checks the dataframes' columns.
        """
        self.assertEqual(co.df.columns.tolist(), ['Ano', 'Código da Área',
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
        self.assertEqual(co.df_non_attendance.columns.tolist(), ['Área de Avaliação', 'Taxa de Desistência Média'])
        
if __name__ == "__main__":
    unittest.main()
