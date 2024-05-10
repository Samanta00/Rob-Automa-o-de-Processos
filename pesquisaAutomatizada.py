import time

from selenium import webdriver
from requests_html import HTMLSession


session = HTMLSession()
response = session.get("https://www.tce.sp.gov.br/jurisprudencia/")


if response.status_code == 200:
    title = response.html.find("title", first=True).text
    url = response.url

    print("Application title is", title)
    print("Application URL is", url)

    navegador = webdriver.Chrome()
    navegador.maximize_window()
    navegador.get("https://www.tce.sp.gov.br/jurisprudencia/")
    print("Application title is", navegador.title)
    print("Application URL is", navegador.current_url)

    navegador.find_element('xpath','/html/body/form/div/div[2]/div[2]/div[1]/div/input').send_keys('fraude em escolas')

    navegador.find_element('xpath','/html/body/form/div/div[2]/div[3]/div[9]/div/input[1]').click()

    time.sleep(50)
else:
    print("Failed to fetch the webpage")




