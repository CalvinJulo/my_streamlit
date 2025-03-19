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

stands4_api = {
    "Definitions.net": f"https://www.stands4.com/services/v2/defs.php?uid=13205&tokenid=01eaLfSB05gMMM8a&word={word}&format=xml",
    "Anagrams.net": f"https://www.stands4.com/services/v2/ana.php?uid=13205&tokenid=01eaLfSB05gMMM8a&term={word}&format=xml",
    "Abbreviations.com": f"https://www.stands4.com/services/v2/abbr.php?uid=13205&tokenid=01eaLfSB05gMMM8a324&term={word}&format=xml",
    "Conversions.net": f"https://www.stands4.com/services/v2/conv.php?uid=13205&tokenid=01eaLfSB05gMMM8a324&expression={word}&format=xml",
    "Synonyms.com": f"https://www.stands4.com/services/v2/syno.php?uid=13205&tokenid=01eaLfSB05gMMM8a&word={word}&format=xml",
    "Quotes.net": "https://www.stands4.com/services/v2/quotes.php?uid=13205&tokenid=01eaLfSB05gMMM8a324&searchtype=AUTHOR&query=Albert+Einstein&format=xml",
    "Poetry.com": f"https://www.stands4.com/services/v2/poetry.php?uid=13205&tokenid=01eaLfSB05gMMM8a&term={word}&format=xml",
    "Lyrics.com": f"https://www.stands4.com/services/v2/lyrics.php?uid=13205&tokenid=01eaLfSB05gMMM8a&term={word}&artist=Alphaville&format=xml",
    "Grammar.com": f"https://www.stands4.com/services/v2/grammar.php?uid=13205&tokenid=01eaLfSB05gMMM8a&text={word}&format=json",
    "Literature.com": f"https://www.stands4.com/services/v2/literature.php?uid=13205&tokenid=01eaLfSB05gMMM8a&term={word}&format=xml",
    "Scripts.com": f"https://www.stands4.com/services/v2/scripts.php?uid=13205&tokenid=01eaLfSB05gMMM8a&term={word}&format=xml",
    "Biographies.net": None,
    "Phrases.com": f"https://www.stands4.com/services/v2/phrases.php?uid=13205&tokenid=01eaLfSB05gMMM8a&phrase={word}&format=xml",
    "Symbols.com": None,
    "References.net": None,
    "Rhymes.net": f"https://www.stands4.com/services/v2/rhymes.php?uid=13205&tokenid=01eaLfSB05gMMM8a&term={word}&format=xml",
    "uszip.com": f"https://www.stands4.com/services/v2/zip.php?uid=13205&tokenid=01eaLfSB05gMMM8a324&zip={word}&format=xml"
}
def fetch_stand4_data(word):
    api_url = f"https://www.stands4.com/services/v2/defs.php?uid=13205&tokenid=01eaLfSB05gMMM8a&word={word}&format=json"
    st.write(api_url)
    response = requests.get(api_url)
    if response:
        st.write('a')
    else:
        st.write('b')
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
# www.synonyms.com/
# www.beedictionary.com/
# www.finedictionary.com/


