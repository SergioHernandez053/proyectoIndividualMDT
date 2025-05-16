import requests
from PIL import Image
from io import BytesIO
import zipfile
import os
import pandas as pd
import re

# Cargar el CSV
df = pd.read_csv("../../scraped_data/imagenes_coches.csv")
df_data = pd.read_csv("../../scraped_data/datos_coches.csv")
url_eliminados = []

# Procesar cada fila
with zipfile.ZipFile("../../scraped_data/imagenes_comprimidas.zip", "w") as zipf:
    for _, fila in df.iterrows():
        src = fila["src"]
        url = fila["url"]

        if url in url_eliminados:
            continue

        patron = r"https://es.wallapop.com/item/"# Nombre de subcarpeta
        nuevo_grupo = re.sub(patron, "", url)

        # Nombre del archivo desde la URL (puedes hacer algo más elaborado si quieres)
        nombre_base1 = src.split("/")[8]
        nombre_base2 = src.split("/")[9].split("?")
        nombre_imagen = nombre_base1 + "_" + re.sub(".jpg", "", nombre_base2[0]) + ".webp"
        ruta_zip = os.path.join(nuevo_grupo, nombre_imagen)

        try:
            # Descargar la imagen
            resp = requests.get(src, timeout=10)
            resp.raise_for_status()

            # Redimensionar y convertir
            img = Image.open(BytesIO(resp.content)).convert("RGB")
            img = img.resize((256, 256))

            buffer = BytesIO()
            img.save(buffer, format="WEBP")
            buffer.seek(0)
            #zipf.writestr(f"{nuevo_grupo}/", "")

            zipf.writestr(ruta_zip, buffer.read())

            print(f"✔ Guardada {nombre_imagen} en {ruta_zip}")

        except Exception as e:
            url_eliminados.append(fila["url"])
            print(f"❌ Error con {url}: {e}")

df_filtrado = df_data[~df_data['id'].isin(url_eliminados)]
df_filtrado.to_csv("datos_coches.csv", index=False)