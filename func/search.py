import urllib.request
import json
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import datetime
import fnmatch
import re

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

def processText(txt):
    specialChars = "!#$%^&*()"
    for specialChar in specialChars:
        txt = txt.replace('  ', ' ')
        txt = txt.replace('   ', ' ')
        txt = txt.replace('    ', ' ')
        txt = txt.replace('     ', ' ')
    return txt.strip()

# 본문에 키워드 언급 갯수
def keyword_search(txt, keyword):
    
    if(txt.find(keyword[0]) != -1):
        a = txt.find(keyword[0])
        b = 1
        while txt[a+1:].find(keyword) != -1:
            a = txt[a+1:].find(keyword) + a + 1
            b+=1
        return b

    

# 키워드가 본문의 처음 100단어 안에 포함되는가
def keyword_in_100(txt):
    a = txt.find("양궁")
    if(a<=100):
        return True
    else:
        return False

def search_naver_api(keyword = '축구', client_id = "mFVJrDtj4trdT2ermoVF", client_secret = "hbpIY84KD3", length = 10):
    """ 
    네이버 api를 사용하여 1000개의 블로그를 크롤링한다.

    통합검색에서 검색한 것 순서가 아닌 블로그 세션(https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=1&groupId=0)에서
    검색한 순서.

    input:
    keyword = 검색어
    client_id = 네이버_api_id
    client_secret = 네이버_api_pw

    output:
    네이버_api_output 
    (json 형식으로 되있음
    "title, link, description, bloggername, bloggerlink, postdate")

    """
    results = []
    encText = urllib.parse.quote(keyword)
    for i in range(1, length, 10):

        url = "https://openapi.naver.com/v1/search/blog?query=" + encText  + f'&display=100&start={i}&sort=sim'# json 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            results += [response_body.decode('utf-8')]
        else:
            print("Error Code:" + rescode)

    return results

def naver_api_blog_url(keyword = '축구', client_id = "mFVJrDtj4trdT2ermoVF", client_secret = "hbpIY84KD3", length = 10):
    results = search_naver_api(keyword, client_id, client_secret)
    items =[]
    blog_url = []
    for result in results:
        items = json.loads(result)['items']

    
        for i in range(len(items)):
            response1 = requests.get(items[i]['link'])
            soup = BeautifulSoup(response1.text)
            idx = str(soup.find_all('iframe').pop()).find('src')
            source = str(soup.find_all('iframe').pop())[idx+5:-11]
            source = source.replace('amp;', '')
            url = 'http://blog.naver.com' + source

            blog_url += [url]
        

    return blog_url

# 게시날짜
def postDate(soup):
    date = soup.find_all("p", class_="date fil5 pcol2 _postAddDate") + soup.find_all("span", class_="se_publishDate pcol2")

    if date:
        postDate = BeautifulSoup(str(date.pop())).text
    else :
        postDate = 0
    
    return postDate

# 댓글 개수
def _commentNum(soup):
    comtemp = str(soup.find_all('em', id='floating_bottom_commentCount'))
    commentNu = comtemp.replace('[<em id="floating_bottom_commentCount">','').replace('\n','').replace('\t','').replace('</em>]','')

    return commentNu

def blog_search(keyword, length = 1000):

    url_list = []

    for start in range(1, length, 30):
        
        url = "https://search.naver.com/search.naver?query="+ keyword + "&nso=&where=blog&sm=tab_opt&start="+str(start)
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
      
        for a in soup.find_all('a', 'api_txt_lines total_tit'):
            start_idx = str(a).find("href")
            end_idx = str(a).find("onclick")
            temp_url = str(a)[start_idx + 6 : end_idx-2].replace('?Redirect=Log&amp;logNo=', '/')
            if(fnmatch.fnmatch(temp_url, '*naver*')):
                response = requests.get(temp_url)
                soup=BeautifulSoup(response.text)
                idx = str(soup.find_all('iframe').pop()).find('src')
                source = str(soup.find_all('iframe').pop())[idx+5:-11]
                    
                source = source.replace('amp;', '')
                url = 'http://blog.naver.com' + source
                url_list += [url]
    return url_list                



def get_data(keyword = '축구', client_id = "mFVJrDtj4trdT2ermoVF", client_secret = "hbpIY84KD3", naver_api = False, length = 1000):
    text1 = [] #데이터 값
    text_amount = []        # 본문 분량
    keyword_mentioned = []  # 키워드 언급 횟수
    commentNum = []         # 댓글 개수
    keyword_100 = []        # 첫 100단어안에 키워드 포함 여부(포함1, 미포함0)
    keyword_title_data = [] # 제목에 키워드 포함 여부
    link_num_data = []      # 링크 개수
    player_num_data = []    # 동영상 개수
    img_num_data = []       # 이미지 개수
    poDate = []

    # naver api
    if naver_api:
        blog_url = naver_api_blog_url(keyword, client_id, client_secret, length)

    else :
        blog_url = blog_search(keyword, length)

    for url in blog_url :
        text2 = ""
        # response1 = requests.get(items[i]['link'])
        # soup = BeautifulSoup(response1.text)
        # idx = str(soup.find_all('iframe').pop()).find('src')
        # source = str(soup.find_all('iframe').pop())[idx+5:-11]
        # source = source.replace('amp;', '')
        # url = 'http://blog.naver.com' + source
        response1 = requests.get(url)
        soup = BeautifulSoup(response1.text)
        # 예외처리
        temp = soup.find_all("div", "se-main-container") + soup.find_all("div", id="postViewArea")
        try:
            temp1 = BeautifulSoup(str(temp.pop()))
        except:
            continue
        text = temp1.text.replace('\n', ' ')
        text1.append([processString(text)])
        title = soup.title.text

        #지난 날짜, 포스트 날짜
        poDate += [postDate(soup)]


        #댓글 갯수
        commentNu = _commentNum(soup)
        
        
        try:
            commentNum.append(int(commentNu))
        except:
            commentNum.append(0)
            

        # 키워드 언급 개수
        keyword_mentioned.append(keyword_search(text, keyword))
            
        # 본문 분량
        text2 += processText(text)
        text_amount.append(len(text2))
        
        if keyword_in_100(text) == True:
            keyword_100.append(1)
        else:
            keyword_100.append(0)
            
        if type(keyword) != list:
            keyword_list = keyword.split()
        keyword_title = []
        
        for k in keyword_list:
            keyword_title += [k in title]
            
        if keyword_title == [True]:
            keyword_title_data.append(1)
        else:
            keyword_title_data.append(0)
                
        
        link_num = len(temp1.find_all('div', class_="se-module se-module-oglink"))
        link_num_data.append(link_num)
        
        player_num= len(temp1.find_all('div', class_= 'se-component se-video se-l-default') + temp1.find_all('a', class_="se-link"))
        player_num_data.append(player_num)

        img_num= len(temp1.find_all('img'))
        img_num_data.append(img_num)

    data_dict = {}
    data_dict['text_amount'] = text_amount
    data_dict['keyword_mentioned'] = keyword_mentioned
    data_dict['commentNum'] = commentNum
    data_dict['keyword_100'] = keyword_100
    data_dict['keyword_title_data'] = keyword_title_data
    data_dict['link_num_data'] = link_num_data
    data_dict['player_num_data'] = player_num_data
    data_dict['img_num_data'] = img_num_data
    data_dict['post_date'] = poDate
    
    
    return data_dict, text1