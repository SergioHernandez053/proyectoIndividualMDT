# Importante

La carpeta nuevo_escrapeo dentro del src no funciona. Se ha intentado hacer esta nueva técnica de escrapeo, puesto que la técnica antigua, que está en la carpeta de escrapeo no funciona ya debido a una actualización de Wallapop. 

Lo que se quería hacer con este nuevo algoritmo era extraer los anuncios por modelo y municipio, es decir, de la siguiente forma: https://es.wallapop.com/coches-segunda-mano/bmw-serie-1/madrid. De esta forma, ir modelo a modelo y municipio a municipio. Para esto, se querái utilizar los municipios extraidos por Julen Peralo y el nombre nombre de todos los modelos de Wikipedia extraidos por mi, pero por falta de tiempo esta ides no se ha podido llevar a cabo.

Los Scripts realmentee importantes con los que se ha escrapeado los datos de Wikipedia son Extraer.py y WallapopMain.py. El script ProcesamientoDatos.py se ha utilizado para eliminar el símbolo del euro de las etiquetas. El script src_a_webp.py en la carpeta procesado_csv se ha utilizado para extraer las imágenes que se almacenaban por enlaces y guardarlas en imágenes_comprimidas.zip en forma de webp.

La carpeta Scraped_data contiene toda la información extraida de todos los sitios.