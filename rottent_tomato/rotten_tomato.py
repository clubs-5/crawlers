#import requests
#from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
import json

header_agent = {
    'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

show_name = input("give me a show name:")
url_tomato = 'https://www.rottentomatoes.com/napi/search/all?type=tv&searchQuery={}'.format(show_name)
session = HTMLSession()


def main():
    response =  establish_session(url_tomato)

    if response.status_code == 200:
        
        result_html = fetch_page_html(response)
        show_main_page_link = get_show_main_page_link(result_html)
        season_main_page = show_main_page_link + '/s1'
        reviews_page_link_by_season = show_main_page_link + '/s1/reviews?type=&sort=&page=1'
        review_page_html = get_seasons_reviews_page_html(reviews_page_link_by_season)
        
        extract_reviews(review_page_html)

        print('-----------')
        #data = {}
        season_n = 1
        season_main_page = show_main_page_link + '/s{}'.format(season_n)
        #if establish_session(season_main_page).status_code == 200:

        test = get_season_infos(season_main_page)

        print(test)

        '''
        year = 
        genre = 
        network = 
        season_number =
        consensus = 
        tomatometer = 
        critic_ratings = 
        user_ratings = 
        
        critic_name = 
        top_critic =        
        critic_org = 
        critic_content = 
        '''
        
    
     
   





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
    info = {'consensus':'', 'Critic_Ratings':'','tomatometer':'', 'User_ratings':'', 'audience_score':''}

    html = establish_session(season_main_page_link).html
    select_consensus = html.find('#topSection > div.tv-season-top-section__ratings-group > div > section > div.mop-ratings-wrap.score_panel.js-mop-ratings-wrap > section > p')
    consensus = select_consensus[0].text

    select_tomato = html.find('mop-ratings-wrap__percentage')
    print(select_tomato)
    tomatometer = select_tomato[0].text
    
    select_critics = html.find('mop-ratings-wrap__text--small')
    critic_ratings = select_critics[0].text

    select_users = html.find('mop-ratings-wrap__text--small')
    user_ratings = select_users[0].text

    info['consensus'] = consensus
    info['Critic_Ratings'] = critic_ratings
    info['tomatometer'] = tomatometer
    info['User_ratings'] = user_ratings
    

    return info
    


def get_seasons_reviews_page_html(url):
    
    html = establish_session(url).html
    return html

def extract_reviews(page_html):
    review_content = page_html.find('.critic__review-quote' )
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
