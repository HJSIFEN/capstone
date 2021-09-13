#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def naver_api_blog_url(keyword = '축구', client_id = "mFVJrDtj4trdT2ermoVF", client_secret = "hbpIY84KD3"):
    results = search_naver_api(keyword, client_id, client_secret)
    items = json.loads(results)['items']

    blog_url = []

    for i in range(len(items)):
        response1 = requests.get(items[i]['link'])
        soup = BeautifulSoup(response1.text)
        idx = str(soup.find_all('iframe').pop()).find('src')
        source = str(soup.find_all('iframe').pop())[idx+5:-11]
        source = source.replace('amp;', '')
        url = 'http://blog.naver.com' + source

        blog_url += [url]
        

    return blog_url

