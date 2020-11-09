from omdbapi.movie_search import GetMovie
import json
import time

import pandas as pd
file = input('give me a csv file name only: ')
df  = pd.read_csv('./{}.csv'.format(file))

with open("omdb_all.json",'w',encoding='utf-8') as f1:
    n = 0
    for i in df['name']:
        n += 1
        movie = GetMovie(title=i, api_key='1368be7b')
        movie_get = movie.get_all_data()
        if "'Movie not found!'" not in movie_get:
            f1.write(json.dumps(movie_get,ensure_ascii=False,indent=1))
            print(f'第 {n} 筆資料正在爬取')