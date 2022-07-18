import json
import os
import time
from tweepy import Stream
from decouple import config
from datetime import datetime


class MyListener(Stream):
    def on_data(self, raw_data):
        out.write(json.dumps(json.loads(raw_data)) + "\n")
        return super().on_data(raw_data)

if __name__ == '__main__':

    # Carregando as Keys do arquivo .env
    API_KEY=config('API_KEY')
    API_KEY_SECRET=config('API_KEY_SECRET')
    ACCESS_TOKEN=config('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET=config('ACCESS_TOKEN_SECRET')

    # Criando pasta que vai receber os tweets e os arquivos txt
    os.makedirs('data', exist_ok=True)
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    out = open(f'data/tweets-{now}.txt', 'w', encoding='UTF-8')
    # Executando o Listener pra obter tweets da Ucrânia por 5 segundos.s
    stream = MyListener(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream.filter(track=['python'], threaded=True)