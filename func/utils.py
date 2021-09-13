from bs4 import BeautifulSoup

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