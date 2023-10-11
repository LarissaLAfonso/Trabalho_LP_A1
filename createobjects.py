import pandas as pd
import openpyxl
import zipfile
# openpyxl is used by pandas when calling the `read_excel` function. It was
# imported here so the script can ensure the user have it installed before
# trying to run anything.

def load_data_as_df(file_path:str) -> pd.DataFrame:
    """Loads the data from a .xlsx file and return a pandas dataframe.
    Parameters
    ----------
    file_path: str
        The path to where the file with data is located.

    Returns
    -------
    pd.DataFrame
        A pandas dataframe with the data contained in the excel file
    """
    try:
        dataframe = pd.read_excel(file_path)
    except FileNotFoundError:
        print("The file path passed is invalid.")
        quit()
    except zipfile.BadZipfile:
        print("the file could not be read. It is probably corrupted. Consider replacing it.")
        quit()
    return dataframe
