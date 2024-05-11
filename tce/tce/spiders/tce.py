import scrapy


class TceSpider(scrapy.Spider):
    name = "tce"
    allowed_domains = ["tce.com"]
    start_urls = ["https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+escolas&txtExp=&txtQqUma=&txtNenhPalvs=&txtNumIni=&txtNumFim=&tipoBuscaTxt=Documento&_tipoBuscaTxt=on&quantTrechos=1&processo=&exercicio=2023%2C2022&dataAutuacaoInicio=&dataAutuacaoFim=&dataPubInicio=&dataPubFim=&_relator=1&_auditor=1&_materia=1&_tipoDocumento=1&acao=Executa"]

    def parse(self, response):
        for doc in response.css('.small:nth-child(1) a::text').getall():
            yield{
                "doc" : doc,
                "Nprocesso" : response.css('.small+ .small a::text').getall(),
                "dataAtuacao" : response.css('.small:nth-child(3) ::text').getall(),
                "partes" : response.css('.small:nth-child(4) ::text').getall(),
                "materia" : response.css('.small:nth-child(6) ::text').getall(),
            }
        

    



        pass
