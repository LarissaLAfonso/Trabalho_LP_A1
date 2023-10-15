"""
Module to download some of the data.
"""

import requests
import json

def download_brazil_geojson() -> None:
    """Requests Brazil map information from IBGE's API and saves it
    in a file named "brasil_estados.json".

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    download_url = "http://servicodados.ibge.gov.br/api/v3/malhas/paises/BR"\
    "?formato=application/vnd.geo+json&qualidade=maxima&intrarregiao=UF"
    try:
        http_response = requests.get(download_url)
        http_response.raise_for_status()
        if http_response.headers["Content-Type"] != "application/vnd.geo+json; charset=utf-8":
            raise TypeError
        else:
            geojson_data = http_response.json()
    except requests.ConnectionError:
        print("It wasn't possible to stabilish a connection with the site."\
            " Either the gov site is down or you have no connection to the internet.")
        quit()
    except requests.HTTPError as error:
        print("The site didn't returned a good status code, which means it "\
            "wasn't possible to download the data.", error)
        quit()
    except requests.Timeout:
        print("There was a timeout while trying to download the data")
        quit()
    except TypeError:
        print("The gov site didn't returned the data in the desired format.")
        quit()

    with open('brasil_estados.json', 'w') as json_file:
        json.dump(geojson_data, json_file)
