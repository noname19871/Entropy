
# coding: utf-8

# In[1]:


import gensim
import clear_text
import logging
import sys
import numpy as np
import os
from random import shuffle
import re
import urllib.request
import zipfile
import lxml.etree
import nltk
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# In[2]:


with zipfile.ZipFile('data.zip', 'r') as z:
    doc = lxml.etree.parse(z.open('ted_ru-20160408.xml', 'r'))
input_text = '\n'.join(doc.xpath('//content/text()'))
input_text = re.sub(r'\([^)]*\)', '', input_text)


# In[3]:


split_text = nltk.sent_tokenize(input_text)


# In[4]:


clear_text.view_samples(split_text, 500)


# In[5]:


diction = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
trash = ['!','@','#','№','$',';','%','^',':','&','?','*','(',')','-','_','=','+','}','{','[',']','*','/','0','1','2','3','4','5','6','7','8','9',',']
for i,item in enumerate(split_text):
    split_text[i] = clear_text.replace(split_text[i], trash).lower()
    string = ''
    for char in split_text[i]:
        if char in diction or char == ' ':
            string += char
    split_text[i] = string
with open('outfilename.txt', 'a', encoding='utf-8') as out:
    for str in split_text:
        out.write(str + '\n')


# In[6]:


split_text[0:10]


# In[7]:


for i,item in enumerate(split_text):
    split_text[i] = split_text[i].split(' ')
   


# In[8]:


for i,item in enumerate(split_text):
   for j,vol in enumerate(split_text[i]):
       if vol == '' or vol == ' ':
           del split_text[i][j]


# In[9]:


split_text[0:10]


# In[11]:


len(split_text)


# In[12]:


model = gensim.models.Word2Vec(sentences=split_text, size=500, window=5, min_count=77, workers=4, sg=1)


# In[13]:


model.wv.most_similar(positive=['хороший','женщина'], negative=['животное'])


# In[14]:


len(model.wv.vocab)
model.save('my.model')


# In[15]:


model.wv.most_similar(positive=['хороший','женщина'], negative=['животное'])


# In[16]:


model.wv.most_similar(positive=['плохой'])


# In[17]:


model.wv.most_similar(positive=['хороший'])


# In[18]:


model_ted = gensim.models.FastText (split_text, size = 200, window = 10, min_count = 5, workers = 4, sg = 1)


# In[82]:


model_ted.wv.most_similar(positive=['партнер'])


# In[19]:


model_ted.wv.most_similar(positive=['партнер'])


# In[20]:


model_ted.save('core_model.model')


# In[44]:


model_ted.wv.most_similar(positive=['ватикан'])

