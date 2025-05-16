import os
import pandas as pd
import shutil

'''
Este script elimina todos los elementos del csv y de la carpeta de imágenes los elementos que su precio sea un valor faltante.
Este script se ha utilizado con los datos del primer scrppeo puesto que había datos de tipo NaN en la columna del precio haciendo que esa muestra sea inservible por la falta de etiqueta.
'''

csv_path = '../../scraped_data/datos_coches_procesados.csv'
imagenes_dir = '../../imagenes_comprimidas'

df = pd.read_csv(csv_path)

filas_precio_vacio = df[df['precio'].isna()]

for url in filas_precio_vacio['url']:
    carpeta_path = os.path.join(imagenes_dir, url)
    if os.path.exists(carpeta_path):
        shutil.rmtree(carpeta_path)  # elimina toda la carpeta y su contenido
        print(f"Carpeta eliminada: {carpeta_path}")
    else:
        print(f"La carpeta NO A PODIDO ser eliminada: {carpeta_path}")



df = df.dropna(subset=['precio'])

df.to_csv(csv_path, index=False)
print("CSV actualizado.")
