import scrapy
import pandas as pd

class TceSpider(scrapy.Spider):
    name = "tce"
    allowed_domains = ["tce.sp.gov.br"]
    start_urls = ["https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+escolas&txtExp=&txtQqUma=&txtNenhPalvs=&txtNumIni=&txtNumFim=&tipoBuscaTxt=Documento&_tipoBuscaTxt=on&quantTrechos=1&processo=&exercicio=2023%2C2022&dataAutuacaoInicio=&dataAutuacaoFim=&dataPubInicio=&dataPubFim=&_relator=1&_auditor=1&_materia=1&_tipoDocumento=1&acao=Executa"]

    def parse(self, response):
        dados = []
    
        for index, doc in enumerate(response.css('.small:nth-child(1) a')):
            doc_text = doc.css('::text').get().strip()
            url = doc.css('::attr(href)').get()
            n_processo = response.css('.small+ .small a ::text')[index].get()
            data_atuacao = response.css('.small:nth-child(3) ::text')[index].getall()
            partes = response.css('.small:nth-child(4) ::text')[index].getall() + response.css('.small:nth-child(5) ::text')[index].getall()
            materia = response.css('.small:nth-child(6) ::text')[index].getall()

            dados.append({
                "doc": doc_text,
                "Nprocesso": n_processo,
                "dataAtuacao": data_atuacao,
                "partes": partes,
                "materia": materia,
                "url": url,
            })

        df = pd.DataFrame(dados)
        df.to_excel('dados_tce.xlsx', index=False)
