from tce.pipelines import savingToMysqlPipeline;


class RegistrandoInformacoes:
    def __init__(self,doc,Nprocesso,dataAtuacao,partes,materia,url,ementa) -> None:
        self.doc=doc,
        self.Nprocesso=Nprocesso,
        self.dataAtuacao=dataAtuacao,
        self.partes=partes,
        self.materia=materia,
        self.url=url,
        self.ementa=ementa

    def salvar_no_banco_de_dados(self):

        pipeline = savingToMysqlPipeline()
        
        item = {
            "doc": self.doc,
            "Nprocesso": self.Nprocesso,
            "dataAtuacao": self.dataAtuacao,
            "partes": self.partes,
            "materia": self.materia,
            "url": self.url,
            "ementa":self.ementa
        }

        # Passar o item para o pipeline para salvá-lo no banco de dados
        pipeline.process_item(item, None)