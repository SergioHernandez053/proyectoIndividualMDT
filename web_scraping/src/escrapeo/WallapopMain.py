import time
import pandas as pd
import csv
from time import sleep
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process, Manager

from src.Extraer import extraer_imagenes, extraer_info, extraer_nuevos_links

NUM_PROCESOS = 4


def obtener_links_iniciales():
    """
    Función que extrae los links iniciales del menu de wallapop
    :return:
    """
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get('https://es.wallapop.com/coches-segunda-mano')
    time.sleep(5)
    driver.implicitly_wait(1)
    links_extraidos = []
    try:
        cookies = driver.find_element("//div[@id = 'onetrust-banner-sdk']//button[@id = 'onetrust-reject-all-handler']")
        cookies.click()
    except:
        print("No se ha podido clickar en el botón de cookies")
        pass

    try:
        # Este paz estaba antes parece ser que lo han cambiado
        # //ul[contains(@class, seo-landing-page-cards-list_SeoLandingPageCardsList__AyyWJ)]/li[@aria-label = 'Items List Card']/a[contains(@class, seo-landing-page-cards-list-card_SeoLandingPageCardsListCard__q0s6N)]
        coches = driver.find_elements(By.XPATH,
                                      "//a[contains(@class, 'item-card_ItemCard--horizontal__zLpZu')]")
        for coche in coches:
            links_extraidos.append(coche.get_attribute('href'))
    except Exception:
        raise Exception
    #sleep(10000)
    driver.quit()
    print(links_extraidos)
    return links_extraidos

def launch_driver():
    """
    Función que devuelve un driver en el que no se cargan los elementos css, no se carga en pantalla el driver y no carga las imágenes para
    que sea más eficiente
    :return: Un driver de Firefox
    """
    # Configuración del driver
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                 "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent)
    profile.set_preference("permissions.default.image", 2)  # 2 = bloquear imágenes
    profile.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")
    profile.set_preference("permissions.default.stylesheet", 2)  # desactiva CSS
    options.profile = profile
    driver = webdriver.Firefox(options=options)
    return driver
def worker(link_queue, data_list, imagenes_list, visited_set, num_muestras):
    """
    Proceso que escrapea links e información de los anuncios de coches de wallapop
    :param link_queue: lista de todos los anuncios sin visitar (compartida por todos los procesos)
    :param data_list: lista de toda la información de los anuncios extraidos (compartida por todos los procesos)
    :param imagenes_list: Lista compuesta por los links que llevan a las imágenes y los links de los respectivos anuncios a los que pertenecen las imágenes (compartida por todos los procesos)
    :param visited_set: Lista de todos los anuncios visitados (compartida por todos los procesos)
    :param num_muestras: Número de anuncios que tiene que extraer cada procesador
    """
    driver = launch_driver()

    i = 0
    paciencia = 0

    while i < num_muestras:
        if i % 1000 == 0 and i != 0:
            sleep(15)
        if i % 50 == 0 and i != 0:
            driver.quit()
            sleep(3)
            driver = launch_driver()
        try:
            url = link_queue.pop(0)
            paciencia = 0
        except IndexError:
            if paciencia < 100:
                paciencia += 1
                sleep(0.1)
                continue
            else:
                print("Se han terminado todos los links")
                break

        if url in visited_set:
            continue
        visited_set.append(url)

        try:
            driver.get(url)
            try:
                WebDriverWait(driver, 1.2).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role = 'navigation' and @aria-label = 'Recommendation']/section[contains(@class, 'item-detail-recommendations_ItemDetailRecommendations___ZyQD')]/div[contains(@class, 'd-flex') and contains(@class, 'justify-content-center')]"))
                )
            except TimeoutException:
                pass
            links = extraer_nuevos_links(driver)
            coche_info, pasar_anuncio = extraer_info(driver, url)
            print(links)
            print(coche_info)
            imagenes = extraer_imagenes(driver, url)

            link_queue.extend(links)
            # Si no se ha conseguido extraer el precio (la etiqueta) no se inserta en los datos
            if pasar_anuncio or coche_info[5] == '':
                continue
            data_list.append(coche_info)
            imagenes_list.extend(imagenes)
            i += 1
        except Exception as e:
            print(f"[x] Error en {url}: {e}")

    driver.quit()

def main(num_muestras, cargar_links_visitados = True):
    """
    Función principal que genera el manager, los procesos y las listas de las funciones de arriba
    :param num_muestras: Número de muestras totales que se quieren extraer
    :param cargar_links_visitados: Si se tiene un csv con datos y no se quieren extraer los datos que ya se tienen
    :return:
    """
    visitados = []
    if cargar_links_visitados:
        df_visitados = pd.read_csv('../../scraped_data/datos_coches.csv')
        visitados = df_visitados['url'].tolist()

    with Manager() as manager:
        link_queue = manager.list()
        visited_set = manager.list()
        data = manager.list()
        imagenes = manager.list()

        visited_set.extend(visitados)
        link_queue.extend(['https://es.wallapop.com/item/bmw-serie-3-2004-1129171646', 'https://es.wallapop.com/item/seat-leon-2003-1129340727', 'https://es.wallapop.com/item/bmw-serie-3-2004-1114477682'])
        muestras_por_hilo = num_muestras/NUM_PROCESOS

        link_queue.extend(obtener_links_iniciales())
        procesos = []
        for _ in range(NUM_PROCESOS):
            p = Process(target=worker, args=(link_queue, data, imagenes, visited_set, muestras_por_hilo))
            procesos.append(p)
            p.start()

        for p in procesos:
            p.join()

        data_list = list(data)
        imagenes_list = list(imagenes)
        link_list = list(link_queue)
        print(len(data_list))
        with open('../../scraped_data/datos_coches.csv', mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(data_list)
        with open('../../scraped_data/imagenes_coches-2.csv', mode='a', newline='', encoding='utf-8') as archivo2:
            escritor2 = csv.writer(archivo2)
            escritor2.writerows(imagenes_list)
        with open('../../scraped_data/links_sin_visitar.csv', mode='a', newline='', encoding='utf-8') as archivo2:
            escritor2 = csv.writer(archivo2)
            escritor2.writerows(link_list)

        #df_data = pd.DataFrame(data_list, columns=["url", 'marca', 'modelo', 'año', 'km', 'precio', 'desc'])
        #df_imagenes = pd.DataFrame(imagenes_list, columns=["url", "src"])
        #df_links = pd.DataFrame(link_list, columns=["url"])
        #df_imagenes.to_csv('imagenes_coches-2.csv', index=False)
        #df_data.to_csv('datos_coches.csv-2', index=False)
        #df_links.to_csv('links_sin_visitar.csv', index=False)

main(10000)