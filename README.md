![introdução](./assets/intro.png)

# Sistema de Recomendação em Tempo Real com Apache Spark e MongoDB

## 🚀 1 - Introdução 

O projeto foca na geração de recomendações usando o modelo ALS (Alternating Least Squares) da MLlib do Apache Spark. As recomendações serão armazenadas localmente no MongoDB. Uma API será desenvolvida com FastAPI. Além disso, uma aplicação Spark Streaming se conectará a um tópico Kafka para fornecer recomendações em tempo real.


## ⚙️ 2 - Hardware e aplicativos utilizados

Apache Spark: Plataforma de processamento de dados em grande escala.

MLlib: Biblioteca de aprendizado de máquina do Spark.

MongoDB: Banco de dados NoSQL.

FastAPI: Framework para construção de APIs em Python.

Docker: Ferramenta para criação e gerenciamento de containers.
                            
## 📖 3 - Requisitos do Projeto 

1 - Implementar um sistema de recomendação utilizando o modelo ALS do Spark MLlib.
2 - Armazenar as recomendações no MongoDB.
3 - Criar uma API utilizando FastAPI para fornecer recomendações baseadas nas preferencias do usuário.

## 📝4 - Procedimentos e resultados


Configuração do Ambiente:

Vamos utilizar o Docker com as imagens do MongoDB e do Jupyter Notebook.

![...](./assets/docker.png)

Como tenho alguns containers de MongoDB instalados, mudei a porta para a 28017 para evitar conflitos.


Vamos criar uma rede para isso, execute no prompt de comando o seguinte comando

```
docker network create app-tier --driver bridge
```
![...](./assets/rede.png)


depois instale o Jupyter

```
docker pull jupyter/pyspark-notebook
```
![...](./assets/instalacao_jupyter.png)

depois instale o MongoDB

```
docker pull mongo
```

![...](./assets/instalacao_mongo.png)

uma vez que o container com o Jypiter e o Mongo estão rodando, vamos acessar o o jupiter e executar o Script ExemploALS.ipynb

![...](./assets/jupyter.png)

o script acima faz o seguinte:


#### 1 - Importação de Bibliotecas
Nesta célula, são importadas as bibliotecas necessárias para a criação do sistema de recomendação. Também há uma verificação da versão do Python para garantir compatibilidade com a função long.

#### 2 - Configuração da Sessão Spark
Cria uma sessão do Spark e configura a conexão com um banco de dados MongoDB.

#### 3 - Leitura e Processamento dos Dados
Lê um arquivo de texto com avaliações de filmes e transforma essas avaliações em um DataFrame do Spark.

#### 4 - Divisão dos Dados
Divide os dados em conjuntos de treinamento e teste, sendo 80% e 20% respectivamente.

#### 5 - Treinamento do Modelo
Configura e treina um modelo de recomendação ALS (Alternating Least Squares) usando o conjunto de treinamento.

#### 6 - Avaliação do Modelo
Transforma os dados de teste com o modelo treinado e avalia a precisão do modelo usando o RMSE (Root Mean Square Error).

#### 7 - Recomendação para Usuários
Gera recomendações de filmes para todos os usuários e exibe as primeiras 10 recomendações.

#### 8 - Recomendação para Itens (Filmes)
Gera recomendações de usuários para todos os filmes e exibe as primeiras 20 recomendações.

#### 9 - Seleção de Recomendação por IDs de Filmes
Seleciona apenas os IDs dos filmes recomendados para os usuários.

#### 10 - Salvando as Recomendações no MongoDB
Salva as recomendações geradas no MongoDB.


Depois da execução do script de treinamento do modelo e inserção das recomendações no MongoDB, vamos utilizar o MongoDBCompass para verificar is itens inseridos:

![...](./assets/Mongo.png)


![...](./assets/Recomendacoes.png)


### 10 - Criação da API utilizando Fast API

Primeiro, vamos criar um script python para realizar consultas em nosso MongoDB

para isso, precisamos instalar os requerimentos com esse executando o arquivo requirements:

```
fastapi==0.68.0
uvicorn==0.15.0
pymongo==3.12.0

```

o script será esse:

```
from pymongo import MongoClient

def inicia_conexao():

    client = MongoClient("localhost", 28017)
    db = client['puc']
    col = db.recomendacoes
    return col

def consulta_recomendacoes(usuario, conexao):
    recomendacoes = list(conexao.find({"userId": usuario}))
    list_rec = []
    for rec in recomendacoes:
        list_rec.append({'id': rec['movieId'], 'rating': rec['rating']})
    return list_rec



conn = inicia_conexao()
print(consulta_recomendacoes(28,conn))
```

Este script Python conecta-se a um banco de dados MongoDB, especificamente à coleção "recomendacoes" dentro do banco "puc" em um servidor. Ele contém uma função para iniciar essa conexão e outra para consultar as recomendações de filmes de um usuário específico, identificado pelo campo userId. A consulta retorna uma lista de dicionários contendo movieId e rating das recomendações do usuário.


agora estamos prontos para criar nossa API utilizando FastAPI. para isso, vamos executar o seguinte script:

```
from fastapi import FastAPI
import uvicorn
from bd import mongo
from typing import List

app = FastAPI()
conexao = mongo.inicia_conexao()

@app.get("/rec/v1")
def rota_padrao():
    return {"Rota padrão": "Você acessou a rota default"}

@app.get("/rec/v2/{usuario}")
def consulta_rec(usuario: int):
    return {"usuario": usuario, "resultado_recs": mongo.consulta_recomendacoes(usuario, conexao)}

## Criar um terceiro , rodando mais de um usuário e retornando somente os Ids dos filmes

@app.post("/rec/v3/")
def consulta_multi_recs(usuarios: List[int]):
    results = {}
    for usuario in usuarios:
        recs = mongo.consulta_recomendacoes(usuario, conexao)
        # Extract only the movie IDs
        movie_ids = [rec['id'] for rec in recs]
        results[usuario] = movie_ids
    return results

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)

```

Este script define uma aplicação web usando FastAPI que se conecta a um banco de dados MongoDB para fornecer recomendações de filmes. Ele possui três rotas: a primeira retorna uma mensagem padrão, a segunda consulta recomendações para um único usuário especificado e a terceira recebe uma lista de usuários e retorna apenas os IDs dos filmes recomendados para cada um. A aplicação é executada localmente usando o servidor uvicorn.

![...](./assets/api.png)


quando executamos a terceira rota, passamos uma lista de usuários e os Ids dos filmes recomendados são retornados:

![...](./assets/api2.png)


## 📋5 - Conclusão

A execução deste projeto permitiu a implementação de um sistema de recomendação robusto utilizando diversas tecnologias de big data e aprendizado de máquina. O uso do modelo ALS do Spark MLlib proporcionou recomendações eficazes, e o armazenamento no MongoDB garantiu uma recuperação rápida dos dados. A API desenvolvida com FastAPI facilitou o acesso às recomendações, enquanto a integração com Kafka e Spark Streaming permitiu o fornecimento de recomendações em tempo real.