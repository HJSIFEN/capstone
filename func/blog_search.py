#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

