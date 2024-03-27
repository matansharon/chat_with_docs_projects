import streamlit as st
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


st.set_page_config(page_title="Chat with Audio", page_icon="🎤", layout="centered", initial_sidebar_state="expanded")
st.header("Chat with Audio 🎤")
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.chat_history = []
    st.session_state.client=OpenAI()
with st.sidebar:
    file=st.file_uploader("Upload your audio file", type=["mp3", "wav", "ogg"], key="audio")
    if file:
        st.session_state.audio_file=file
if 'audio_file' in st.session_state:
    audio_file = open(st.session_state.audio_file.name, "rb")
    transcription = st.session_state.client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )
    st.write(transcription)