from omdbapi.movie_search import GetMovie
import json
import time
import urllib3
import requests

import pandas as pd
file = input('give me a csv file name only: ')
df  = pd.read_csv('./{}.csv'.format(file))

with open("omdb_all.json4",'w+',encoding='utf-8') as f1:
        n = 0
        for i in df['name']:
            try:
                n += 1
                movie = GetMovie(title=i, api_key='fe65b15e')
                movie_get = movie.get_all_data()
                if "Movie not found!" not in movie_get:
                    data = f1.write(json.dumps(movie_get,ensure_ascii=False,indent=1))
                    print(f' 第 {n} 筆資料爬取 ')
                    time.sleep(0.8)
            except    json.decoder.JSONDecodeError:
                print('jsonDecodeerror')
                continue
            except    requests.exceptions.ConnectionError:
                print('ConnectionError')
                continue
            except   urllib3.connection.HTTPConnection:
                print('HTTPConnection')
                continue
