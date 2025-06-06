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
            st.write('defintion:','**'+syn['definition']+'**',)
            st.write('examples:',set(syn['examples']))
            st.write('synonyms:',set(syn['synonyms']),'antonyms:',set(syn['antonyms']),
                     'derivation:',set(syn['derivation']),'pertainyms:',set(syn['pertainyms']))

# st.write("tree",a1.tree())

st.write('## Data From wordnet by nltk')
# st.write(fetch_wordnet_data_nltk(word))
output_to_streamlit(word)



# ********************************************************************
# Data From Ety

st.write('## Data From Ety')
# st.write(ety.origins(word, recursive=True))
st.write(ety.tree(word))

# ********************************************************************
# Data From Wiktionay by pywikibot

site = pywikibot.Site("en", "wiktionary")

# Connect to English Wiktionary
def fetch_wiktionary_text(word):
    page = pywikibot.Page(site, word)
    page_text = page.text
    return page_text

# ********************************************************************
# parse the wiktionary by page.get_parsed_page and beautifulsoup

def parse_wiktionary_by_bs(word):
    page = pywikibot.Page(site, word)
    page_html = page.get_parsed_page()
    soup = bs(page_html, 'html.parser')
    body = soup.find_all('div',class_='mw-content-ltr mw-parser-output')[0]
    elements = body.find_all(['div', 'ul','ol','p'])
    section_dict = {}
    section_stack = []  
    current_section = section_dict  # Start at root level
    for elem in elements:
        if elem.get('class') and elem.get('class')[0]=='mw-heading':
            level=elem.get('class')[1][-1]
            section_name=elem.get_text().replace('[edit]','').strip()
            while len(section_stack)+2 > int(level):
                section_stack.pop()
            parent = section_dict
            for sec in section_stack:
                parent = parent[sec]
            parent[section_name] = {}
            current_section=parent[section_name]
            section_stack.append(section_name)
        elif elem.get('class') and elem.get('class')[0]=='NavFrame':
            Navhead = elem.find_all(class_='NavHead')[0].get_text()
            for li in elem.find_all('li'):
                text =li.get_text()
                current_section.setdefault(Navhead, []).append(text)
        elif elem.name=='p':
            current_section['intro_']=elem.get_text()
        elif elem.name=='ul' and not section_name=="Translations" and elem.find(class_='citation-whole') is None:
            for li in elem.find_all('li'):
                audio = li.find_all('a')
                if len(audio)==2 and audio[1].get_text()=='file':
                    text=li.get_text()+'https://en.wiktionary.org'+audio[1].get('href')
                else:
                    text =li.get_text()
                current_section.setdefault("content", []).append(text)
        elif elem.name=='ol':
            for li in elem.find_all('li'):
                meanings={}
                examples=[]
                definition=li.get_text()
                for ul in li.find_all('ul'):
                    if ul:
                        definition=definition.replace(ul.get_text(), '')
                for dd in li.find_all('dd'):
                    if dd:
                        example = dd.get_text()
                        examples.append(example)
                        definition=definition.replace(example, '')
                meanings['definition'] = definition.strip()
                meanings['examples'] =examples
                if li.find(class_='citation-whole') is not None and li.find(class_="usage-label-sense") is None:
                    pass
                else:
                    current_section.setdefault('meaning', []).append(meanings)
    return section_dict
 
st.write('## Data From Wiktionay by pywikibot')
st.write(parse_wiktionary_by_bs(word))

def output_to_streamlit_from_pywikibot(word):
    data_wiktionary=parse_wiktionary_by_bs(word)
    for sect2, sect2_value in data_wiktionary.items():
        if sect2=='English':
            for sect3, sect3_value in sect2_value.items():
                if sect3_value =={}:
                    continue
                st.write('###',sect3)
                if sect3_value['intro_']:
                    st.write(sect3_value['intro_'])
                try:
                    st.write(set(sect3_value['Pronunciation']['content'][:2]))
                except:
                    pass
                for sect4, sect4_value in sect3_value.items():
                    if sect4 not in ['intro_','Pronunciation']:
                        st.write('###',sect4)
                        st.write(sect4_value['intro_'])
                        for sect5, sect5_value in sect4_value.items():
                            if sect5=='meaning':
                                for value in sect4_value['meaning']:
                                    st.write('definition:',value['definition'])
                                    st.write('examples:', set(value['examples']))
                            if sect5 not in ['intro_','meaning'] :
                                try:
                                    st.write(sect5,set(sect4_value[sect5]['content']))
                                except:
                                    pass
    
# output_to_streamlit_from_pywikibot(word)

st.write('## kkkkkkkkkkkk')
def output_333_1(word):
    data_wiktionary=parse_wiktionary_by_bs(word)
    stack = [{'English':data_wiktionary['English']}]  # Start with the outer dictionary
    results = []  # Store extracted dictionaries

    while stack:
        current = stack.pop()  # Process the last element (LIFO)
        st.write('lllll')
        for k1,v1 in current['English'].items():
                for k2,v2 in v1.items():
                    if isinstance(v2, str):
                        st.write('bbbbb')
                        st.write(k1,v2)
                    elif isinstance(v2, list):
                        st.write('aaaaaa')
                        st.write(k2,set(v2))
                    elif isinstance(v2, dict):
                        for k3,v3 in v2.items():
                            if isinstance(v3, str):
                                st.write('nnnnnn')
                                st.write(k2,v3)
                            elif isinstance(v3, list):
                                st.write('ggggg')
                                st.write(k2,v3)
    # Print extracted dictionaries

output_333_1(word)

# ********************************************************************
# Data from DictionaryAPI.dev
def fetch_dictionaryapi_data(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    st.write(api_url)
    response = requests.get(api_url)
    if response.status_code == 200:
        api_data = response.json()
    return api_data

def output_dictionaryAPI(word):
    data_dictionaryAPI=fetch_dictionaryapi_data(word)
    stack = [i for i in data_dictionaryAPI]  # Start with the outer dictionary
    results = []  # Store extracted dictionaries

    while stack:
        current = stack.pop()  # Process the last element (LIFO)
        if isinstance(current, dict):
            results.append(current)  # Store the dictionary
            for value in current.values():  # Add all dictionary values to the stack
                if isinstance(value, dict):  # Only add dictionaries
                    stack.append(value)
                elif isinstance(value, list):  # If value is a list, check each element
                    for item in value:
                        if isinstance(item, dict):  # Add nested dictionaries in lists
                            stack.append(item)
    for result in results:
        for key,value in result.items():
            if not isinstance(value, dict) and value is not None:
                st.write(key, value)
st.write('## Data from DictionaryAPI.dev')
output_dictionaryAPI(word)

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
# www.vocabulary.com/
# www.dictionary.com/

st.write('## Other network')
st.write(f'https://www.merriam-webster.com/dictionary/{word}')
st.write(f'https://dictionary.cambridge.org/dictionary/english/{word}')
st.write(f'https://www.wordreference.com/es/translation.asp?tranword={word}')

