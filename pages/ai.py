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





st.write('### Text-to-Speech (TTS) App')


text = st.text_area("Enter the text you want to convert to speech:")
language = st.selectbox("Select language:", ["en", "es", "fr", "de", "zh-cn"])

if st.button("Convert to Speech"):
    if text:
        mp3_fp = BytesIO()
        tts = gTTS(text=text, lang=language, slow=False)
        # tts.save("output.mp3")
        st.success("Conversion successful! Playing audio:")
        tts_play = tts.write_to_fp(mp3_fp)

        # Play audio
        # audio_file = open("output.mp3", "rb")
        # audio_bytes = audio_file.read()
        st.audio(tts_play, format="audio/mp3")
    else:
        st.warning("Please enter some text.")
