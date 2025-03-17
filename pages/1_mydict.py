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


# Download nltk resources
nltk.download("wordnet")


# Streamlit UI
st.title("English Dictionary with Pronunciation")
word = st.text_input("Enter a word:", "")

details = []
for syn in wn.synsets(word):
    detail = {
        "word": word,
        "definitions": syn.definition(),
        "part_of_speech": syn.pos(),
        "examples": syn.examples(),
        "synonyms": list(set([lemma.name() for lemma in syn.lemmas()])),
        "antonyms": list(set([ant.name() for lemma in syn.lemmas() for ant in lemma.antonyms()])),
        "phonetics": '',  # Get phonetic transcription (IPA)
        "etymology": '', #https://www.etymonline.com/word
        "paronyms": '',
        "cognates": '',
        "phrases": '',
        "collocations": '',
    }
    details.append(detail)
st.write(details)


import pywikibot
import re


family = pywikibot.family.WikimediaFamily.content_families
# st.write(family)
site = pywikibot.Site("en", "wiktionary")
page = pywikibot.Page(site, 'articulate')
text = page.text

def clean_text(text):
    """Removes brackets, templates, and formatting."""
    text = re.sub(r"\{\{.*?\}\}", "", text)  # Remove {{template}}
    text = re.sub(r"\[\[(?:[^|\]]+\|)?([^|\]]+)\]\]", r"\1", text)  # Remove [[links]]
    text = re.sub(r"'''(.*?)'''", r"\1", text)  # Remove bold
    text = re.sub(r":\s*", "", text)  # Remove extra colons
    return text.strip()



from pywikibot.data import api
import json

# Connect to English Wiktionary
site = pywikibot.Site("en", "wiktionary")

def fetch_wiktionary_wikitext(word):
    """Fetches the raw WikiText of a word from Wiktionary."""
    
    params = {
        "action": "query",
        "format": "json",
        "titles": word,
        "prop": "revisions",
        "rvprop": "content"
    }
    
    request = api.Request(site=site, **params)
    response = request.submit()

    # Extract page content
    pages = response.get("query", {}).get("pages", {})
    page_content = next(iter(pages.values())).get("revisions", [{}])[0].get("*", "")

    return page_content

# Example: Fetch Wiktionary data for "articulate"
word = "articulate"
result = fetch_wiktionary_wikitext(word)
st.write(result)


def parse_wiktionary_page(word):
    site = pywikibot.Site("en", "wiktionary")
    page = pywikibot.Page(site, word)

    if not page.exists():
        return {"error": "Word not found"}
    st.code(page.text)
    st.write('---')
    lines = page.text.split("\n")
    word_data = {"word": word}
    current_2th_section=None
    current_3th_section=None
    current_4th_section=None
    current_5th_section=None

    current_meaning = None
    current_list = []
    in_list = False  # Track whether we are inside a list

    for line in lines:
        line = line.strip()
        if line.startswith("="):
            level= line.count("=") // 2
            section_name = line.strip("=").strip()
            if level == 2:
                word_data[section_name] = {}
                current_2th_section = section_name
                current_section = word_data[section_name]
            elif level == 3:
                word_data[current_2th_section][section_name] = {}
                current_3th_section = section_name
                current_section = word_data[current_2th_section][section_name]
            elif level == 4:
                word_data[current_2th_section][current_3th_section][section_name] = {}
                current_4th_section = section_name
                current_section = word_data[current_2th_section][current_3th_section][section_name]
            elif level == 5:
                word_data[current_2th_section][current_3th_section][current_4th_section][section_name] = {}
                current_5th_section = section_name   
                current_section = word_data[current_2th_section][current_3th_section][current_4th_section][section_name]
            in_list = False  # Reset list tracking
            current_section['definition'] =[]

        # Detect Lists (Synonyms, Antonyms, Derived Terms)
        elif line.startswith("*"):  
            if current_2th_section and current_3th_section:
                if isinstance(word_data[current_2th_section][current_3th_section], list):
                    word_data[current_2th_section][current_3th_section].append(line[2:].strip())

        # Detect Meanings (Start with "#")
        elif line.startswith("#") and not line.startswith("#*"):  
            definition = line[2:].strip()
            current_section['definition'].append(definition)

        # Detect Examples (Start with "#*")
        elif line.startswith("#*"):  
            example = line[3:].strip()
            if current_meaning:
                current_meaning["examples"].append(example)

        # Detect Synonyms and Antonyms (Start with "{{synonyms}}" or "{{antonyms}}")
        elif line.startswith("{{synonyms|"):
            synonyms = line.replace("{{synonyms|", "").replace("}}", "").split(", ")
            if current_meaning:
                current_meaning["synonyms"].extend(synonyms)
        elif line.startswith("{{antonyms|"):
            antonyms = line.replace("{{antonyms|", "").replace("}}", "").split(", ")
            if current_meaning:
                current_meaning["antonyms"].extend(antonyms)

        # Add regular text content if relevant
        elif line:
            if current_2th_section and current_3th_section:
                if isinstance(word_data[current_2th_section][current_3th_section], list):
                    word_data[current_2th_section][current_3th_section].append(line.strip())
    return word_data,lines


# Example Usage
# word_dict = parse_wiktionary_page("articulate")




tt ='https://api.dictionaryapi.dev/api/v2/entries/en/articulate'
st.write(tt)

