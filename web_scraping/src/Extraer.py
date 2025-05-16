from selenium.webdriver.common.by import By

def extraer_info(driver, url):
    """
    Extrae todos los datos de un anuncio
    :param driver: Driver de firefox
    :param url: enlace al anuncio
    :return: una lista de con todos los datos y un booleano que dice si se ha conseguido extraer la etiqueta (el precio) o no.
    """
    descripcion = ''
    marca = ''
    modelo = ''
    año = ''
    km = ''
    precio = ''
    pasar_elemento = False
    try:
        desc = driver.find_element(By.XPATH, "//div[@class = 'px-4']/div[contains(@class, 'item-detail_ItemDetail__separator__SCH3p')]/section[contains(@class, 'item-detail_ItemDetail__description__7rXXT')]")
        descripcion = desc.text
    except:
        pass
    try:
        obj_marca = driver.find_element(By.XPATH, "//div[contains(@class, 'item-detail-car-extra-info_ItemDetailCarExtraInfo__section__n4g_P')]/span[contains(text(), 'Marca')]")
        obj_marca_enc = obj_marca.find_element(By.XPATH, "./../a/span")
        marca = obj_marca_enc.text
    except:
        pass
    try:
        obj_modelo = driver.find_element(By.XPATH, "//div[contains(@class, 'item-detail-car-extra-info_ItemDetailCarExtraInfo__section__n4g_P')]/span[contains(text(), 'Modelo')]")
        obj_modelo_enc = obj_modelo.find_element(By.XPATH, "./../a/span")
        modelo = obj_modelo_enc.text
    except:
        pass
    try:
        obj_año = driver.find_element(By.XPATH, "//div[contains(@class, 'item-detail-car-extra-info_ItemDetailCarExtraInfo__section__n4g_P')]/span[contains(text(), 'Año')]/../span[not(@class)]")
        año = obj_año.text
    except:
        pass
    try:
        obj_km = driver.find_element(By.XPATH, "//div[contains(@class, 'item-detail-car-extra-info_ItemDetailCarExtraInfo__section__n4g_P')]/span[contains(text(), 'Kilómetros')]/../span[not(@class)]")
        km = obj_km.text
    except:
        pass
    try:
        precio_obj = driver.find_element(By.XPATH, "//span[contains(@class, 'item-detail-price_ItemDetailPrice--standard__TxPXr')]")
        precio = precio_obj.text
    except:
        try:
            precio_obj = driver.find_element(By.XPATH, "//span[contains(@class, 'item-detail-price_ItemDetailPrice--standardFinanced__14D3z')]")
            precio = precio_obj.text
        except:
            pasar_elemento = True
            pass
        pass

    return [url, marca, modelo, año, km, precio, descripcion], pasar_elemento

def extraer_nuevos_links(driver):
    links_coches = []
    try:
        coches = driver.find_elements(By.XPATH, "//div[@role = 'navigation' and @aria-label = 'Recommendation']/section[contains(@class, 'item-detail-recommendations_ItemDetailRecommendations___ZyQD')]/div[contains(@class, 'd-flex') and contains(@class, 'justify-content-center')]/a[contains(@class, 'item-detail-card-recommendation_ItemDetailCardRecommendation__DnAj6')]")
        for coche in coches:
            links_coches.append(coche.get_attribute('href'))
    except Exception:
        print("No se ha encontrado ningún coche")
        raise Exception
    return links_coches

def extraer_imagenes(driver, url):
    imagenes = []
    obj_imagen = driver.find_elements(By.XPATH, "//img[@slot = 'carousel-content-preview']")
    for obj in obj_imagen:
        imagenes.append([url,obj.get_attribute("src")])
    return imagenes
