import time
import scrapy
from selenium import webdriver
from requests_html import HTMLSession
import pandas as pd
import logging
from tce.pipelines import savingToMysqlPipeline
from .registrando import RegistrandoInformacoes

def parse_date(date_string):

    # Remova os espaços em branco extras e divida a data
    date_parts = date_string.strip().split('/')
    
    # Formato convertido para data DD-MM-YYYY


    formatted_date = f"{date_parts[0]}-{date_parts[1]}-{date_parts[2]}"
    
    return formatted_date


class TceSpider(scrapy.Spider):
    name = "tce"
    allowed_domains = ["tce.sp.gov.br"]
    
    def start_requests(self):
        session = HTMLSession()

        mysql_pipeline = savingToMysqlPipeline()


        try:
            response = session.get("https://www.tce.sp.gov.br/jurisprudencia/")
            response.raise_for_status()  # Raises an HTTPError if the status is not 200

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
            navegador.find_element('xpath','//*[@id="exercicio"]').send_keys('2023,2022')
            navegador.find_element('xpath','/html/body/form/div/div[2]/div[3]/div[9]/div/input[1]').click()

            time.sleep(5)

            mysql_pipeline.create_connection()

            yield scrapy.Request(url=navegador.current_url, callback=self.parse)
        except Exception as e:
            logging.error("Failed to fetch the webpage: %s", e)
    
    def parse(self, response):
        dados = []
    
        for index, doc in enumerate(response.css('.small:nth-child(1) a')):
            doc_text = doc.css('::text').get().strip()
            url = doc.css('::attr(href)').get()
            n_processo = response.css('.small+ .small a ::text')[index].get()
            data_atuacao_raw = response.css('.small:nth-child(3) ::text')[index].getall()
           
            data_atuacao = parse_date(data_atuacao_raw[0]) if data_atuacao_raw else None

            partes = response.css('.small:nth-child(4) ::text')[index].getall() + response.css('.small:nth-child(5) ::text')[index].getall()
            materiaraw = response.css('.small:nth-child(6) ::text')[index].getall()
            materia = materiaraw[0] if materiaraw else None
           
            ementaraw = response.css('.small:nth-child(7) ::text')[index].getall()
            ementa=ementaraw[0] if ementaraw else None

            dados.append({
                "doc": doc_text,
                "Nprocesso": n_processo,
                "dataAtuacao": data_atuacao,
                "partes": partes,
                "materia": materia,
                "url": url,
                "ementa":ementa
            })

            df = pd.DataFrame(dados)
            df.to_excel('dados_tce.xlsx', index=False)
            # info = RegistrandoInformacoes(doc_text, n_processo, data_atuacao, partes, materia, url, ementa)
            # info.salvar_no_banco_de_dados()
