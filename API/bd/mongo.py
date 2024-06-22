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

