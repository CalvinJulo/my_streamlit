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


family = pywikibot.family.WikimediaFamily.content_families
st.write(family)
site = pywikibot.Site("en", "wiktionary")

def parse_wiktionary_page(word):
    site = pywikibot.Site("en", "wiktionary")
    page = pywikibot.Page(site, word)

    if not page.exists():
        return {"error": "Word not found"}
    st.write(page.text)
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
word_dict = parse_wiktionary_page("articulate")

st.write(word_dict[0])
st.write(word_dict[1])



tt= [{"word":"articulate","phonetic":"/ɑː(ɹ)ˈtɪk.jʊ.lət/","phonetics":[{"text":"/ɑː(ɹ)ˈtɪk.jʊ.lət/","audio":"https://api.dictionaryapi.dev/media/pronunciations/en/articulate-1-uk.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=57060355","license":{"name":"BY-SA 4.0","url":"https://creativecommons.org/licenses/by-sa/4.0"}},{"text":"/ɑːɹˈtɪk.jə.lət/","audio":"https://api.dictionaryapi.dev/media/pronunciations/en/articulate-1-us.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=179574","license":{"name":"BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"}}],"meanings":[{"partOfSpeech":"noun","definitions":[{"definition":"An animal of the subkingdom Articulata.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]},{"partOfSpeech":"adjective","definitions":[{"definition":"Clear; effective.","synonyms":[],"antonyms":[]},{"definition":"Speaking in a clear and effective manner.","synonyms":[],"antonyms":[],"example":"She’s a bright, articulate young woman."},{"definition":"Consisting of segments united by joints.","synonyms":[],"antonyms":[],"example":"The robot arm was articulate in two directions."},{"definition":"Distinctly marked off.","synonyms":[],"antonyms":[],"example":"an articulate period in history"},{"definition":"Expressed in articles or in separate items or particulars.","synonyms":[],"antonyms":[]},{"definition":"(of sound) Related to human speech, as distinct from the vocalisation of animals.","synonyms":[],"antonyms":[]}],"synonyms":["eloquent","well-spoken"],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/articulate"]},{"word":"articulate","phonetic":"/ɑː(ɹ)ˈtɪk.jʊ.leɪt/","phonetics":[{"text":"/ɑː(ɹ)ˈtɪk.jʊ.leɪt/","audio":"https://api.dictionaryapi.dev/media/pronunciations/en/articulate-2-uk.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=57060367","license":{"name":"BY-SA 4.0","url":"https://creativecommons.org/licenses/by-sa/4.0"}},{"text":"/ɑːɹˈtɪk.jə.leɪt/","audio":"https://api.dictionaryapi.dev/media/pronunciations/en/articulate-2-us.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=179575","license":{"name":"BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"}}],"meanings":[{"partOfSpeech":"verb","definitions":[{"definition":"To make clear or effective.","synonyms":[],"antonyms":[]},{"definition":"To speak clearly; to enunciate.","synonyms":[],"antonyms":[],"example":"I wish he’d articulate his words more clearly."},{"definition":"To explain; to put into words; to make something specific.","synonyms":[],"antonyms":[],"example":"I like this painting, but I can’t articulate why."},{"definition":"To bend or hinge something at intervals, or to allow or build something so that it can bend.","synonyms":[],"antonyms":[],"example":"an articulated bus"},{"definition":"To attack a note, as by tonguing, slurring, bowing, etc.","synonyms":[],"antonyms":[],"example":"Articulate that passage heavily."},{"definition":"To form a joint or connect by joints","synonyms":[],"antonyms":[],"example":"The lower jaw articulates with the skull at the temporomandibular joint."},{"definition":"To treat or make terms.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/articulate"]}]
st.write(tt)

