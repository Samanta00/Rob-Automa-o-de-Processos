import unittest
from unittest.mock import patch
from scrapy import Item
from test_myspider import MyPipeline
from test_myspider import MyItem
from dataclasses import is_dataclass

class TestMyPipeline(unittest.TestCase):

    def test_if_it_is_a_dataclass(self):
        self.assertTrue(is_dataclass(MyItem))

    def setUp(self):
        self.pipeline = MyPipeline()

    def test_is_valid_date_format_valid(self):
        # Testa se a função is_valid_date_format retorna True para uma data no formato correto
        date_str = '11-05-2024'
        self.assertTrue(self.pipeline.is_valid_date_format(date_str))

    def test_is_valid_date_format_invalid(self):
        # Testa se a função is_valid_date_format retorna False para uma data no formato incorreto
        date_str = '2024-05-11'
        self.assertFalse(self.pipeline.is_valid_date_format(date_str))

    def test_is_valid_valid_item(self):
        # Testa se a função is_valid retorna True para um item válido
        valid_item = {
            'doc': 'Despacho',
            'Nprocesso': '7279/989/24',
            'dataAtuacao': '26-02-2024', 
            'partes': ['FRANCISCO ALVES DA SILVA', 'PREFEITURA MUNICIPAL DE AGU...'],  # Convertido para lista
            'materia': 'ENCAMINHA DOCUMENTO',
            'url': 'https://jurisprudencia.tce.sp.gov.br/arqs_juri/pdf/20008081.pdf',
            'ementa': 'Denúncia referente à fraude de dispensa de...'
        }

        self.assertTrue(self.pipeline.is_valid(valid_item))

    def test_is_valid_missing_fields(self):
        # Testa se a função is_valid retorna False para um item com campos ausentes
        invalid_item = {
            'doc': '123456',
            'Nprocesso': 'FRANCISCO ALVES DA SILVA, PREFEITURA MUNICIPAL DE AGU...	',
            'dataAtuacao': '26-02-2024',
            'materia':'ENCAMINHA DOCUMENTO',
            'url': 'http://example.com',
            'ementa': 'Denúncia referente à fraude de dispensa de... '
        }
        self.assertFalse(self.pipeline.is_valid(invalid_item))

    @patch('builtins.print')
    def test_process_item_invalid(self, mock_print):
        # Testa se a função process_item imprime uma mensagem para um item inválido
        invalid_item = {
            'doc': '123456',
            'Nprocesso': 'FRANCISCO ALVES DA SILVA, PREFEITURA MUNICIPAL DE AGU...	',
            'dataAtuacao': '26-02-2024',
            'materia':'ENCAMINHA DOCUMENTO',
            'url': 'http://example.com',
            'ementa': 'Denúncia referente à fraude de dispensa de... '
        }
        self.pipeline.process_item(invalid_item, None)
        mock_print.assert_called_once_with('Item inválido:', invalid_item)

    # Outros testes podem ser adicionados conforme necessário

if __name__ == '__main__':
    unittest.main()
