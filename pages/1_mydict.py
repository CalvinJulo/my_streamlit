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


# Connect to English Wiktionary
site = pywikibot.Site("en", "wiktionary")

def fetch_wiktionary_text(word):
    """Use data.api to fetches the raw WikiText of a word from Wiktionary."""
    """The same to pywikibot.Page(site,word)"""
    params = {"action": "query", "format": "json", "titles": word, "prop": "revisions", "rvprop": "content"}
    request = pywikibot.data.api.Request(site=site, **params)
    response = request.submit()
    # Extract page content
    pages = response.get("query", {}).get("pages", {})
    page_content = next(iter(pages.values())).get("revisions", [{}])[0].get("*", "")
    return page_content

# Example: Fetch Wiktionary data for "articulate"
word = "articulate"

# *** Method 1 ***
page = pywikibot.Page(site, word)
page_text = page.text
# *** Method 2 ***
# page_text = fetch_wiktionary_text(word)
st.code(page_text)



def parse_wikitext_to_dict(text):
    """Parses raw WikiText into a structured five-level dictionary.""" 
    lines = text.split("\n")
    text_to_dict = {}
    stack = [text_to_dict]  # Stack to track nested levels
    section_levels = {}  # Track previous sections and their nesting levels

    for line in lines:
        # Match headings with = signs
        match = re.match(r"^(=+)\s*(.*?)\s*\1$", line)
        if match:
            level = len(match.group(1))  # Number of '=' determines hierarchy
            title = match.group(2)
            # Navigate stack to correct depth
            while len(stack) >= level:
                stack.pop()
            # Create new nested dictionary
            stack[-1][title] = {}
            stack.append(stack[-1][title])
        elif line.strip():  # Non-empty lines (content)
            stack[-1].setdefault("content", []).append(line.strip())
    return text_to_dict

# Example: Fetch Wiktionary data for "articulate"
parsed_dict = parse_wikitext_to_dict(page_text)
st.write(parsed_dict)

st.write('---')

st.write(json.dumps(parsed_dict, indent=4, ensure_ascii=False))





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
ss = [{"word":"articulation","phonetics":[{"audio":"https://api.dictionaryapi.dev/media/pronunciations/en/articulation-au.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=75729565","license":{"name":"BY-SA 4.0","url":"https://creativecommons.org/licenses/by-sa/4.0"}},{"text":"/ɑːˌtɪk.jəˈleɪ.ʃən/","audio":""},{"text":"/ɑɹˌtɪk.jəˈleɪ.ʃən/","audio":"https://api.dictionaryapi.dev/media/pronunciations/en/articulation-us.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=194530","license":{"name":"BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"}}],"meanings":[{"partOfSpeech":"noun","definitions":[{"definition":"A joint or the collection of joints at which something is articulated, or hinged, for bending.","synonyms":[],"antonyms":[],"example":"The articulation allowed the robot to move around corners."},{"definition":"A manner or method by which elements of a system are connected.","synonyms":[],"antonyms":[]},{"definition":"The quality, clarity or sharpness of speech.","synonyms":[],"antonyms":[],"example":"His volume is reasonable, but his articulation could use work."},{"definition":"The manner in which a phoneme is pronounced.","synonyms":[],"antonyms":[]},{"definition":"The manner in which something is articulated (tongued, slurred or bowed).","synonyms":[],"antonyms":[],"example":"The articulation in this piece is tricky because it alternates between legato and staccato."},{"definition":"The interrelation and congruence of the flow of data between financial statements of an entity, especially between the income statement and balance sheet.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/articulation"]}]
st.write(ss)

