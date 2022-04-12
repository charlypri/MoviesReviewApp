from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def cargaSemanal():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm")
    a=driver.find_elements(By.CLASS_NAME , "titleColumn")
    lista = []
    for i in a:
        nombre = i.find_element(By.TAG_NAME, "a")
        lista.append({"name":nombre.text,"cine":"Place Holder"})
    return lista

def cargaInicial():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
    a=driver.find_elements(By.CLASS_NAME , "titleColumn")
    lista = []
    for i in a:
        nombre = i.find_element(By.TAG_NAME, "a")
        lista.append({"name":nombre.text,"cine":"Place Holder"})
    return lista