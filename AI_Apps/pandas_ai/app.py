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


from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from pandasai.llm import OpenAI
from dotenv import load_dotenv
from pandasai import SmartDataframe



load_dotenv()

def init():
    llm=OpenAI()
    df=pd.read_csv('laptops.csv',encoding='ISO-8859-1')
    st.session_state.llm=llm
    st.session_state.df=df
    smart_df=SmartDataframe(df,config={'llm':llm})
    
    st.session_state.smart_df=smart_df
# 

def main():
    st.title('Chat with Excel Files Using PandasAI 🐼')
    st.header('Ask me anything about the the excel files')
    # st.chat_input("Ask me anything")
    with st.sidebar:
        st.write("## Database")
        st.write("### Add new file")
        file=st.file_uploader("Upload a file", type=["csv"])
    
if 'init' not in st.session_state:
    init()
    st.session_state.init=True
if 'df' in st.session_state:
    st.write(st.session_state.df.head())
user_input=st.chat_input("Ask me anything")
if user_input and 'smart_df' in st.session_state:
    response=st.session_state.smart_df.chat(user_input)
    st.write(response)
        


if __name__ == '__main__':
    main()
    