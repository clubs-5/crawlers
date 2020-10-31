#import requests
#from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re


header_agent = {
    'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

keyword = input("give me a show name:")
url_tomato = 'https://www.rottentomatoes.com/napi/search/all?type=tv&searchQuery={}'.format(keyword)
session = HTMLSession()


def main():
    response_code =  establish_session(url_tomato)
    result_html_text = fetch_shows_search_page_html(response_code)
    show_main_page_link = get_show_main_page_link(result_html_text)
    reviews_page_link_by_season = show_main_page_link + '/s1/reviews'
    review_page_html = get_seasons_reviews_page_html(reviews_page_link_by_season)

    
    print(review_page_html)





def establish_session(url):
    response = session.get(url, headers = header_agent)

    return response


# get show's search result html
def fetch_shows_search_page_html(res):
    code = res.status_code
    if code == 200:
        html = res.html.find('*', first = True)
        html_text = html.text
        return html_text

    else:
        return 'Non 200'

def get_show_main_page_link(s):
    urls = re.findall(r"https://rottentomatoes.com/tv/\w+", s)

    return urls[0]

def get_seasons_reviews_page_html(url):
    
    html = establish_session(url).html.find('.critic__review-quote' )
    for i in html:
        print(i.text)

#def get_season_rating():

#def get_season_reviews():
'''
response =  establish_session(url_tomato)
result_html_text = fetch_shows_search_page_html(response)
show_main_page_link = get_show_main_page_link(result_html_text)
    
print(show_main_page_link)
'''

if __name__ == '__main__':
    main()
