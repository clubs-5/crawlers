#import requests
#from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re


header_agent = {
    'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

keyword = input("give me a show name:")
url = 'https://www.rottentomatoes.com/napi/search/all?type=tv&searchQuery={}'.format(keyword)
session = HTMLSession()





# get show's search result html
def fetch():
    
    req = session.get(url, headers = header_agent)
    html = req.html.find('*', first = True)
    html_text = html.text
    
    return html_text


def get_show_page_links(html_text):
    urls = re.findall(r"https://rottentomatoes.com/tv/\w+",html_text)

    return url[0]

def get_seasons_page_html(show_link):
    response = 

#def get_season_rating():

#def get_season_reviews():


html = fetch()
show_link=get_show_page_links(html)


print('==============')
#print(html)
#print('==============')
print(link[0])


#def main():


#if __name__ == '__main__':
#    main()
