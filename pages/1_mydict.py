"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description：
"""
# CMD Run Command ： streamlit run /Users/xx.py --server.port 8501

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import streamlit as st
from gtts import gTTS
import nltk
from nltk.corpus import wordnet as wn
from io import BytesIO
import json
import requests
import pywikibot
import re
import ety


st.title("English Dictionary")
word = st.text_input("Enter a word:", "")

# *****************************************************************
# Data From wordnet by nltk

# Download nltk resources
nltk.download("wordnet")

def fetch_wordnet_data_nltk(word):
    details = []
    for syn in wn.synsets(word):
        detail = {
            "word": word,
            "definitions": syn.definition(),
            "part_of_speech": syn.pos(),
            "examples": syn.examples(),
            "hypernyms":syn.hypernyms(),
            "hyponyms":syn.hyponyms(),
            "entailments":syn.entailments(),         
            "synonyms": list(set([lemma.name() for lemma in syn.lemmas()])),
            "antonyms": list(set([ant.name() for lemma in syn.lemmas() for ant in lemma.antonyms()])),
            "derivationally_related_forms": list(set([drf.name() for lemma in syn.lemmas() for drf in lemma.derivationally_related_forms()])),
            "pertainyms": list(set([per.name() for lemma in syn.lemmas() for per in lemma.pertainyms()])),
        }
        details.append(detail)
    return details

langs= ['als', 'arb', 'bul', 'cat', 'cmn', 'dan', 'ell', 'eng', 'eus',
'fin', 'fra', 'glg', 'heb', 'hrv', 'ind', 'isl', 'ita', 'ita_iwn',
'jpn', 'lit', 'nld', 'nno', 'nob', 'pol', 'por', 'ron', 'slk',
'slv', 'spa', 'swe', 'tha', 'zsm']
st.write(len(set(wn.all_lemma_names())))
st.write(len(set(wn.all_synsets())))
# st.write('langs',wn.langs())
# st.write('sorted(wn.langs())', sorted(wn.langs()))
# st.write('wn.synonyms(word)', wn.synonyms(word))

st.write(wn.synset('dog.n.01'))
st.write(wn.synset('dog.n.02'))
st.write(wn.synset('dog.n.02').lemma_names())
st.write(wn.synset('dog.n.03'))
st.write(wn.synset('dog.n.04'))
st.write(wn.synset('dog.n.05'))
st.write(wn.synset('dog.n.06'))
st.write(wn.synset('dog.n.07'))
st.write(wn.synset('dog.n.08'))

st.write(wn.synsets('dog'))
for syn in wn.synsets('dog'):
    st.write(syn,syn.name(),syn.offset())
    for lemma in syn.lemmas():
        st.write(lemma,lemma.name(),lemma.key(),lemma.frame_strings(),lemma.frame_ids())

st.write('---')
st.write(wn.synset('dog.n.01'))
st.write(wn.synset('dog.n.01').lemmas())

st.write(wn.synset('dog.n.01').lemmas()[0].frame_strings())
st.write(wn.synset('dog.n.01').lemmas()[0].frame_ids())
st.write(wn.synset('dog.n.01').lemmas()[0].key())
st.write(wn.synset('dog.n.01').lemmas()[1].frame_strings())
st.write(wn.synset('dog.n.01').lemmas()[0].frame_ids())
st.write(wn.synset('dog.n.01').lemmas()[1].key())
st.write(wn.synset('dog.n.01').lemmas()[1].key())
st.write(wn.lemma_from_key(wn.synset('dog.n.01').lemmas()[1].key()))

st.write('---')
st.write(wn.lemmas('dog'))
st.write(wn.lemma('dog.n.01.dog').synset())
st.write(wn.synonyms('dog'))

c=[]
for i in wn.synsets(word):
    d={}
    d[i.name()]=i.lemmas()
    d['lemmas_names']=i.lemma_names()
    d['example']=i.examples()
    d['definition']=i.definition()
    d['name']=i.name()
    d['pos']=i.pos()
    d['verb_groups']=i.verb_groups()
    d['lemmas']=[]
    for j in i.lemmas():
        e={}
        e['verb_groups']=j.count()
        e['attributes']=j.attributes()
        e['antonyms']=j.antonyms()
        e['key']=j.key()
        e['lang']=j.lang()
        e['name']=j.name()
        e['synset']=j.synset()
        e['verb_groups']=j.verb_groups()
        e['derivation']=j.derivationally_related_forms()
        e['pertainyms']=j.pertainyms()       
        d['lemmas'].append(e)
    c.append(d)
st.write('c',c)




# st.write("tree",a1.tree())




    
st.write('## Data From wordnet by nltk')

st.write(fetch_wordnet_data_nltk(word))


# ********************************************************************
# Data From Ety

st.write('## Data From Ety')
# st.write(ety.origins(word, recursive=True))
st.write(ety.tree(word))

# ********************************************************************
# Data From Wiktionay by pywikibot

# family = pywikibot.family.WikimediaFamily.content_families
# st.write(family)

site = pywikibot.Site("en", "wiktionary")

# Connect to English Wiktionary
def fetch_wiktionay_data(word):
    page = pywikibot.Page(site, word)
    page_text = page.text
    return page_text

st.write('## Data From Wiktionay by pywikibot')
with st.expander('Expander'):
    st.code(fetch_wiktionay_data(word))

# ********************************************************************
# Data from DictionaryAPI.dev
def fetch_dictionaryapi_data(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    if response.status_code == 200:
        api_data = response.json()
    return api_data
st.write('## Data from DictionaryAPI.dev')
st.write(fetch_dictionaryapi_data(word))



# ********************************************************************
# Data from Stand4 network

def fetch_stand4_data(word):
    api_url = f"https://www.stands4.com/services/v2/defs.php?uid=13205&tokenid=01eaLfSB05gMMM8a&word={word}&format=json"
    st.write(api_url)
    response = requests.get(api_url)
    if response.status_code == 200:
        api_data = response.json()
    else:
        api_data = 'No response'
    return api_data
st.write('## Data from Stand4 network')
st.write(fetch_stand4_data(word))



# ********************************************************************
# Data source mainly from wordnet and wiktionary
# Data from spaCy
# Data from TextBlob
# Data from pattern.en
# www.definitions.net
# www.beedictionary.com/
# www.finedictionary.com/


