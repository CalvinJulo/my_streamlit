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
API2 = "https://api.freedictionaryapi.com/v2/entries/en/"

def lookup(word):
    data = {'source1': None, 'source2': None}
    try:
        resp1 = requests.get(API1 + word).json()
        data['source1'] = resp1[0]
    except: pass
    try:
        resp2 = requests.get(API2 + word).json()
        data['source2'] = resp2['entries'][0]
    except: pass
    return data

st.title("📘 My Streamlit Dictionary")

q = st.text_input("Enter a word")
if q:
    results = lookup(q)
    st.write(results)
    s1, s2 = results['source1'], results['source2']

    if s1:
        st.subheader(f"{s1['word']}  •  {s1.get('phonetic','')}")
        for p in s1.get('phonetics',[]):
            if 'audio' in p:
                st.audio(p['audio'])
        for meaning in s1.get('meanings',[]):
            st.write(f"**{meaning['partOfSpeech']}**")
            for d in meaning['definitions']:
                st.write("-", d['definition'])
                if 'example' in d:
                    st.write("  >", d['example'])
    if s2 and 'etymology' in s2:
        st.subheader("Etymology")
        st.write(s2['etymology'])
