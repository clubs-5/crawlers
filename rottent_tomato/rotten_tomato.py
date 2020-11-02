#import requests
#from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
import json


show_name = input("give me a show name:")

header_agent = {
    'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

session = HTMLSession()


def main():
    url_tomato = 'https://www.rottentomatoes.com/napi/search/all?type=tv&searchQuery={}'.format(show_name)
    query_response =  establish_session(url_tomato)
    stuff = {}

    while query_response.status_code == 200:
        
        result_html = fetch_page_html(query_response)
        show_main_page_url = get_show_main_page_link(result_html)
        
        season = 1
        season_main_page_url = show_main_page_url + '/s{}'.format(season)
        while establish_session(season_main_page_url).status_code == 200:
            page = 1
            info = get_season_infos(season_main_page_url)
            

            reviews_page_link_by_season = season_main_page_url + '/reviews?type=&sort=&page={}'.format(page)
            review_page_html = get_seasons_reviews_page_html(reviews_page_link_by_season)
        
            extract_reviews(review_page_html)

            page += 1

        
        #data = {}
       
        #if establish_session(season_main_page).status_code == 200:


        

        
    
     
   





def establish_session(url):
    response = session.get(url, headers = header_agent)

    return response


# get show's search result html
def fetch_page_html(res):
    
    code = res.status_code
    if code == 200:
        #html = res.html.find('*', first = True)
        html = res.html
        return html

    else:
        return 'Non 200'

def get_show_main_page_link(html):
    s = html.text
    urls = re.findall(r"https://rottentomatoes.com/tv/\w+", s)

    return urls[0]

def get_season_infos(season_main_page_link):
    '''
    This function will take TV Show's season info and output them in json format
    '''
    info = {'Year':'','consensus':'', 'Critic_Ratings':'','tomatometer':'', 'User_ratings':'', 'audience_score':''}

    html = establish_session(season_main_page_link).html

    select_year = html.find('#tv_title_headers > h1 > span')
    year = select_year[0].text

    select_consensus = html.find('#topSection > div.tv-season-top-section__ratings-group > div > section > div.mop-ratings-wrap.score_panel.js-mop-ratings-wrap > section > p')
    consensus = select_consensus[0].text

    select_tomato = html.find('#tomato_meter_link > span.mop-ratings-wrap__percentage')
    tomatometer = select_tomato[0].text
    
    select_critics = html.find('#topSection > div.tv-season-top-section__ratings-group > div > section > div.mop-ratings-wrap.score_panel.js-mop-ratings-wrap > section > section > div.mop-ratings-wrap__half.critic-score > div > small')
    critic_ratings = select_critics[0].text

    select_users = html.find('#topSection > div.tv-season-top-section__ratings-group > div > section > div.mop-ratings-wrap.score_panel.js-mop-ratings-wrap > section > section > div.mop-ratings-wrap__half.audience-score > div > strong')
    user_ratings = select_users[0].text

    select_audience = html.find('#topSection > div.tv-season-top-section__ratings-group > div > section > div.mop-ratings-wrap.score_panel.js-mop-ratings-wrap > section > section > div.mop-ratings-wrap__half.audience-score > h2 > a > span.mop-ratings-wrap__percentage')
    audience_score = select_audience[0].text

    info['Year'] = year
    info['consensus'] = consensus
    info['Critic_Ratings'] = int(critic_ratings)
    info['tomatometer'] = int(re.findall(r'\d+',tomatometer)[0])
    info['User_ratings'] = int(re.findall(r'\d+',user_ratings)[0])
    info['audience_score'] = int(re.findall(r'\d+',audience_score)[0])
    

    return info
    


def get_seasons_reviews_page_html(url):
    
    html = establish_session(url).html
    return html

def extract_reviews(page_html):
    review_content = page_html.find('.critic__review-quote' )
    review_obj = {'name':'', 'org':'', 'content':''}
    for i in review_content:
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
