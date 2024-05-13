import scrapy
import datetime
from dataclasses import dataclass
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()
from scrapy.crawler import CrawlerProcess

@dataclass()
class MyItem(scrapy.Item):
    doc : str
    Nprocesso : str
    dataAtuacao : str
    partes : list
    materia : str
    url : str
    ementa : str

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['http://example.com']

    def parse(self, response):
        item = MyItem(  # Corrigindo a criação do objeto MyItem
            doc='Despacho',
            Nprocesso='7279/989/24',
            dataAtuacao='26-02-2024',
            partes=['FRANCISCO ALVES DA SILVA', 'PREFEITURA MUNICIPAL DE AGU...'],  # Usando tupla em vez de lista
            materia='ENCAMINHA DOCUMENTO',
            url='https://jurisprudencia.tce.sp.gov.br/arqs_juri/pdf/20008081.pdf',
            ementa='Denúncia referente à fraude de dispensa de...'
        )
        yield item

class MyPipeline:
    def __init__(self):
     
        self.connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port= os.getenv('MYSQL_PORT', '3307'),
            database=os.getenv('MYSQL_DATABASE'),
            username='root',
            password=os.getenv('MYSQL_PASSWORD')
        )


    def save_to_mysql(self, item):
        try:
            cursor = self.connection.cursor()

            # Exemplo de comando SQL para inserir dados em uma tabela fictícia chamada 'items'
            sql = "INSERT INTO items (doc, Nprocesso, dataAtuacao, partes, materia, url, ementa) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (
                item['doc'],
                item['Nprocesso'],
                item['dataAtuacao'],
                item['partes'],
                item['materia'],
                item['url'],
                item['ementa']
            )

            cursor.execute(sql, values)
            self.connection.commit()

            print("Item salvo no MySQL:", item)
        except mysql.connector.Error as error:
            print("Erro ao salvar no MySQL:", error)


    def process_item(self, item, spider):
        if self.is_valid(item):
            self.save_to_mysql(item)
        else:
            print("Item inválido:", item)
            return None  # Interrompe o processamento do item se for inválido
        return item


    def is_valid(self, item):
        # Verifica se o campo dataAtuacao está no formato correto DD-MM-YYYY
        if not self.is_valid_date_format(item['dataAtuacao']):
            return False

        # Verifica se os campos doc e Nprocesso estão preenchidos
        if not item.get('doc'):
            return False
        
        if not item.get('Nprocesso'):
            return False
        # Verifica se a URL está vazia
        if not item.get('url'):
            return False

        # Verifica se partes, materia e ementa não estão vazios
        if not item.get('partes'):
            return False
            
        if not item.get('materia'):
            print('erro 5')
            return False
            
        if not item.get('ementa'):
            return False

        return True



    def is_valid_date_format(self, date_str):
        try:
            # Verifica se a data está no formato DD-MM-YYYY
            datetime.datetime.strptime(date_str, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def save_to_mysql(self, item):
        # Implemente a lógica para salvar o item no MySQL aqui
        print("Salvando no MySQL:", item)

# Iniciar o processo de rastreamento
process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(MySpider)
process.start()
