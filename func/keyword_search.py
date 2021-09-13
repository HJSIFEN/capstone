#!/usr/bin/env python
# coding: utf-8

# In[1]:


def keyword_search(txt):
    
    if(txt.find(keyword[0]) != -1):
        a = txt.find(keyword[0])
        b = 1
        while txt[a+1:].find(keyword) != -1:
            a = txt[a+1:].find(keyword) + a + 1
            b+=1
        return b

