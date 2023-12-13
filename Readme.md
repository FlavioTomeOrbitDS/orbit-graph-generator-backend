# Orbit Graph Data Generator - Backend

<br>

## Descrição do Projeto:


---

O Graph Data Generator é um web app que recebe uma tabela de dados no formato .xlsx do usuário e, em seguida, processa as informações gerando um outro arquivo .xlsx contendo uma tabela com os Vértices, Rótulos e Pesos de um grafo. Essa documentação é referente ao back end, desenvolvido na linguagem Python e com o uso do Framework Flask.

Link do projeto no Google Cloud Run:
```
https://console.cloud.google.com/run/detail/us-central1/graph-generator-backend-v2/metrics?project=orbit-web-apps-hub
```

<br>

## Pré-requisitos:


---



*   Python 3.10.10
*   VS Code 1.76.0 (ou outro editor de código)

<br>

## Como editar o projeto localmente:


---



1. Abra o terminal do VSCode e clone o repositório do projeto do github com o seguinte comando: 
  ```
  git clone https://github.com/FlavioTomeOrbitDS/orbit-graph-generator-backend.git
  ```



2.  Crie e ative um Virtual Enviroment:


*   Um virtual enviroment é utlizado para encapsular o projeto dentro de um ambiente próprio, onde só serão instaladas as bibliotecas necessárias para o funcionanemto da aplicação. Este módulo já vem instado junto com o Python;



*   Dentro do diretório principal do projeto crie um novo ambiente virtual chamado venv com o seguinte comando:   
```
PS ...\orbit-graph-generator-backend>python -m venv venv
```

* Ative o virtual enviroment:
```
  PS ...\orbit-graph-generator-backend>venv\Scripts\activate
```
* Caso o virtual enviroment tenha sido ativado corretamente, o path do projeto no terminal ficará com (venv) logo no início
```
(venv) PS ...\orbit-graph-generator-backend>
```
<br>

3. Com o virtual enviroment ativado, você pode instalar as bibliotecas do projeto:

* A Lista das bibliotecas do projeto está em um arquivo chamado **requirements.txt**. Instale as bibliotecas com o seguinte comando:
```
(venv) PS ...\orbit-graph-generator-backend>pip install -r requirements.txt
```

4. Finalment, assim que todas as bibliotecas forem instaladas, você poderá rodar o backend do Orbit Export Comments:
```
(venv) PS ...\orbit-graph-generator-backend>python app.py
```

5. A API estará disponível em :[ http://localhost:8080](https://)

<br>

## API Endpoints
---
 ### POST: /api/download
1. Payload:<br>
* Recebe um arquivo.xlsx formatado como um Json que será processado dentro de um Dataframe do Pandas.

2. Resposta:
* Como resposta envia um dataframe no formato .xlsx com os dados do Grafo para o front end.

<br>

## Deploy no Google Cloud Plataform
---
O Orbit Export Comments Backend é executado no Google Cloud Run por meio de um container Docker.

Para fazer o deploy no GCP, você deve sergir os seguintes passos:
1.   Criar um projeto no GCP e ativar as API's necessárias. 
2.   Ativar a Cloud Run API.
3.   Criar uma imagem de container Docker do projeto.
4.   Executar o git clone do projeto no Google Cloud.
5.   Fazer o upload da imagem do containder no Google Container Registry.
6.   Fazer o Deploy do container e executá-lo por meio do Google Cloud Run.

<br>

### 1.  Criando um novo projeto do Google Cloud Plataform
Para criar um novo projeto no Google Cloud Platform, siga estes passos:
* Acesse o Console do Google Cloud Platform (https://console.cloud.google.com/).
* Clique no botão "Selecionar Projeto" localizado no canto superior direito da página.
* Clique no botão "Novo Projeto".
* Insira um nome para o projeto.
* (Opcional) Selecione uma organização ou pasta para o projeto.
* Clique no botão "Criar".
* Aguarde alguns instantes enquanto o projeto é criado.
* Uma vez que o projeto esteja pronto, você será redirecionado para a página do Console do Google Cloud Platform com o novo projeto selecionado.  
Para ativar a API do Google Cloud Run 

<br>

### 2. Ativando a Google Cloud API:  
* No menu de navegação, selecione "APIs e Serviços" e clique em "Biblioteca de APIs".  
* Na barra de busca, digite "Cloud Run" e selecione a opção "Cloud Run API".  
* Clique no botão "Ativar".

<br>

### 3. Criando o container Docker do Projeto:  
No diretório raiz do projeto, crie um novo arquivo chamado "Dockerfile".  
Abra o Dockerfile no editor e insira o código a seguir:
```
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]


```
Salve e feche o arquivo.

<br>

### 4. Clonando o projeto no Google Cloud:
* Abra o terminal do GCP e execute o comando git clone [URL do repositório] para clonar o repositório do projeto no github para o Google Cloud. Substitua [URL do repositório] pela URL do repositório que deseja clonar.
* Insira as credenciais de login do Git, se solicitado.
* Use o comando **CD** para navegar até o diretório raiz do projeto no Google Cloud.

<br>

### 5. Fazendo o upload do containder no Google Container Registry.
O Container Registry é um serviço de armazenamento e gerenciamento de containers da Google Cloud Plataform.
Para fazer o upload de um container siga os seguintes passos:
* Certifique-se de que o Docker esteja instalado em sua máquina local.
* Faça o build da imagem do Docker para o Google Container Registry usando o comando:
```
 docker build -t gcr.io/[PROJECT_ID]/[IMAGE_NAME] .

 Exemplo:

 docker build -t gcr.io/orbit-graph-generator/backend .
```
* Realize o Push do container para o Container Registry:
```
 docker push gcr.io/[PROJECT_ID]/[IMAGE_NAME]

 Exemplo:

 docker push gcr.io/orbit-graph-generator/backend 
```


### 6. Realizando o Deploy no Google Cloud Run
* Com a imagem do container já salva no Google Container Registry, basta executar o código a seguir para fazer o deploy do projeto:
```
 gcloud run deploy my-service --image my-image --platform managed 

 Exemplo:

 gcloud run deploy backend --image gcr.io/orbit-graph-generator/backend --platform managed
```
* Após o deploy ter sido realizado com sucesso, basta acessar a URL informada no termial e verificar se aparece a frase "Server Online" no browser.
