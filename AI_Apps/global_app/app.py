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
    st.set_page_config(page_title="Global AI Apps",page_icon="🌍",layout="wide")
    st.title("Global AI Apps")
    st.write("This app is designed to help you navigate between the different AI apps")
    st.write("Please select the app you want to use from the sidebar")
    with st.sidebar:
        file=st.file_uploader("Upload a .pdf file", type=["pdf","csv",'mp3'])
        if file:
            st.session_state['file']=file
            
        #add a dropdown menu to select the app
        app=st.selectbox("Select the app you want to use",["Chat with PDF","Chat with Audio",'Chat with CSV'])
        if app:
            st.write(app)
    if 'file' in st.session_state:
        st.write(file.type)
    
    llm=ChatOpenAI(model_name='gpt-4-turbo-preview')
    # st.write(llm)
    user_input=st.chat_input("Ask me Anything about the documents")
    if user_input:
        # st.write(f"You: {user_input}")
        with st.chat_message("Human"):
                    st.write(f"AI: {user_input}")
        response=llm.invoke(f"base your answer on the following input {user_input}")
        # st.write(f"AI: {response.content}")
        with st.chat_message("AI"):
                    st.write(f"AI: {response.content}")
        
    
    
        
if __name__=="__main__":
    main()