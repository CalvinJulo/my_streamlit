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

a1 = wn.synsets(word)[0]
b1 = a1.lemmas()[0]

c=[]
for i in wn.synsets(word):
    d={}
    d[i.name()]=i.lemmas()
    c.append(d)
st.write('c',c)

st.write("acyclic_tree",a1.acyclic_tree())
st.write("also_sees",a1.also_sees())
st.write("causes",a1.causes())
# st.write("closure",a1.closure())
# st.write("common_hypernyms",a1.common_hypernyms())
st.write("definition",a1.definition())
st.write("entailments",a1.entailments())
st.write("examples",a1.examples())
st.write("frame_ids",a1.frame_ids())
st.write("hypernym_distances",a1.hypernym_distances())
st.write("hypernym_paths",a1.hypernym_paths())
st.write("hypernyms",a1.hypernyms())
st.write("hyponyms",a1.hyponyms())
st.write("in_region_domains",a1.in_region_domains())
st.write("in_topic_domains",a1.in_topic_domains())
st.write("in_usage_domains",a1.in_usage_domains())
st.write("instance_hypernyms",a1.instance_hypernyms())
st.write("instance_hyponyms",a1.instance_hyponyms())
# st.write("jcn_similarity",a1.jcn_similarity())
# st.write("lch_similarity",a1.lch_similarity())
st.write("lemma_names",a1.lemma_names())
st.write("lemmas",a1.lemmas())
st.write("lexname",a1.lexname())
# st.write("lowest_common_hypernyms",a1.lowest_common_hypernyms())
st.write("max_depth",a1.max_depth())
st.write("member_holonyms",a1.member_holonyms())
st.write("member_meronyms",a1.member_meronyms())
st.write("min_depth",a1.min_depth())
# st.write("mst",a1.mst())
st.write("name",a1.name())
st.write("offset",a1.offset())
st.write("part_holonyms",a1.part_holonyms())
st.write("part_meronyms",a1.part_meronyms())
# st.write("path_similarity",a1.path_similarity())
st.write("pos",a1.pos())
st.write("region_domains",a1.region_domains())
# st.write("res_similarity",a1.res_similarity())
st.write("root_hypernyms",a1.root_hypernyms())
# st.write("shortest_path_distance",a1.shortest_path_distance())
st.write("similar_tos",a1.similar_tos())
st.write("substance_holonyms",a1.substance_holonyms())
st.write("substance_meronyms",a1.substance_meronyms())
st.write("topic_domains",a1.topic_domains())
# st.write("tree",a1.tree())
st.write("usage_domains",a1.usage_domains())
st.write("verb_groups",a1.verb_groups())
# st.write("wup_similarity",a1.wup_similarity())

st.write('***')

st.write("also_sees",b1.also_sees())
st.write("antonyms",b1.antonyms())
st.write("attributes",b1.attributes())
st.write("causes",b1.causes())
st.write("count",b1.count())
st.write("derivationally_related_forms",b1.derivationally_related_forms())
st.write("entailments",b1.entailments())
st.write("frame_ids",b1.frame_ids())
st.write("frame_strings",b1.frame_strings())
st.write("hypernyms",b1.hypernyms())
st.write("hyponyms",b1.hyponyms())
st.write("in_region_domains",b1.in_region_domains())
st.write("in_topic_domains",b1.in_topic_domains())
st.write("in_usage_domains",b1.in_usage_domains())
st.write("instance_hypernyms",b1.instance_hypernyms())
st.write("key",b1.key())
st.write("lang",b1.lang())
st.write("member_holonyms",b1.member_holonyms())
st.write("member_meronyms",b1.member_meronyms())
st.write("name",b1.name())
st.write("part_holonyms",b1.part_holonyms())
st.write("part_meronyms",b1.part_meronyms())
st.write("pertainyms",b1.pertainyms())
st.write("region_domains",b1.region_domains())
st.write("similar_tos",b1.similar_tos())
st.write("substance_holonyms",b1.substance_holonyms())
st.write("substance_meronyms",b1.substance_meronyms())
st.write("synset",b1.synset())
st.write("syntactic_marker",b1.syntactic_marker())
st.write("topic_domains",b1.topic_domains())
st.write("usage_domains",b1.usage_domains())
st.write("verb_groups",b1.verb_groups())


    
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


