import requests as re
import pandas as pd
import redis
import json

#conexao com redis.
#colocar o host, port, password criada ao criar uma database no site https://app.redislabs.com/#/login ou inserindo as informações de localhost
redis_client = redis.Redis(host="", port=123, db=0, password="")
data = redis_client.get('df')

#se os dados não forem vazios, pegar dados no redis, senao buscar na aplicacao na aplicacao
if data:
    result = json.loads(data)
    ranking = pd.json_normalize(result)
    print(ranking.sort_values(['score', 'bonus'], ascending=False))
else:
    url = "https://87dyrojjxk.execute-api.us-east-1.amazonaws.com/dev/fiap/ranking?skip=1&take=20"
    api_rank_geral = re.get(url)
    json_data = api_rank_geral.json()
    json_dump = json.dumps(json_data['results'])
    redis_client.setex('df', 100, json_dump)
    data = redis_client.get('df')
    result = json.loads(data)
    ranking = pd.json_normalize(result)
    print(ranking.sort_values(['score', 'bonus'], ascending=False))