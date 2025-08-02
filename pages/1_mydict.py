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
from pages.dictionary.dict_source import *


st.title("English Dictionary")
word = st.text_input("Enter a word:", "")

with st.expander("dictionaryapi"):
    st.write(parse_dictionaryapi_data(word))
with st.expander("freedictionaryapi"):
    st.write(parse_freedictionaryapi_data(word))
with st.expander("stand4 (need rewrite)"):
    try:
        st.write(parse_stand4_data(word))
    except:
        pass
with st.expander("ety"):
    st.write(parse_ety_data(word))
with st.expander("wordnet"):
    st.write(parse_wordnet_data_by_nltk(word))
with st.expander("wiktionary"):
    st.write(parse_wiktionary_data(word))

with st.expander("1"):
    page = pywikibot.Page(site, word)
    page_html = page.get_parsed_page()
    st.write(page_html)



st.write('## Other network')
st.write(f'https://www.merriam-webster.com/dictionary/{word}')
st.write(f'https://dictionary.cambridge.org/dictionary/english/{word}')
st.write(f'https://www.wordreference.com/es/translation.asp?tranword={word}')

