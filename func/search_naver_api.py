#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def search_naver_api(keyword = '축구', client_id = "mFVJrDtj4trdT2ermoVF", client_secret = "hbpIY84KD3"):
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

    encText = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        results = response_body.decode('utf-8')
    else:
        print("Error Code:" + rescode)

    return results

