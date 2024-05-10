from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.tce.sp.gov.br/jurisprudencia/")
print("Application title is", driver.title)
print("Application URL is", driver.current_url)
driver.quit()
