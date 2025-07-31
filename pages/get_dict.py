# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：
# Description： 
"""

# CMD Run Command ： streamlit run /Users/stock/st_stock.py --server.port 8501

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)




'''
def parse_json(data, indent=0):
    space = "." * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if value == '':
                pass
            elif value == []:
                pass
            else:
                st.write(f"{space}{key}:")
                parse_json(value, indent + 1)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            # st.write(f"{space}- Item {index + 1}:")
            parse_json(item, indent + 1)
    else:
        st.write(f"{space}{data}")

'''



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



# *****************************************************************
# Data From wordnet by nltk

# Download nltk resources
nltk.download("wordnet")

langs= ['als', 'arb', 'bul', 'cat', 'cmn', 'dan', 'ell', 'eng', 'eus',
'fin', 'fra', 'glg', 'heb', 'hrv', 'ind', 'isl', 'ita', 'ita_iwn',
'jpn', 'lit', 'nld', 'nno', 'nob', 'pol', 'por', 'ron', 'slk',
'slv', 'spa', 'swe', 'tha', 'zsm']

# st.write(len(set(wn.all_lemma_names())))
# st.write(len(set(wn.all_synsets())))
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



def fetch_wordnet_data_by_nltk(word):
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


def parse_wordnet_data_by_nltk(word):
    data_nltk_wn=fetch_wordnet_data_by_nltk(word)
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



# ********************************************************************
# Data From Ety
def fetch_ety_data(word):
    return 

def parse_ety_data(word):
    # data = fetch_ety_data(word)
    st.write(ety.origins(word, recursive=True))
    st.write(ety.tree(word))


# *****************************************************************
# Data from Stand4 network

def fetch_stand4_data(word):
    api_url = f"https://www.stands4.com/services/v2/defs.php?uid=13205&tokenid=01eaLfSB05gMMM8a&word={word}&format=json"
    # st.write(f'https://www.definitions.net/definition/{word}')
    try:
        return requests.get(api_url).json()
    except Exception:
        return []

def parse_stand4_data(word):
    data = fetch_stand4_data(word)
    st.write(data)
    st.write('sdjkads')
    for term in data['result']:
        st.subheader(f"{term['term']} ")
        st.write(f"**{term['partofSpeech']}**")
        st.write("-", term['definition'])
        if not isinstance(data_list, dict):
            st.write("  >", term['example'])


# *****************************************************************
# Data From dictionaryapi

def fetch_dictionaryapi_data(word):
    dictionaryapi_API = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    try:
        return requests.get(dictionaryapi_API).json()
    except Exception:
        return []

def parse_dictionaryapi_data(word):
    data_list = fetch_dictionaryapi_data(word)
    for index, data in enumerate(data_list):
        st.subheader(f"{data['word']}  •  {data.get('phonetic')}")
        for p in data.get('phonetics'):
            if 'text' in p and p['text'] != '':
                st.write(p['text'])
            if 'audio' in p and p['audio'] != '':
                st.audio(p['audio'])       
        for meaning in data.get('meanings',[]):
            st.write(f"**{meaning['partOfSpeech']}**")
            if "synonyms" in meaning and meaning["synonyms"] != []:
                st.write("  >",'synonyms',set(meaning['synonyms']))
            if "antonyms" in meaning and meaning["antonyms"] != []:
                st.write("  >",'antonyms',set(meaning['antonyms']))
            for d in meaning['definitions']:
                st.write("-", d['definition'])
                if "synonyms" in d and d["synonyms"] != []:
                    st.write("  >",'synonyms',set(d['synonyms']))
                if "antonyms" in d and d["antonyms"] != []:
                    st.write("  >",'antonyms',set(d['antonyms']))
                if 'example' in d:
                    st.write("  >", d['example'])
                


# *****************************************************************
# Data From freedictionaryapi

def fetch_freedictionaryapi_data(word):
    freedictionaryapi_API = "https://freedictionaryapi.com/api/v1/entries/en/" + word
    try:
        return requests.get(freedictionaryapi_API).json()
    except Exception:
        return []

def parse_freedictionaryapi_data(word):
    data = fetch_freedictionaryapi_data(word)
    st.subheader(f"{data['word']}")
    for entry in data['entries']:
        st.write(f"**{entry['partOfSpeech']}**")
        st.write("Pronunciations:")
        columns=st.columns(len(entry['pronunciations']))
        for num, col in enumerate(columns):
            pr = entry['pronunciations'][num]
            # col.write(pr.get('type'))
            col.write(pr.get('text'))
            # col.write(pr.get('tags'))
            
        #st.write("Forms (word family):")
        #for f in entry['forms']:
        #    st.write("-", f.get('word'), f.get('tags', []))
            
        st.write("Senses / Definitions:")
        for s in entry.get('senses', []):
            st.write("-", "Definition:", s.get('definition'))
            #if s.get('tags'):
            #     st.write("  Tags:", set(s.get('tags')))
            if s.get('examples'):
                for ex in s.get('examples'):
                    st.write("  >", "Example:", ex)
            if s.get('synonyms'):
                st.write("  Synonyms:", ", ".join(s['synonyms']))
            if s.get('antonyms'):
                st.write("  Antonyms:", ", ".join(s['antonyms']))
            if s.get('quotes'):
                st.write("  Quotes:")
                for q in s['quotes']:
                    st.write("  >", q.get('text'), "(", q.get('reference'), ")")

            for subs in s['subsenses']:
                st.write(" – Sub-definition:", subs.get('definition'))
                # if subs.get('tags'):
                #    st.write("  Tags:", set(subs.get('tags')))
                if subs.get('examples'):
                    for ex in subs.get('examples'):
                        st.write("  >", "Example:", ex)
                if subs.get('quotes'):
                    st.write("  Quotes:")
                    for q in subs['quotes']:
                        st.write("  >", q.get('text'), "(", q.get('reference'), ")")
                if subs.get('synonyms'):
                    st.write("  Synonyms:", ", ".join(subs['synonyms']))
                if subs.get('antonyms'):
                    st.write("  Antonyms:", ", ".join(subs['antonyms']))

                # Translations if present
                #if subs.get('translations'):
                #    st.write("  Translations:")
                #    for tr in subs['translations']:
                #        lang2 = tr.get('language', {})
                #        st.write(f"    {lang2.get('name')} ({lang2.get('code')}): {tr.get('word')}")
                # Subsenses
                if subs.get('subsenses'):
                    st.write("  Subsenses:")
                    for subs in s['subsenses']:
                        st.write("    – Sub-definition:", subs.get('definition'))

        # Entry-level synonyms / antonyms
        if entry.get('synonyms'):
            st.write("Entry Synonyms:", ", ".join(entry['synonyms']))
        if entry.get('antonyms'):
            st.write("Entry Antonyms:", ", ".join(entry['antonyms']))


word = st.text_input("Enter a word")
# st.write(parse_dictionaryapi_data(word))
# st.write(parse_freedictionaryapi_data(word))
# st.write(parse_stand4_data(word))
st.write(parse_ety_data(word))
st.write(parse_wordnet_data_by_nltk(word))



