import streamlit as st
import os
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage

import PyPDF2

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from pandasai.llm import OpenAI as SmartOpenAI
from openai import OpenAI

from pandasai import SmartDataframe,SmartDatalake

load_dotenv()



def init():
    st.session_state['init']=True
    st.session_state['llm']=ChatOpenAI()
    # st.session_state['llm']=ChatOpenAI(model_name='gpt-4-turbo-preview')
    st.session_state['pandas_llm']=OpenAI()
    st.session_state['pdf_file']=None
    st.session_state['csv_file']=None
    st.session_state['audio_file']=None
    st.session_state['website_url']=None
    st.session_state['app']='Chat with PDF'
    st.session_state['chat_history']=[
        AIMessage("Hello and welcome to the Global AI Apps"),
    ]



def Write_UI():
    # UI stage
    if st.session_state.app=="Chat with PDF":
        st.title("Chat with PDF's 📚")
    elif st.session_state.app=="Chat with Audio":
        st.title("Chat with Audio's 🎧")
    elif st.session_state.app=="Chat with CSV":
        st.title("Chat with CSV's 📊")
    elif st.session_state.app=="Chat with Website":
        st.title("Chat with Website's 🌍")
    
    st.subheader("This app is designed to help you navigate between the different AI apps")
    st.write("#### Please select the app you want to use from the sidebar")
    
    
    with st.sidebar:
        file=st.file_uploader("Upload a file", type=["pdf","csv",'mp3'])
        if file:
            if file.type=="application/pdf":
                st.session_state['pdf_file']=handel_pdf(file)


            elif file.type=="text/csv":
                st.session_state['csv_file']=file
            elif file.type=="audio/mpeg":
                st.session_state['audio_file']=file
            else:
                # st.write("Unsupported file type")
                st.write(file.type)
        st.session_state.website_url=st.text_input("Enter a website url")
        st.session_state.app=st.selectbox("Select the app you want to use",["Chat with PDF","Chat with Audio",'Chat with CSV','Chat with Website'],)
        
    display_chat_history()
        
def display_chat_history():
    for message in st.session_state.chat_history:
        if isinstance(message,HumanMessage):
            with st.chat_message("Human"):
                st.write(f"Human: {message.content}")
        else:
            with st.chat_message("AI"):
                st.write(f"AI: {message.content}")

def handel_pdf(file):
    if st.session_state.app:
            if st.session_state.app=="Chat with PDF":
                # text=PyPDF2.PdfReader(st.session_state.pdf_file)
                
                pages=PyPDF2.PdfReader(file).pages
                text=""
                for page in pages:
                    text+=page.extract_text()
                
                st.write('len of the uploaded text is: ',len(text))
                return text


def handel_audio():
    
    audio_file = open(st.session_state.audio_file.name, "rb")
    # return audio_file
    client=OpenAI()
    transcription = client.audio.transcriptions.create(
        
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )
    return transcription
def handel_csv():
    pass

def get_response(query):
    if st.session_state.app=="Chat with PDF":
        response=st.session_state.llm.invoke(f"base your answer on the following context {st.session_state['pdf_file']} and answer the following query: {query}")

        return response.content
    elif st.session_state.app=="Chat with Audio":
        transcription=handel_audio()
        response=st.session_state.llm.invoke(f"base your answer on the following context {transcription} and answer the following query: {query}")

        return response.content




def main():
    st.set_page_config(page_title="ALL AI Apps",page_icon="🌍",layout="wide")
    #init stage
    if 'init' not in st.session_state:
        init()
    Write_UI()


    #interaction stage

    user_input=st.chat_input("Ask me Anything...")
    if user_input:
        if st.session_state.app=="Chat with PDF":
            if st.session_state.pdf_file is None:
                st.write("Please upload a pdf file")
            else:
                response=get_response(user_input)
                st.session_state.chat_history.append(HumanMessage(user_input))
                st.session_state.chat_history.append(AIMessage(response))
                # st.write(get_response(user_input))
                display_chat_history()
        elif st.session_state.app=="Chat with Audio":
            if st.session_state.audio_file is None:
                st.write("Please upload an audio file")
            else:
                transcription=handel_audio()
                st.session_state['transcription']=transcription
                response=st.session_state.llm.invoke(f"base your answer on the following context {transcription} and answer the following query: {user_input}")
                st.session_state.chat_history.append(HumanMessage(user_input))
                st.session_state.chat_history.append(AIMessage(response.content))
                display_chat_history()
        elif st.session_state.app=="Chat with CSV":
            if st.session_state.csv_file is None:
                st.write("Please upload a csv file")
            # else:
            #     response=get_response(user_input)
            #     st.session_state.chat_history.append(HumanMessage(user_input))
            #     st.session_state.chat_history.append(AIMessage(response))
            #     display_chat_history()
        elif st.session_state.app=="Chat with Website":
            if st.session_state.website_url is None:
                st.write("Please enter a website url")
            else:
                st.write("Chat with website")
            #     response=get_response(user_input)
            #     st.session_state.chat_history.append(HumanMessage(user_input))
            #     st.session_state.chat_history.append(AIMessage(response))
            #     display_chat_history()
            
            
            


            
            
            
        
    
    #display the chat history
    
        
if __name__=="__main__":
    main()