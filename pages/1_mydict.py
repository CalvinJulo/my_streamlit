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
            "word": word,"definitions": syn.definition(),"part_of_speech": syn.pos(),
            "examples": syn.examples(),
            "synonyms": list(set([lemma.name() for lemma in syn.lemmas()])),
            "antonyms": list(set([ant.name() for lemma in syn.lemmas() for ant in lemma.antonyms()])),
            "phonetics": '',  # Get phonetic transcription (IPA)
            "etymology": '', #https://www.etymonline.com/word
            "paronyms": '',
            "cognates": '',
            "phrases": '',
            "collocations": '',}
        details.append(detail)
    return details

st.write('dir(wn)',dir(wn))
st.write('dir(wn.synsets(word))',dir(wn.synsets(word)))
st.write('dir(wn.synonyms(word))',dir(wn.synonyms(word)))
st.header("Data From wordnet by nltk")
# st.write(fetch_wordnet_data_nltk(word))
st.write('wn.synsets(word)',wn.synsets(word))
for syn in wn.synsets(word):
    st.write('dir(syn)',dir(syn))
    st.write('syn.lemmas()',syn.lemmas())
    st.write('dir(syn.lemmas()[0])',dir(syn.lemmas()[0]))





# ********************************************************************
# Data From Wiktionay by pywikibot

# family = pywikibot.family.WikimediaFamily.content_families
# st.write(family)

word = st.text_input("Enter a word:", "articulate")
site = pywikibot.Site("en", "wiktionary")

# Connect to English Wiktionary
def fetch_wiktionay_data(word):
    page = pywikibot.Page(site, word)
    page_text = page.text
    return page_text

st.write('## Data From Wiktionay by pywikibot')
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

