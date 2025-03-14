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



@st.cache_data
def text_to_audio(text,language):
    audio_byte = BytesIO()
    tts = gTTS(text=text, lang=language, slow=False)
    # tts.save("output.mp3")
    tts.write_to_fp(audio_byte)
    return audio_byte
    

st.write('### Text-to-Speech (TTS) App')

accents = {
    "English (US)": "en",
    "English (UK)": "en-uk",
    "English (Australia)": "en-au",
    "French": "fr",
    "Spanish": "es"
}

text = st.text_area("Enter the text you want to convert to speech:",'')
# language = st.selectbox("Select language:", ["en", "es", "fr", "de", "zh-cn"])
language = st.selectbox("Select language:", list(accents.keys()))

if text:
    audio_byte = text_to_audio(text,accents[language])
    st.audio(audio_byte, format="audio/mp3")
    st.download_button(label="Download Speech", data=audio_byte,file_name="speech.mp3", mime="audio/mp3")
