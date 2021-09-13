#!/usr/bin/env python
# coding: utf-8

# In[1]:


def keyword_in_100(txt):
    a = txt.find("양궁")
    if(a<=100):
        return True
    else:
        return False

