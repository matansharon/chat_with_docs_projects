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
    if st.button("Show summary") and 'transcription' in st.session_state:
        audio_file = open(st.session_state.audio_file.name, "rb")
        complition=st.session_state.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "the following is a transcription. Please summarize it."},
            {"role": "user", "content": st.session_state.transcription},
        ]
        )
        st.write("here is a summerztion of the audio file: ")
        st.write(complition.choices[0].message.content)
if 'audio_file' in st.session_state:
    audio_file = open(st.session_state.audio_file.name, "rb")
    transcription = st.session_state.client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )
    st.session_state.transcription=transcription
user_query=st.chat_input("Type something...")
if user_query:
    response = st.session_state.client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. base your answers on the following transcription: "+st.session_state.transcription},
        {"role": "user", "content": user_query},
    ]
    )
    st.write(response.choices[0].message.content)
