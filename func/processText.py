#!/usr/bin/env python
# coding: utf-8

# In[1]:


def processText(txt):
    specialChars = "!#$%^&*()"
    for specialChar in specialChars:
        txt = txt.replace('  ', ' ')
        txt = txt.replace('   ', ' ')
        txt = txt.replace('    ', ' ')
        txt = txt.replace('     ', ' ')
    return txt.strip()

