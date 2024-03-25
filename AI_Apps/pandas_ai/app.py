import streamlit as st
import os
from langchain_core.messages import AIMessage, HumanMessage

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage, ChatMessage
from langchain_community.vectorstores.chroma import Chroma

import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
load_dotenv()


def init():
    pass


def main():
    st.title('Chat with Excel Files Using PandasAI 🐼')
    st.header('Ask me anything about the the excel files')
    st.chat_input("Ask me anything")
    with st.sidebar:
        st.write("## Database")
        st.write("### Add new file")
        file=st.file_uploader("Upload a file", type=["csv"])
        if file:
            st.write(f"{file.name} uploaded")
            st.session_state.file=file
    if "file" in st.session_state:
        df = pd.read_csv(st.session_state.file.name, encoding='ISO-8859-1')
        st.write(df.head())
        
    
    