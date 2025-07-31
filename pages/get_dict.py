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


import requests
import streamlit as st


API1 = "https://api.dictionaryapi.dev/api/v2/entries/en/"
API2 = "https://freedictionaryapi.com/api/v1/entries/en/"



def parse_json(data, indent=0):
    space = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            st.write(f"{space}{key}:")
            parse_json(value, indent + 1)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            st.write(f"{space}- Item {index + 1}:")
            parse_json(item, indent + 1)
    else:
        st.write(f"{space}{data}")





# *****************************************************************
# Data From dictionaryapi

def fetch_dictionaryapi_data(word):
    dictionaryapi_API = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    try:
        dictionaryapi_resp = requests.get(dictionaryapi_API).json()[0]
    except:
        dictionaryapi_resp =[]
        pass
    return dictionaryapi_resp

def parse_dictionaryapi_data(word):
    data = fetch_dictionaryapi_data(word)
    st.subheader(f"{data['word']}  •  {data.get('phonetic','')}")
    for p in data.get('phonetics',[]):
        if 'audio' in p:
            st.audio(p['audio'])
    for m in data.get('meanings',[]):
        st.write(f"**{m['partOfSpeech']}**")
        for d in m['definitions']:
            st.write("-", d['definition']) 
            if 'example' in d:
                st.write("  >", d['example'])


# *****************************************************************
# Data From freedictionaryapi

def fetch_freedictionaryapi_data(word):
    freedictionaryapi_API = "https://freedictionaryapi.com/api/v1/entries/en/" + word
    try:
        freedictionaryapi_resp = requests.get(freedictionaryapi_API).json()
    except:
        freedictionaryapi_resp =[]
        pass
    return freedictionaryapi_resp

def parse_freedictionaryapi_data_by_bs(word):
    data = fetch_freedictionaryapi_data(word)
    if data and 'etymology' in data:
        st.subheader("Etymology")
        st.write(data['etymology'])

word = st.text_input("Enter a word")
# st.write(parse_dictionaryapi_data(word))
# st.write(parse_freedictionaryapi_data_by_bs(word))

parse_json(fetch_dictionaryapi_data(word), indent=0)
parse_json(fetch_freedictionaryapi_data(word), indent=0)
