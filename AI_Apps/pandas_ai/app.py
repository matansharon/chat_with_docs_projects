import streamlit as st
import os


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



# API_TOKEN = os.getenv('OPENAI_API_KEY')
load_dotenv()

def init():
    llm=OpenAI()
    df=pd.read_csv('laptops.csv',encoding='ISO-8859-1')
    st.session_state.llm=llm
    st.session_state.df=df
    smart_df=SmartDataframe(df,config={'llm':llm})
    smart_lake=SmartDatalake([df,df2],config={'llm':llm})
    st.session_state.smart_df=smart_df
    st.session_state.smart_lake=smart_lake
# 


st.set_page_config(page_title="Chat with Excel", page_icon="📈")
st.title('Chat with Excel Files Using PandasAI 🐼')


with st.sidebar:
    st.write("## Database")
    st.write("### Add new file")
    # file=st.file_uploader("Upload a file", type=["csv"])

if 'init' not in st.session_state:
    llm=OpenAI()
    df=pd.read_csv('/Users/matansharon/python/chat_with_doc/AI_Apps/pandas_ai/laptops.csv',encoding='ISO-8859-1')
    df2=pd.read_csv('/Users/matansharon/python/chat_with_doc/AI_Apps/pandas_ai/Sales Summary.csv',encoding='ISO-8859-1')
    st.session_state.llm=llm
    st.session_state.df=df
    smart_df=SmartDataframe(df,config={'llm':llm})
    
    st.session_state['smart_df']=smart_df
    st.session_state['smart_lake']=SmartDatalake([df,df2],config={'llm':llm})
    st.session_state.init=True
    
    
    
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]
user_input=st.chat_input("Ask me anything")
if user_input and user_input!="" and 'smart_df' in st.session_state and 'chat_history' in st.session_state:
    response=st.session_state.smart_lake.chat(user_input)
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    try:
        
        st.session_state.chat_history.append(AIMessage(content=response))
    except:
        st.session_state.chat_history.append(AIMessage(content="here is the answer: ",additional_kwargs={"content":response}))
        
if "chat_history" in st.session_state:
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
                if message.additional_kwargs:
                    st.write(message.additional_kwargs.get("content"))
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)
    
