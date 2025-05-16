import pandas as pd
import re
def quitar_euro_punto(df_data):
    """
    Procesa los precios para quitarles el símbolo del euro
    :param df_data: dataframe a procesar
    :return: dataframe sin el símbolo de euro en la columna de precio
    """
    df_data["precio"] = df_data["precio"].str.replace(r" €", '', regex=True)
    return df_data

def url_a_clave(df_data):
    df_data['url'] = df_data["url"].replace(r'https://es.wallapop.com/item/', '', regex=True)
    return df_data

df = pd.read_csv('../scraped_data/datos_coches.csv')
df = quitar_euro_punto(df)
df = url_a_clave(df)
df.to_csv('datos_coches_procesados.csv', index=False)