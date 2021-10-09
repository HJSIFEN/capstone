from bs4 import BeautifulSoup
import datetime
import re
import requests


def past_day(day):
    if day.find('전') > -1:
        return 0
    dt = day.split('.')
    return (datetime.datetime.now() - datetime.datetime(int(dt[0]), int(dt[1]) , int(dt[2]))).days

def visitor(url):
    id = url.split('/')[3]
    id = id[15:].split('&')[0]
    v_url = 'http://blog.naver.com/NVisitorgp4Ajax.nhn?'+id
    response = requests.get(v_url)
    sum_visitor = 0

    for text in BeautifulSoup(response.text).find_all('visitorcnt'):
        text = str(text)
        idx = re.search('cnt="[0-9]*"', text)
        idx1 = re.search('id="[0-9]*"', text)
        sum_visitor+=int(text[idx.span()[0]:idx.span()[1]].replace("cnt=", "").replace('"', ''))

    return sum_visitor

def make_past_day(data_dict):
    past_d = list(map(past_day, data_dict['post_date']))
    return past_d    

def processText(txt):
    specialChars = "!#$%^&*()"
    for specialChar in specialChars:
        txt = txt.replace('  ', ' ')
        txt = txt.replace('   ', ' ')
        txt = txt.replace('    ', ' ')
        txt = txt.replace('     ', ' ')
    return txt.strip()


def processString(txt):
    specialChars = "!#$%^&*()"
    for specialChar in specialChars:
        txt = txt.replace(specialChar, '')
        txt = txt.replace(',', ' ')
        txt = txt.replace('.', ' ')
        txt = txt.replace('"', ' ')
        txt = txt.replace('ღ', ' ')
        txt = txt.replace('​', ' ')
        txt = txt.replace('  ', ' ')
        txt = txt.replace('   ', ' ')
        txt = txt.replace('    ', ' ')
        txt = txt.replace('     ', ' ')
    return txt.strip()


def postDate(soup):
    date = soup.find_all("p", class_="date fil5 pcol2 _postAddDate") + soup.find_all("span", class_="se_publishDate pcol2")

    if date:
        postDate = BeautifulSoup(str(date.pop())).text
    else :
        postDate = 0
    
    return postDate


def keyword_in_100(txt):
    a = txt.find("양궁")
    if(a<=100):
        return True
    else:
        return False


def commentN(soup):
    comtemp = str(soup.find_all('em', id='floating_bottom_commentCount'))
    commentNu = comtemp.replace('[<em id="floating_bottom_commentCount">','').replace('\n','').replace('\t','').replace('</em>]','')

    return commentNu


import re

def site_popularity(link):
    if(re.search("naver", link)):
        return 10
    elif(re.search("daum", link)):
        return 5
    elif(re.search("tistory", link)):
        return 3
    else:
        return 1

def keyword_search(txt, keyword):
    
    if(txt.find(keyword) != -1):
        a = txt.find(keyword)
        b = 1
        while txt[a+1:].find(keyword) != -1:
            a = txt[a+1:].find(keyword) + a + 1
            b+=1
        return b
    else:
        return 0