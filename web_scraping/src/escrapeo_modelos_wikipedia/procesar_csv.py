from time import sleep

import pandas as pd
import re

def separar_colavoraciones(df, crear_csv = False, nombre = 'ModelosFiltrados'):
    marcas_modelos = []
    for index, row in df.iterrows():
        modelo = row["modelo"]
        modelo_split = modelo.split()
        marca2 = ""
        x = 0
        for idx in range(len(modelo_split) - 1):
            apilado = " ".join(modelo_split[0:idx])
            if apilado in df["marca"].values:

                modelo = " ".join(modelo_split[idx:])
                marca2 = apilado
                x = 1
                break
        nuevo_modelo = [row["marca"], marca2, modelo]
        if x == 1:
            print(nuevo_modelo)

        marcas_modelos.append(nuevo_modelo)
    print(marcas_modelos)
    df_filtrado = pd.DataFrame(marcas_modelos, columns=["marca", "marca_colavoracion", "modelo"])
    if crear_csv:
        df_filtrado.to_csv(f'{nombre}.csv', index = False)
    return df_filtrado

def eliminar_duplicados(df):
    df_sin_duplicados = df.drop_duplicates()
    return df_sin_duplicados

def main(path, nombre = 'ModelosFiltrados'):
    df = pd.read_csv(path)
    df_sin_duplicados = eliminar_duplicados(df)
    df_filtrado = separar_colavoraciones(df_sin_duplicados)
    df_filtrado.to_csv(f'{nombre}.csv', index=False)

main(path = 'modelos.csv')