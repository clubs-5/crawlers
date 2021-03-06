from requests_html import HTMLSession
import re
import json
import os
import pandas as pd 
import time
import random

csv_file_name = input('Give me a csv file name without extension: ')
df = pd.read_csv('./{}.csv'.format(csv_file_name))
show_list = df.name.to_list()
#ip_csv = input('Give me a ip csv file a,b,c or d: ')
# dd = pd.read_csv('./ip_list.csvaa')
# ip_list = dd.ip.to_list()

header_agent = {
    'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}
session = HTMLSession()

def main():
    n = 0
    for show_name in show_list:
        start_time = time.time()
        print(show_name)
        sleep_time = random.randint(1,3)
        
        url_tomato = 'https://www.rottentomatoes.com/napi/search/all?type=tv&searchQuery={}'.format(show_name)
        

        #print('checking proxy')
        #proxy_results = check_proxy(url_tomato)
        #print('Done checking proxy')
        #query_response =  proxy_results[0]
        #proxy = proxy_results[1]
        while True:
            try :
                print('Connecting to {}'.format(url_tomato))
                query_response = establish_session(url_tomato)
                print('Not banned yet!')
                if query_response.status_code == 200:
                    result_html = fetch_page_html(query_response)
                    show_main_page_url = get_show_main_page_link(result_html)
                    if not show_main_page_url:
                        print('Empty URL')
                        pass
                    else:
                        try:
                            # print('gg')
                            with open('results_{}.json'.format(csv_file_name),'a') as obj:
                                print('Working on it now...')
                                info_dict = show_full_info(show_main_page_url, show_name)
                                info_json_string = json.dumps(info_dict)
                                obj.write(info_json_string)
                                obj.close() # doesn't need to use close method
                        except:
                            # print('some exception')
                            # pass
                            with open('failed.txt', 'a') as f:
                                print('Nothing in here ...{}'.format(show_name))
                                f.write('{}\n'.format(show_name))
                                f.close # doesn't need to use close method
                            
                else:
                    pass
                print('Wait {} seconds'.format(sleep_time))
                time.sleep(sleep_time)
                session.close
                n += 1
                print('{} Shows processed'.format(n))
                elapsed_time = round(time.time() - start_time,1)
                print('{} seconds elapsed'.format(elapsed_time))
                break
                
            except:
                print("Taking a break from Rotten Tomato. Will resume in 5 mins")
                time.sleep(300)
                print('Resuming...')


def show_full_info(show_main_page_url, show_name):

    
    stuff = {'Show':''}        
    season = 1
    season_main_page_url = show_main_page_url + '/s{}'.format(season)   
    
    while establish_session(season_main_page_url).status_code == 200:
        check_prerelease = check_pre(season_main_page_url) #check to see if the season is available
        name = []
        org = []
        content =[]
        reviews = []
        page = 1
        
        print('Now working on season {}'.format(season))

        if not check_prerelease:
            info = get_season_infos(season_main_page_url)
            reviews_page_link_by_season = season_main_page_url + '/reviews?type=&sort=&page={}'.format(page)
            review_page_html = get_seasons_reviews_page_html(reviews_page_link_by_season)
            check = check_no_reviews(review_page_html) # check to see if there is any reviews on the review page
            
            
            while check :
                sleep_time = random.randint(1,3)
                print('working on page {}'.format(page))
                extract_reviews(review_page_html,name,org,content)
                            
                page += 1
                reviews_page_link_by_season = season_main_page_url + '/reviews?type=&sort=&page={}'.format(page)
                review_page_html = get_seasons_reviews_page_html(reviews_page_link_by_season)
                check = check_no_reviews(review_page_html)

                assemble_reviews(reviews, name, org, content)
                info['Reviews'] = reviews
                stuff['Show'] = show_name
                stuff['Season {}'.format(season)] = info
                time.sleep(sleep_time)
                
        else:
            print('Season {} is not available yet'.format(season))
            break
        
        print('Season {} is done'.format(season))
        season += 1
        season_main_page_url = show_main_page_url + '/s{}'.format(season)
        print('Season {} page response is {}'.format(season,establish_session(season_main_page_url).status_code))
        #check_prerelease = check_pre(season_main_page_url)
    return stuff        
    
# def check_proxy(url):
#     # ths function will check to see if the proxy ip is working and return both response and the ip
#     for ip in ip_list:
#         print('Going through ip list now...')
#         try:
#             proxy = {
#                 'http': ip, 'https': ip
#             }
#             print('Trying...')
#             response = session.get(url, headers = header_agent, proxies=proxy)
#             print(ip + ' is working!')
#             return response, proxy
            
        
#         except:
#             print(ip + ' not working. Trying a new one...')
    
    
def establish_session(url):
    #this function will use the working proxy ip to establish session
            
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
    if not urls:
        return urls
    else:
        return urls[0]    
    

def check_pre(season_main_page_link):
    html = establish_session(season_main_page_link).html

    select_prerelease = html.find('.mop-ratings-wrap__prerelease-text')
    
    return select_prerelease


def get_season_infos(season_main_page_link):
    '''
    This function will take TV Show's season info and output them in json format
    '''
    info = {'Year':'', 'User_ratings':'', 'audience_score':'', 'Critic_Ratings':'', 'tomatometer':'', 'consensus':'', 'Reviews':[]}

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
   

def check_no_reviews(html):
    check = html.find('.critic__review-quote')
    return check


def assemble_reviews(review_list, name_list, org_list, content_list):
    for i in range(len(name_list)):
                    review_keys = ['name', 'org', 'content']
                    value = [name_list[i], org_list[i], content_list[i]]

                    review_obj = dict(zip(review_keys,value))

                    review_list.append(review_obj)




if __name__ == '__main__':
    main()
