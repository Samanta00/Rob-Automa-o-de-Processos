import logging
import time
from selenium import webdriver
import scrapy
from requests_html import HTMLSession
from tce.pipelines import SavingToMysqlPipeline
from .utils import parse_date


class TceSpider(scrapy.Spider):
    name = "tce"
    allowed_domains = ["tce.sp.gov.br"]

    def start_requests(self):

        #utilização da biblioteca requests_html para verificar se site está acessível
        session = HTMLSession()
        mysql_pipeline = SavingToMysqlPipeline()

    # o código vai tentar a conexão ao site
        try:
            response = session.get("https://www.tce.sp.gov.br/jurisprudencia/")
            response.raise_for_status()  # Gera um HTTPError se o status não for 200

            title = response.html.find("title", first=True).text
            url = response.url

            logging.info("Application title is %s", title)
            logging.info("Application URL is %s", url)

           # código para o robô entrar na página desejada
            navegador = webdriver.Chrome()
            navegador.maximize_window()
            navegador.get("https://www.tce.sp.gov.br/jurisprudencia/")
            logging.info("Application title is %s", navegador.title)
            logging.info("Application URL is %s", navegador.current_url)

            navegador.find_element('xpath', '/html/body/form/div/div[2]/div[2]/div[1]/div/input').send_keys('fraude em escolas')
            navegador.find_element('xpath', '//*[@id="exercicio"]').send_keys('2023,2022')
            navegador.find_element('xpath', '/html/body/form/div/div[2]/div[3]/div[9]/div/input[1]').click()

            time.sleep(2)

            mysql_pipeline.create_connection()

            yield scrapy.Request(url=navegador.current_url, callback=self.parse)
        except Exception as e:
            logging.error("Failed to fetch the webpage: %s", e)

    #função para extração de dados da página
    def parse(self, response):
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
            ementa = ementaraw[0] if ementaraw else None

            #criar um objeto com os valores extraidos da página 
            item = {
                "doc": doc_text,
                "Nprocesso": n_processo,
                "dataAtuacao": data_atuacao,
                "partes": partes,
                "materia": materia,
                "url": url,
                "ementa": ementa
            }
            # Criação de uma instância do pipeline
            pipeline = SavingToMysqlPipeline()

            # Processando o item individualmente para enviar ao banco de dados
            pipeline.process_item(item, None)

