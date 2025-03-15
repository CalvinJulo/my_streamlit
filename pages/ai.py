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


# related audio library: pytorch, pyaudio, pyworld, soundfile, sounddevice, pydub, soundillusionist, torchaudio, speech_recognition,pyttsx3

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
import streamlit as st

audio_data = st.audio_input("Record a voice message")

if audio_data:
    st.audio(audio_data)




from pydub import AudioSegment
import numpy as np
import soundfile as sf

if audio_data:
    # Convert audio data to a format Pydub can use
    audio_bytes = audio_data.read()
    audio = AudioSegment.from_file(BytesIO(audio_bytes), format="wav")

    st.audio(audio_bytes, format="audio/wav", start_time=0)

    # Pitch shift (increase or decrease pitch)
    pitch_shift = st.slider("🎚️ Change pitch", -5, 5, 0)
    speed_change = st.slider("⚡ Change speed", 0.5, 2.0, 1.0)

    # Apply effects
    if pitch_shift != 0:
        audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * (2.0 ** (pitch_shift / 12.0)))
        }).set_frame_rate(audio.frame_rate)

    # Change speed
    if speed_change != 1.0:
        audio = audio.speedup(playback_speed=speed_change)

    # Export edited audio
    buffer = BytesIO()
    audio.export(buffer, format="wav")
    st.audio(buffer, format="audio/wav")




'''
import speech_recognition as sr

st.title("🎙️ Speech to Text Converter")

# Recorder for live speech input
recognizer = sr.Recognizer()

st.write("Click 'Start Recording' and speak...")

if st.button("Start Recording"):
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)  # Using Google’s free STT
            st.success("Transcription:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand the audio.")
        except sr.RequestError:
            st.error("Could not request results; please check your internet connection.")

st.write("🎉 Done!")

'''
