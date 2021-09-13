#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def naverKwdApi(keyword):
    
    rel_kwd_stat = RelKwdStat.RelKwdStat(BASE_URL, API_KEY, SECRET_KEY, CUSTOMER_ID)

    target_rel_kwd_stat = rel_kwd_stat.get_rel_kwd_stat_list(None, hintKeywords=keyword, showDetail='1')
    #for i in target_rel_kwd_stat:
    print("PC조회수: ", target_rel_kwd_stat[0].monthlyPcQcCnt)

