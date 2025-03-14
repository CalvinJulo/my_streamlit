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

import pandas as pd
import streamlit as st
from gtts import gTTS
from io import BytesIO
import speech_recognition as sr




@st.cache_data
def text_to_audio(text,language,topleveldomain='com'):
    audio_byte = BytesIO()
    tts = gTTS(text=text, lang=language, tld=topleveldomain)
    # tts.save("output.mp3")
    tts.write_to_fp(audio_byte)
    return audio_byte
    

st.write('### Text-to-Speech (TTS) App')
accents = {
    "English (United Kingdom)": {"lang": "en", "tld": "co.uk"},
    "English (United States)": {"lang": "en", "tld": "us"},
    "English (India)": {"lang": "en", "tld": "co.in"},
    "French (France)": {"lang": "fr", "tld": "fr"},
    "Mandarin (China Mainland)": {"lang": "zh-CN", "tld": "com"},
    "Mandarin (Taiwan)": {"lang": "zh-TW", "tld": "com"},
    "Portuguese (Portugal)": {"lang": "pt", "tld": "pt"},
    "Spanish (Spain)": {"lang": "es", "tld": "es"},
}

text = st.text_area("Enter the text you want to convert to speech:",'')
# language = st.selectbox("Select language:", ["en", "es", "fr", "de", "zh-cn"])
accent = st.selectbox("Select language:", list(accents.keys()))

if text:
    audio_byte = text_to_audio(text,accents[accent]['lang'],accents[accent]['tld'])
    st.audio(audio_byte, format="audio/mp3")
    st.download_button(label="Download Speech", data=audio_byte,file_name="speech.mp3", mime="audio/mp3")


st.write('### Accent Change App')
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    st.info("🎧 Speak something...")
    try:
        audio = recognizer.listen(source, timeout=5)
        spoken_text = recognizer.recognize_google(audio)
        st.success(f"✅ You said: {spoken_text}")
    except sr.UnknownValueError:
        st.error("❌ Could not understand audio")
    except sr.RequestError:
        st.error("❌ Could not request results")

st.write(spoken_text)
