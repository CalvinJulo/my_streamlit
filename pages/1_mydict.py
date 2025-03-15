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
from PyDictionary import PyDictionary
from gtts import gTTS
import nltk
from nltk.corpus import wordnet as wn
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# Download nltk resources
nltk.download("wordnet")

# Initialize dictionary
dictionary = PyDictionary()

# Function to get word details
def get_word_details(word):
    details = {}

    # Get Definition
    details["Definition"] = dictionary.meaning(word)

    # Get Synonyms & Antonyms
    synonyms = []
    antonyms = []
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())
    details["Synonyms"] = list(set(synonyms))
    details["Antonyms"] = list(set(antonyms))

    # Get Example Sentences
    examples = []
    for syn in wn.synsets(word):
        examples.extend(syn.examples())
    details["Examples"] = examples[:3]

    # Get Etymology (Root)
    # details["Root/Etymology"] = dictionary.get_etymology(word)

    return details

# Function to generate pronunciation
def generate_audio(text):
    tts = gTTS(text, lang="en")
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

# Streamlit UI
st.title("📖 English Dictionary with Pronunciation")
word = st.text_input("Enter a word:", "")

if word:
    details = get_word_details(word)
    st.write(details)
    
    if details["Definition"]:
        st.subheader("📌 Definition")
        for pos, defs in details["Definition"].items():
            st.write(f"**{pos.capitalize()}**: {', '.join(defs[:3])}")

    if details["Synonyms"]:
        st.subheader("🔹 Synonyms")
        st.write(", ".join(details["Synonyms"][:5]))

    if details["Antonyms"]:
        st.subheader("🔻 Antonyms")
        st.write(", ".join(details["Antonyms"][:5]))

    if details["Examples"]:
        st.subheader("📝 Example Sentences")
        for i, example in enumerate(details["Examples"], 1):
            st.write(f"{i}. {example}")
            audio = generate_audio(example)
            st.audio(audio, format="audio/mp3")

    #if details["Root/Etymology"]:
    #    st.subheader("🌱 Root & Etymology")
    #    st.write(details["Root/Etymology"])

    # Pronunciation
    st.subheader("🔊 Pronunciation")
    pronunciation_audio = generate_audio(word)
    st.audio(pronunciation_audio, format="audio/mp3")
