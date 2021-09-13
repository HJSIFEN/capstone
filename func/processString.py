#!/usr/bin/env python
# coding: utf-8

# In[19]:


def processString(txt):
    specialChars = "!#$%^&*()"
    for specialChar in specialChars:
        txt = txt.replace(specialChar, '')
        txt = txt.replace(',', ' ')
        txt = txt.replace('.', ' ')
        txt = txt.replace('"', ' ')
        txt = txt.replace('ღ', ' ')
        txt = txt.replace('​', ' ')
        txt = txt.replace('  ', ' ')
        txt = txt.replace('   ', ' ')
        txt = txt.replace('    ', ' ')
        txt = txt.replace('     ', ' ')
    return txt.strip()

