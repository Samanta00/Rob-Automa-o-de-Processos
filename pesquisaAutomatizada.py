from selenium import webdriver
from requests_html import HTMLSession


session = HTMLSession()
response = session.get("https://www.tce.sp.gov.br/jurisprudencia/")


if response.status_code == 200:
    title = response.html.find("title", first=True).text
    url = response.url

    print("Application title is", title)
    print("Application URL is", url)

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.tce.sp.gov.br/jurisprudencia/")
    print("Application title is", driver.title)
    print("Application URL is", driver.current_url)
else:
    print("Failed to fetch the webpage")




