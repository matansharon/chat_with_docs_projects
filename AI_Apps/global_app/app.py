import streamlit as st
import os
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.vectorstores.chroma import Chroma
import PyPDF2

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from pandasai.llm import OpenAI
from dotenv import load_dotenv
from pandasai import SmartDataframe,SmartDatalake
load_dotenv()

def main():
    # UI stage
    st.set_page_config(page_title="Global AI Apps",page_icon="🌍",layout="wide")
    st.title("Global AI Apps")
    st.write("This app is designed to help you navigate between the different AI apps")
    st.write("Please select the app you want to use from the sidebar")
    
    #init stage
    if 'init' not in st.session_state:
        st.session_state['init']=True
        st.session_state['llm']=ChatOpenAI()
        # st.session_state['llm']=ChatOpenAI(model_name='gpt-4-turbo-preview')
        st.session_state['pandas_llm']=OpenAI()
        st.session_state['pdf_file']=None
        st.session_state['csv_file']=None
        st.session_state['audio_file']=None
        st.session_state['app']=None
        st.session_state['chat_history']=[
            AIMessage("Hello and welcome to the Global AI Apps"),
        ]
    
    #sidebar stage
    with st.sidebar:
        file=st.file_uploader("Upload a .pdf file", type=["pdf","csv",'mp3'])
        if file:
            if file.type=="application/pdf":
                st.session_state['pdf_file']=file
            elif file.type=="text/csv":
                st.session_state['csv_file']=file
            elif file.type=="audio/mpeg":
                st.session_state['audio_file']=file
                
                
            
            
        #add a dropdown menu to select the app
        st.session_state.app=st.selectbox("Select the app you want to use",["Chat with PDF","Chat with Audio",'Chat with CSV'])
    if st.session_state.app:
        if st.session_state.app=="Chat with PDF" and st.session_state.pdf_file:
            # text=PyPDF2.PdfReader(st.session_state.pdf_file)
            st.write(st.session_state.pdf_file)
            pages=PyPDF2.PdfReader(st.session_state.pdf_file).pages
            text=""
            for page in pages:
                text+=page.extract_text()
            st.write('len of the uploaded text is: ',len(text))
            
            
    
    

    #interaction stage

    user_input=st.chat_input("Ask me Anything about the documents")
    if user_input:
        
        response=st.session_state.llm.invoke(f"base your answer on the following input {user_input}")
        st.session_state.chat_history.append(HumanMessage(user_input))
        st.session_state.chat_history.append(AIMessage(response.content))
        
    
    #display the chat history
    for message in st.session_state.chat_history:
        if isinstance(message,HumanMessage):
            with st.chat_message("Human"):
                st.write(f"Human: {message.content}")
        else:
            with st.chat_message("AI"):
                st.write(f"AI: {message.content}")
        
if __name__=="__main__":
    main()