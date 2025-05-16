import pandas as pd
import re

# Cargar el CSV
df = pd.read_csv('../../scraped_data/ciudades.csv')

# Define la columna a modificar
columna = 'text'  # <- cambia esto por el nombre real de tu columna
palabra_a_eliminar = 'Describe'  # <- cambia esto por la palabra que quieras quitar

# Función para limpiar cada valor
def limpiar_texto(texto):
    if pd.isna(texto):
        return texto
    texto = str(texto)
    # Eliminar la palabra
    texto = re.sub(rf'\b{re.escape(palabra_a_eliminar)}\b', '', texto, flags=re.IGNORECASE)
    # Eliminar ñ, Ñ, tildes
    texto = texto.lower()
    texto = re.sub(r'[ñÑ]', 'n', texto)
    texto = re.sub(r'[áÁ]', 'a', texto)
    texto = re.sub(r'[éÉ]', 'e', texto)
    texto = re.sub(r'[íÍ]', 'i', texto)
    texto = re.sub(r'[óÓ]', 'o', texto)
    texto = re.sub(r'[úÚ]', 'u', texto)
    texto = texto.replace('.', '')
    texto = texto.replace(' ', '-')
    return texto.strip()

# Aplicar la limpieza
df[columna] = df[columna].apply(limpiar_texto)

# Guardar el resultado en un nuevo CSV
df[[columna]].to_csv('ciudades.csv', index=False)