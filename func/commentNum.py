#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def commentNum(soup):
    comtemp = str(soup.find_all('em', id='floating_bottom_commentCount'))
    commentNu = comtemp.replace('[<em id="floating_bottom_commentCount">','').replace('\n','').replace('\t','').replace('</em>]','')

    return commentNu

