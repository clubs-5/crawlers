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

    if query_response.status_code == 200:
        
        result_html = fetch_page_html(query_response)
        show_main_page_url = get_show_main_page_link(result_html)
        
        season = 1
        season_main_page_url = show_main_page_url + '/s{}'.format(season)
        page = 1
       
        while establish_session(season_main_page_url).status_code == 200:
            
            print(season)
            
            check_prerelease = check_pre(season_main_page_url)
            name = []
            org = []
            content =[]
            reviews = []
            page = 1

            if not check_prerelease:
                info = get_season_infos(season_main_page_url)
                reviews_page_link_by_season = season_main_page_url + '/reviews?type=&sort=&page={}'.format(page)
                review_page_html = get_seasons_reviews_page_html(reviews_page_link_by_season)
                check = check_no_reviews(review_page_html)
                
                
                while check :
            
                    #print('###################')
                    #print('@@@@@@@@@@@@@')
                    #print(reviews_page_link_by_season)
                    extract_reviews(review_page_html,name,org,content)
                    #x = extract_reviews(review_page_html)
                    #reviews = reviews.extend(x)
                
                    page += 1
                    reviews_page_link_by_season = season_main_page_url + '/reviews?type=&sort=&page={}'.format(page)
                    review_page_html = get_seasons_reviews_page_html(reviews_page_link_by_season)
                    check = check_no_reviews(review_page_html)

                for i in range(len(name)):
                    review_keys = ['name', 'org', 'content']
                    value = [name[i], org[i], content[i]]

                    review_obj = dict(zip(review_keys,value))

                    reviews.append(review_obj)




                info['Season'] = season
                info['Reviews'] = reviews
                info['Reviews'] = reviews
                print(info)
              

            season += 1
            season_main_page_url = show_main_page_url + '/s{}'.format(season)
                

    






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

def check_pre(season_main_page_link):
    html = establish_session(season_main_page_link).html

    select_prerelease = html.find('.mop-ratings-wrap__prerelease-text')
    
    return select_prerelease


def get_season_infos(season_main_page_link):
    '''
    This function will take TV Show's season info and output them in json format
    '''
    info = {'Year':'', 'Season':'', 'User_ratings':'', 'audience_score':'', 'Critic_Ratings':'', 'tomatometer':'', 'consensus':'', 'Reviews':[]}

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
    info['Critic_Ratings'] = critic_ratings
    info['tomatometer'] = int(re.findall(r'\d+',tomatometer)[0])
    info['User_ratings'] = int(re.findall(r'\d+',user_ratings)[0])
    info['audience_score'] = int(re.findall(r'\d+',audience_score)[0])
    

    return info
    


def get_seasons_reviews_page_html(url):
    
    html = establish_session(url).html
    return html

def extract_reviews(page_html,x,y,z):

    review_content = page_html.find('.critic__review-quote' )
    critic_name = page_html.find('.critic__name')
    critic_org = page_html.find('.critic__publication')
   
    
   
    name_list = x
    org_list = y
    content_list = z

    
    for name in critic_name:
        
        name_list.append(name.text)
        
    
    for org in critic_org:
        org_list.append(org.text)

    for content in review_content:
        content_list.append(content.text)
    

        #for review in reviews:
        #    review['org'] = 

    '''
    for review in reviews:
        while review:
            review['org'] = org.text
    for content in review_content:
        for review in reviews:
            review['content'] = content.text
    '''

    
        
          
               

def check_no_reviews(html):
    check = html.find('.critic__review-quote')
    return check

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
