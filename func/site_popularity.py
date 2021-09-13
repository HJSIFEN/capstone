#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

