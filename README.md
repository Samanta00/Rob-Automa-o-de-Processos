
<p align="center">
  <img src="https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/020eb26a-5ca9-4464-b50f-a3f8d7986260" width="320">
</p>


# Robô de Automação de Processos (RPA) para extração de dados.
## Objetivo
#### Desenvolver um robô de automação de processos utilizando Python e as bibliotecas requests_html, Selenium e Scrapy. O candidato deverá demonstrar habilidades em navegação web, extração de dados e manipulação de informações, utilizando essas ferramentas.


## Requisitos:
#### Utilizar biblioteca requests-html para raspagem de dados para fazendo o scraping do site e extrair os dados necessários. 
#### Priorizar performance na raspagem dos dados.
#### Extrair e salvar os dados em um banco de dados (MySQL)
#### A modelagem da tabela no banco de dados está otimizada para recuperação de informação baseada em data, matéria e Doc, ou seja através de id, ou seja, chave primaria.
#### O código está pensado de modo a ser colocado em ambiente de produção, isto é com variaveis de ambiente localizadas em arquivos de separados (no caso é o arquivo: .env)
#### Código está bem Documentado e estruturado, também utilizando melhores práticas de commits explicando a lógica por trás das ações realizadas.
#### os algoritmos estão seguindo as boas práticas de PEP8
#### Para um ambiente bem organizado a arquitetura do software está sendo envolvida por docker
#### o código tem testes funcionais


## Let's GO

## Como usar?

![image](https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/85f84463-b013-4832-90fe-e6b158c1289f)

### Copie esse link e clone esse repositório no seu ambiente de desenvolvimento, atenção, antes de realizar essa ação é importante que seu embiente esteja adequado para poder clonar repositórios do github

### você vai fazer dessa forma:
![image](https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/4e3141d5-28f1-4d66-a648-2f051c173541)


### o projeto vai se abrir e arquitetura original dele é essa:
![image](https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/f2a58291-7ca8-45cc-9bb0-e4eb84141480)

### note que existem arquivos .env, esse arquivo é onde será configurada a estrutura de conexão com o banco de dados, porém como essa conexão é realizada pelo docker você só precisa mudar a senha para uma mais forte, caso você deseje

### se você fizer a alteração em 1 arquivo .env, você precisa ajustar a mesma configuração para todos os outros arquivos .env

![image](https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/d8292d4e-5771-434a-8c2e-ae5efb4d3b65)



### Ótimo, já temos nosso arquivo .env configurado, agora vamos iniciar nosso container docker para executar a conexão ao banco de dados

### Localize a pasta docker e executa o seguinte comando pelo terminal: docker-compose up --build

### Se tudo ocorrer bem, você terá algo semelhante a isso:

![image](https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/ac70e539-e1e7-4bec-b1c4-1ad2e9573693)

### Ótimo, já temos nosso ambiente docker rodando, precisamos ter uma visualização do banco de dados então baixe a seguinte extensão para melhorar a sua experiência

![image](https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/597d98e3-6e49-4336-a4fb-99426b3d26e9)

### execute a extensão e crie a sua conexão com o banco de dados, você pode criar da seguinte forma 
![image](https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/445f52bf-c4d1-424d-9f9f-dc5f0b1333e9)

### note que eu estou mostrando apenas um exemplo, na sua conexão com a extensão você vai colocar as informações que estão nos seus arquivos .env

### feito isso, você terá já uma visualização de como está o seu banco de dados e todas as tabelas registradas dentro dele, vamos executar o código

### Localize a sua pasta tce e execute esse comando: scrapy crawl tce

### Se tudo ocorrer bem, você terá algo semelhante a isso:

![image](https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/2c3a4891-68a2-4899-aaa4-b84c53d7fa5e)


### Parabéns você já executou o código quase por completo, vamos analisar agora se as informações foram salvas

### se você analisar bem, após executar o código, um arquivo json foi criado, nele está contido todos os registros que o robÔ conseguiu capturar da página mas vamos analisar se isso foi salvo no banco de dados

### se ao abrir a extensão o banco permanecer vázio, dê um refresh, e selecione todos os registros da tabela, bem, eu consegui obter o seguinte resultado

![image](https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/f1309bc7-c5b8-4ad5-8458-9671dd7f7a40)

## Inicianos os Testes funcionais:

### Encontre a sua pasta testes e execute o seguinte comando: python3 main_test.py
### você terá algo semelhante a isso:
![image](https://github.com/Samanta00/Robo-Automatizador-de-Processos/assets/80990432/e8d54797-063c-4ae0-b9f2-a0b9f59234d5)


### Ao chegar no final do arquivo, você verá que 6 testes foram executados e todos foram rodados sem nenhum erro, pois os testes vão executar:

----------------------------------------------------------------------
Ran 6 tests in 0.040s

OK

### Ótimo, e quais testes foram executados?

### o arquivo test_myspider.py vai fazer um teste de conexão com o banco de dados e vai verificar se todos os valores que chegarem nele estão preenchidos e formatados ao que é esperado, se tiver tudo certo ele retorna true, se não tiver ele retorna false

### o arquivo main_test.py vai testar se o valor de data está no formato '11-05-2024'

### vai testar se todos os outros itens estão adequados ou se estão ausentes e também presentes para o envio ao banco de dados e no formato padrão de
   ##### {
   #####             'doc': 'Despacho',
   #####             'Nprocesso': '7279/989/24',
   #####             'dataAtuacao': '26-02-2024', 
   #####             'partes': ['FRANCISCO ALVES DA SILVA', 'PREFEITURA MUNICIPAL DE AGU...'],  # Convertido para lista
   #####             'materia': 'ENCAMINHA DOCUMENTO',
   #####             'url': 'https://jurisprudencia.tce.sp.gov.br/arqs_juri/pdf/20008081.pdf',
   #####             'ementa': 'Denúncia referente à fraude de dispensa de...'
   ##### }

### Contudo Testa se a função process_item imprime uma mensagem para um item inválido


## Bom, o projeto chegou ao fim, espero que tenha gostado :)



