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



# *****************************************************************
# Data From dictionaryapi

def fetch_dictionaryapi_data(word):
    dictionaryapi_API = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    try:
        dictionaryapi_resp = requests.get(dictionaryapi_API).json()
    except:
        dictionaryapi_resp =[]
        pass
    return dictionaryapi_resp  # list type

def parse_dictionaryapi_data(word):
    data = fetch_dictionaryapi_data(word)
    st.write('lllllllllll')
    def parse_data(data):
        if isinstance(data, dict):
            st.write('ggggggg')
            st.write(data)
            for key, value in data.items():
                if value == '':
                    pass
                elif value == []:
                    pass
                elif key == 'phonetics':
                    for index, item in enumerate(key):
                        st.write(item['text'])
                        if item['audio'] and item['audio'] is not '':
                            st.audio(item['audio'])
                elif key == 'partOfSpeech':
                    st.write(f"**{value}**")
                elif key == 'definitions':
                    for d in value:
                        st.write("-", d['definition'])
                        if 'example' in d and d['example'] is not '':
                            st.write("  >", d['example'])
                        if 'synonyms' in d and d['synonyms'] is not '':
                            st.write("  >", d['synonyms'])
                        if 'antonyms' in d and d['antonyms'] is not '':
                            st.write("  >", d['antonyms'])
                elif key == 'antonyms':
                    st.write("  >", d['antonyms'])
                elif key == 'synonyms':
                    st.write("  >", d['synonyms'])
                else:
                    parse_data(value)
        elif isinstance(data, list):
            st.write('ooooooooo')
            for index, item in enumerate(data):
                if item['word']:
                    st.subheader(f"{item['word']}  •  {item.get('phonetic')}")
                st.write(data)
                parse_data(item)
        else:
            pass


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
st.write(parse_dictionaryapi_data(word))
# st.write(parse_freedictionaryapi_data_by_bs(word))

#parse_json(fetch_freedictionaryapi_data(word), indent=0)
