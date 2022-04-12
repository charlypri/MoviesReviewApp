import requests as rq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import sys


def recogerDatosFilmaffinity(pelicula):
    #Busqueda de la pelicula
    url="https://www.filmaffinity.com/es/search.php?stext="+(pelicula.replace(" ","+").lower())

    pagina=rq.get(url)    

    temp=pagina.text[pagina.text.find("<div class=\"cpanel\">"):][pagina.text[pagina.text.find("<div class=\"cpanel\">"):].find("movie-card movie-card-1")+40:pagina.text[pagina.text.find("<div class=\"cpanel\">"):].find("movie-card movie-card-1")+46]

    urlPelicula = "https://www.filmaffinity.com/es/film"+temp+".html"

    paginaPelicula=rq.get(urlPelicula)  
    #Obtencion de puntuacion
    punt=paginaPelicula.text[paginaPelicula.text.find("<div id=\"movie-rat-avg\" itemprop=\"ratingValue\" content=\"")+len("<div id=\"movie-rat-avg\" itemprop=\"ratingValue\" content=\""):paginaPelicula.text.find("<div id=\"movie-rat-avg\" itemprop=\"ratingValue\" content=\"")+len("<div id=\"movie-rat-avg\" itemprop=\"ratingValue\" content=\"")+3].replace("\">","")

    inicio=paginaPelicula.text.find("<ul id=\"pro-reviews\">")+len("<ul id=\"pro-reviews\">")
    fin=paginaPelicula.text[inicio:].find("</ul>")
    #Obtencion de criticas
    criticas=paginaPelicula.text[inicio : inicio+fin]  

    criticas=criticas.split("<div itemprop=\"reviewBody\">")[1:]

    for i in range(len(criticas)):
        criticas[i]=criticas[i][:criticas[i].find("<")].replace("&nbsp;","").replace("&quot;","")
    #Creacion del JSON
    resultado = {"Nombre": pelicula,"Puntuacion":punt,"Criticas":criticas}

    return resultado

def getRottenTomatoes(pelicula):
    #This makes the browser run headless
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    #Run the web browser with the setted options
    # driver = webdriver.Chrome()
    driver.get("https://www.rottentomatoes.com/m/"+(pelicula.replace(" ","_").lower()) )

    inp_xpath_movieTitle = "//h1[@class='mop-ratings-wrap__title mop-ratings-wrap__title--top'][@data-qa='score-panel-movie-title']"
    movieTitle = driver.find_element_by_xpath(inp_xpath_movieTitle).text
    
    #Get criticas
    criticas = []
    inp_xpath_Criticas = driver.find_elements_by_xpath("//blockquote[@class='media-body quote_bubble__quote']/p")
    for crit in inp_xpath_Criticas:
        criticas.append(crit.text)

    inp_xpath_button = "//button[@class='mop-ratings-wrap__score-detail-text']"
    driver.find_element_by_xpath(inp_xpath_button).click()
    
    #Get puntuación de los criticos de rotten tomatoes
    inp_xpath_Tomatometer = "//span[@class='js-tomatometer-score-info']"
    tomatometer = driver.find_element_by_xpath(inp_xpath_Tomatometer).text
    tomatometer = tomatometer.split("/")[0]

    #Get puntuación de la audiencia
    inp_xpath_Audience = "//span[@class='js-audience-score-info']"
    audience = driver.find_element_by_xpath(inp_xpath_Audience).text
    audience = float(audience)*2

    

    resultado = {"Nombre": movieTitle,"Puntuacion":tomatometer,"Criticas":criticas}
    # print(resultado)
    return resultado
    driver.quit()

def recogerDatosIMDb(pelicula):
    #Busqueda de la pelicula
    url="https://www.imdb.com/find?q="+pelicula+"&ref_=nv_sr_sm"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html) # create a new bs4 object from the html data loaded    
    for link in soup.find_all('a'):
        tmp=str(link.get('href'))
        if tmp.startswith("/title"):
            url="https://www.imdb.com"+tmp
            break
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for s in soup.select('script'):
        s.extract()
    paginapunt=str(soup)[str(soup).find("<div class=\"ratingValue\">")+len("<div class=\"ratingValue\">"):]
    puntuacion=float(paginapunt[len("<strong title=\"")+1:len("<strong title=\"")+4].replace(",","."))
    driver.close()
    return {"Nombre": pelicula,"Puntuacion":puntuacion,"Criticas":[]}