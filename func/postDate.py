#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def postDate(soup):
    date = soup.find_all("p", class_="date fil5 pcol2 _postAddDate") + soup.find_all("span", class_="se_publishDate pcol2")

    if date:
        postDate = BeautifulSoup(str(date.pop())).text
    else :
        postDate = 0
    
    return postDate

