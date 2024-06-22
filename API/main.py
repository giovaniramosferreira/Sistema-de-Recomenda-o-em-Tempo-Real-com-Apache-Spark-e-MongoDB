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
