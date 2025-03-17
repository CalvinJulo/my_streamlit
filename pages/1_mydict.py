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


# family = pywikibot.family.WikimediaFamily.content_families
# st.write(family)


word = "articulate"


# Connect to English Wiktionary
site = pywikibot.Site("en", "wiktionary")
page = pywikibot.Page(site, word)
page_text = page.text



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


def extract_pronunciation(data):
    """Extract IPA and audio files from Pronunciation section."""
    pronunciation_data = data.get("content", [])
    ipa_list = []
    audio_list = []
    for line in pronunciation_data:
        ipa_match = re.findall(r"[^|]*\/", line)
        if ipa_match:
            ipa_list.extend(ipa_match)   
        audio_match = re.findall(r"[^|]*\.ogg", line)
        if audio_match:
            audio_list.extend(audio_match)
    return {"IPA": ipa_list, "Audio": audio_list}

def extract_word_list(section_data):
    """Extract words from bullet-point lists."""
    words = []
    for line in section_data.get("content", []):
        match = re.match(r"^\*+\s*\[\[(.*?)\]\]", line)  # Match [[word]]
        if match:
            words.append(match.group(1))
    return words

def extract_definitions_and_examples(part_of_speech_data):
    """Extract definitions and examples from adjective, noun, verb sections."""
    definitions = []
    examples = []
    
    for line in part_of_speech_data.get("content", []):
        if line.startswith("# "):  # Definition
            definitions.append(line[2:])
        elif line.startswith("#* "):  # Example
            examples.append(line[3:])
    
    return {"Definitions": definitions, "Examples": examples}

def refine_wiktionary_data(parsed_data):
    """Refine parsed Wiktionary data, keeping multiple Etymologies."""
    refined = {}

    for etymology_key in parsed_data:
        if etymology_key.startswith("Etymology"):
            etymology_data = parsed_data[etymology_key]
            refined[etymology_key] = {}

            # Extract pronunciation if present
            if "Pronunciation" in etymology_data:
                refined[etymology_key]["Pronunciation"] = extract_pronunciation(etymology_data["Pronunciation"])

            # Extract lists
            for section in ["Synonyms", "Derived terms", "Translations", "Related terms"]:
                if section in etymology_data:
                    refined[etymology_key][section] = extract_word_list(etymology_data[section])

            # Extract Part of Speech (Noun, Verb, Adjective)
            for pos in ["Noun", "Verb", "Adjective"]:
                if pos in etymology_data:
                    refined[etymology_key][pos] = extract_definitions_and_examples(etymology_data[pos])

    return refined



parsed_dict = parse_wikitext_to_dict(page_text)
refined_data = refine_wiktionary_data(parsed_dict)



st.write(f'{parsed_dict}')
st.write(parsed_dict)
st.write(refined_data)

tt ='https://api.dictionaryapi.dev/api/v2/entries/en/articulate'
ss = [{"word":"articulation","phonetics":[{"audio":"https://api.dictionaryapi.dev/media/pronunciations/en/articulation-au.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=75729565","license":{"name":"BY-SA 4.0","url":"https://creativecommons.org/licenses/by-sa/4.0"}},{"text":"/ɑːˌtɪk.jəˈleɪ.ʃən/","audio":""},{"text":"/ɑɹˌtɪk.jəˈleɪ.ʃən/","audio":"https://api.dictionaryapi.dev/media/pronunciations/en/articulation-us.mp3","sourceUrl":"https://commons.wikimedia.org/w/index.php?curid=194530","license":{"name":"BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"}}],"meanings":[{"partOfSpeech":"noun","definitions":[{"definition":"A joint or the collection of joints at which something is articulated, or hinged, for bending.","synonyms":[],"antonyms":[],"example":"The articulation allowed the robot to move around corners."},{"definition":"A manner or method by which elements of a system are connected.","synonyms":[],"antonyms":[]},{"definition":"The quality, clarity or sharpness of speech.","synonyms":[],"antonyms":[],"example":"His volume is reasonable, but his articulation could use work."},{"definition":"The manner in which a phoneme is pronounced.","synonyms":[],"antonyms":[]},{"definition":"The manner in which something is articulated (tongued, slurred or bowed).","synonyms":[],"antonyms":[],"example":"The articulation in this piece is tricky because it alternates between legato and staccato."},{"definition":"The interrelation and congruence of the flow of data between financial statements of an entity, especially between the income statement and balance sheet.","synonyms":[],"antonyms":[]}],"synonyms":[],"antonyms":[]}],"license":{"name":"CC BY-SA 3.0","url":"https://creativecommons.org/licenses/by-sa/3.0"},"sourceUrls":["https://en.wiktionary.org/wiki/articulation"]}]
st.write(ss)

