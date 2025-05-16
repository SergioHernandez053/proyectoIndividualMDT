import time
import pandas as pd
import numpy as np
from datetime import datetime
import re
import locale
import multiprocessing as mp
from multiprocessing import Process
import numpy as np
import threading

# Importing Selenium library and relevant classes
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


WIKI = 'https://es.wikipedia.org'

def unir(str1, str2):
    return str1+str2

def obtener_links(driver):
    driver.get("https://es.wikipedia.org/wiki/Categor%C3%ADa:Modelos_de_autom%C3%B3viles_por_marca")
    driver.implicitly_wait(1)
    objetos_iniciales = driver.find_elements(By.XPATH, '//a[contains(@title, "Categoría:Modelos de")]')
    links = []
    texto = []
    for obj in objetos_iniciales:
        links.append(obj.get_attribute('href'))
        texto.append(re.sub(r"^(Modelos de )+", r"", obj.text))
    obj_link = np.column_stack((np.array(links), np.array(texto))).tolist()
    return obj_link

def obtener_modelos(driver, link):
    driver.get(link[0])
    driver.implicitly_wait(0)
    lista_modelos = []
    lista_links = []
    try:
        modelos = driver.find_elements(By.XPATH, "//div[contains(@id, 'bodyContent')]//div[@class = 'mw-category mw-category-columns']//li/a")
        for mod in modelos:
            nombre = re.sub(re.escape(link[1]), r"", mod.text)
            if nombre.strip() != '':
                lista_modelos.append([link[1], nombre])

    except NoSuchElementException:
        print("No se ha encontrado ningún modelo o la aplicación ha fallado")
        pass
    try:
        links_nuevos = driver.find_elements(By.XPATH, f"//div[@class = 'mw-content-ltr']//ul/li/div[@class = 'CategoryTreeSection']/div[@class = 'CategoryTreeItem']/bdi[@dir = 'ltr']/a")

        for li in links_nuevos:
            lista_links.append([li.get_attribute('href'), link[1]])

    except NoSuchElementException:
        print("No se ha encontrado ningún link nuevo")
        pass
    return lista_modelos, lista_links


def main(driver):
    modelos = []
    links = obtener_links(driver)
    it = 0
    while len(links) != 0 and it < 202:
        link = links.pop(0)
        mod_nuevos, links_nuevos = obtener_modelos(driver, link)
        modelos.extend(mod_nuevos)
        links.extend(links_nuevos)
    df = pd.DataFrame(modelos, columns = ["marca", "modelo"])
    df.to_csv("modelos.csv", index=False, encoding="utf-8")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

#obtener_links(driver)
#mod, link = obtener_modelos(driver, ['https://es.wikipedia.org/wiki/Categor%C3%ADa:Modelos_de_BMW', 'BMW'])
print(main(driver))
