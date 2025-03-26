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
from bs4 import BeautifulSoup as bs


st.title("English Dictionary")
word = st.text_input("Enter a word:", "")

# *****************************************************************
# Data From wordnet by nltk

# Download nltk resources
nltk.download("wordnet")



langs= ['als', 'arb', 'bul', 'cat', 'cmn', 'dan', 'ell', 'eng', 'eus',
'fin', 'fra', 'glg', 'heb', 'hrv', 'ind', 'isl', 'ita', 'ita_iwn',
'jpn', 'lit', 'nld', 'nno', 'nob', 'pol', 'por', 'ron', 'slk',
'slv', 'spa', 'swe', 'tha', 'zsm']
st.write(len(set(wn.all_lemma_names())))
st.write(len(set(wn.all_synsets())))
# st.write('langs',wn.langs())
# st.write('sorted(wn.langs())', sorted(wn.langs()))
# st.write('wn.synonyms(word)', wn.synonyms(word))


def fetch_synset_info(synset):
    syn = synset
    syn_detail ={
        'synset_name':syn.name(),
        "definition": syn.definition(),
        'syn_offset':syn.offset(),
        "examples": syn.examples(),
        "hypernyms":syn.hypernyms(),
        "hyponyms":syn.hyponyms(),
        "entailments":syn.entailments(),
        "synonyms": list(set([lemma.name() for lemma in syn.lemmas()])),
        "antonyms": list(set([ant.name() for lemma in syn.lemmas() for ant in lemma.antonyms()])),
        "derivation": list(set([drf.name() for lemma in syn.lemmas() for drf in lemma.derivationally_related_forms()])),
        "pertainyms": list(set([per.name() for lemma in syn.lemmas() for per in lemma.pertainyms()])),
        "lemma_keys": list(set([lemma.key() for lemma in syn.lemmas()])),}
    return syn_detail



def fetch_wordnet_data_nltk(word):
    pos_tags = list(set([synset.pos() for synset in wn.synsets(word)]))
    details = {"word": word, 'etymology':{}}
    for pos in pos_tags:
        details['etymology'][pos]=[]
        for sense_num in range(len(wn.synsets(word,pos=pos))):
            synset=wn.synset(f'{word}.{pos}.{sense_num+1}')
            detail = fetch_synset_info(synset)
            detail['sense_num']= f'{word}.{pos}.{sense_num+1}'
            details['etymology'][pos].append(detail)
    return details


def output_to_streamlit(word):
    data_nltk_wn=fetch_wordnet_data_nltk(word)
    etymology=data_nltk_wn['etymology']
    st.write('##', data_nltk_wn['word'])
    for pos,synsets in etymology.items():
        st.write('###', pos)
        for syn in synsets:
            st.write(syn['sense_num'],syn['synset_name'])
            st.write('defintion:',syn['definition'])
            st.write('examples:',set(syn['examples']))
            st.write('synonyms:',set(syn['synonyms']))
            st.write('antonyms:',set(syn['antonyms']))
            st.write('derivation:',set(syn['derivation']))
            st.write('pertainyms:',set(syn['pertainyms']))

# st.write("tree",a1.tree())

    
st.write('## Data From wordnet by nltk')
# output_to_streamlit(word)



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
def fetch_wiktionary_data(word):
    page = pywikibot.Page(site, word)
    page_text = page.text
    return page_text

def parser_wikitionary_data(word):
    text=fetch_wiktionary_data(word)
    lines = text.split("\n")
    section_dict = {}
    section_stack = []  # Stack to track section hierarchy
    current_section = section_dict  # Start at root level
    
    for line in lines:
        line = line.strip()
        st.write(line)
        if not line:
            continue  # Skip empty lines
        # Check if it's a section header (Markdown format: == Section ==)
        match = re.match(r"^(=+)\s*(.*?)\s*\1$", line)
        if match:
            level = len(match.group(1))  # Number of '=' determines hierarchy
            section_name = match.group(2).strip()
            while len(section_stack)+2 > level:
                section_stack.pop()
            parent = section_dict
            for sec in section_stack:
                parent = parent[sec]
            parent[section_name] = {}
            section_stack.append(section_name)
        else:
            # If it's content, add it to the last section in the stack
            if section_stack:
                parent = section_dict
                for sec in section_stack:
                    parent = parent[sec]
                parent.setdefault("_content", []).append(line)
    return section_dict
    
st.write('## Data From Wiktionay by pywikibot')
# st.write(parser_wikitionary_data(word))
# st.code(fetch_wiktionary_data(word))

# page = pywikibot.Page(site, word)

# page.get_parsed_page()
# page_text = page.text
# page_text = page.get()
# sect = pywikibot.textlib.extract_sections(page.text, site)

# st.write('pywikibot',dir(pywikibot))
# st.write('page',dir(page))
# st.write('page_text',dir(page_text))

# ********************************************************************
# parse the wiktionary by page.get_parsed_page

def parse_wiktionary_by_bs(word):
    page = pywikibot.Page(site, word)
    page_html = page.get_parsed_page()
    soup = bs(page_html, 'html.parser')
    # body = soup.find_all('div',class_=re.compile(r'mw-heading mw-heading'))
    body = soup.find_all()
    # body = soup.find_all('div',class_="mw-content-ltr mw-parser-output")[0].find_all()
    # body = soup.find_all('main',id='content',class_='mw-body')[0].get_text()
    # mw-heading mw-heading2
    return body
st.write(parse_wiktionary_by_bs(word))




# ********************************************************************
# Data from DictionaryAPI.dev
def fetch_dictionaryapi_data(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    st.write(api_url)
    response = requests.get(api_url)
    if response.status_code == 200:
        api_data = response.json()
    return api_data
st.write('## Data from DictionaryAPI.dev')
data_dictionaryAPI=fetch_dictionaryapi_data(word)



# ********************************************************************
# Data from Stand4 network

def fetch_stand4_data(word):
    api_url = f"https://www.stands4.com/services/v2/defs.php?uid=13205&tokenid=01eaLfSB05gMMM8a&word={word}&format=json"
    st.write(api_url)
    st.write(f'https://www.definitions.net/definition/{word}')
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

st.write('## Other network')
st.write(f'https://www.merriam-webster.com/dictionary/{word}')
st.write(f'https://dictionary.cambridge.org/dictionary/english/{word}')
st.write(f'https://www.wordreference.com/es/translation.asp?tranword={word}')

