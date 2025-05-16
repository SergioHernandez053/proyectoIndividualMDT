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

def obtener_links(driver, url):
    """
    Función que extrae los links de los submenus
    :return: Lista con links extraidos
    """
    driver.get(url)
    driver.implicitly_wait(1)
    links_extraidos = []


    try:
        # Este paz estaba antes parece ser que lo han cambiado
        # //ul[contains(@class, seo-landing-page-cards-list_SeoLandingPageCardsList__AyyWJ)]/li[@aria-label = 'Items List Card']/a[contains(@class, seo-landing-page-cards-list-card_SeoLandingPageCardsListCard__q0s6N)]
        coches = driver.find_elements(By.XPATH,
                                      "//a[contains(@class, 'item-card_ItemCard--horizontal__zLpZu')]")
        for coche in coches:
            links_extraidos.append(coche.get_attribute('href'))
    except:
        print("NO HABÍA LINKS QUE EXTRAER")
        pass
    #sleep(10000)
    driver.quit()
    return links_extraidos