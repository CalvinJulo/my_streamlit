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
def fetch_Stand4_data(word):
    api_url = f"https://www.stands4.com/services/v2/defs.php?uid=13205&tokenid=01eaLfSB05gMMM8a&word={word}&format=json"
    response = requests.get(api_url)
    if response.status_code == 200:
        api_data = response.json()
    return api_data
st.write('## Data from Stand4 network')
st.write(fetch_Stand4_data(word))



# ********************************************************************
# Data source mainly from wordnet and wiktionary
# Data from spaCy
# Data from TextBlob
# Data from pattern.en
# www.synonyms.com/
# www.beedictionary.com/
# www.finedictionary.com/


