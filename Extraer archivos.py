import requests
from urllib.request import urlretrieve
from zipfile import ZipFile
import os
import pandas as pd

# Hacer la petición a la API para obtener los recursos
raw_json = requests.get('https://us-central1-duoc-bigdata-sc-2023-01-01.cloudfunctions.net/datos_transporte_et').json()
resources = raw_json['result']['resources']
i = 0

# Diccionario para almacenar listas de DataFrames por nombre de archivo
dataframes_dict = {}

extract_path = f"{os.getcwd()}/data/"

for resource in resources:
    # Crear el directorio donde se extraerán los archivos
    extract_path = f"{os.getcwd()}/data/file_{i}"
    os.makedirs(extract_path, exist_ok=True)
    print(f"Downloading from {resource['url']}")
    # Descargo los archivos de la URL extraída directamente de la API.
    zip_path = f'{os.getcwd()}/data/file_{i}.zip'
    urlretrieve(resource['url'], zip_path)
    
    with ZipFile(zip_path, "r") as zObject:
        zObject.extractall(extract_path)
    
    # Leer y almacenar DataFrames
    for filename in os.listdir(extract_path):
        if filename.endswith(".txt"):
            txt_file_path = os.path.join(extract_path, filename)
            csv_file_path = os.path.join(extract_path, filename.replace(".txt", ".csv"))
            os.rename(txt_file_path, csv_file_path)
            
            # Leer el archivo CSV y añadirlo al diccionario
            df = pd.read_csv(csv_file_path)
            csv_filename = os.path.basename(csv_file_path)
            if csv_filename not in dataframes_dict:
                dataframes_dict[csv_filename] = []
            dataframes_dict[csv_filename].append(df)
    i += 1

# Fusionar y guardar los DataFrames
output_path = f"{os.getcwd()}/merged"
os.makedirs(output_path, exist_ok=True)
for filename, dataframes in dataframes_dict.items():
    merged_df = pd.concat(dataframes, ignore_index=True)
    merged_df.to_csv(os.path.join(output_path, filename), index=False)
os.remove(f'{os.getcwd()}/data/')

print("Descarga, extracción y fusión completadas.")
