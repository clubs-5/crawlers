from urllib import request
from bs4 import BeautifulSoup
url = 'https://www.imdb.com/feature/genre/?ref_=nv_tv_gr'
res = request.urlopen(url)
soup = BeautifulSoup(res, 'html.parser')
soup1 =soup.select('.ab_ninja')
for t in soup1:
    imageurl = t.select('.image')
    img_url = list(map(lambda x: x.select_one('a'), imageurl))
    for i in img_url:
        res_img = request.urlopen(i.get('href'))
        soup_url = BeautifulSoup(res_img, 'html.parser')
        soup_url1 = soup_url.select('.lister-item mode-advanced')
        print(soup_url1)