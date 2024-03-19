import streamlit as st
import requests
import bs4
from langchain_core.messages import AIMessage,HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import  create_stuff_documents_chain


load_dotenv()


def get_conversion_rag_chain(retriever_chain):
    llm=ChatOpenAI()
    prompt=ChatPromptTemplate.from_messages([
        ('system',"answer the following questions base on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    
    
    stuff_documents_chain= create_stuff_documents_chain(retriever_chain)

def get_response(user_input):
    return "Hello from the website!"

def get_vectorstore_from_url(url):
    loader=WebBaseLoader(url)
    document=loader.load()
    text_splitter=RecursiveCharacterTextSplitter()
    document_chunks=text_splitter.split_documents(document)
    vector_store=Chroma.from_documents(document_chunks,OpenAIEmbeddings()) 
    return vector_store

def context_retriever_chain(vector_store):
    llm=ChatOpenAI()
    retriever=vector_store.as_retriever()
    prompt=ChatPromptTemplate.from_messages(
        [MessagesPlaceholder(variable_name="chat_history"), 
         ("user", "{input}"), 
         ("user", "Hello from the website!"),
         ])
    retriever_chain=create_history_aware_retriever(llm,retriever,prompt)
    return retriever_chain



def main():
    st.set_page_config(page_title="Chat with Website", page_icon="🤖")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = [
            AIMessage("Hello! I am a bot. Ask me anything!")
        ]
    st.title("Chat with Website")
    st.header("Welcome to Chat with Website")
    st.markdown("""
    ## Instructions:
    1. Enter the URL of the website you want to chat with in the sidebar.
    2. Start chatting with the website using the input box below.
    """)
    st.subheader("Chat Box")
    with st.sidebar:
        st.write("Enter URL")
        url = st.text_input("URL")
        
        if st.button("Send") and url:
        # Add code here to send the message to the website and display the response
            st.write("You: " + url)
    
    if url is not None and url!= "":
        st.info("Please wait while we load the website...")
    else:
        url="https://en.wikipedia.org/wiki/Graphics_processing_unit"
        vectore_store = get_vectorstore_from_url(url)
    
        retriever_chain = context_retriever_chain(vector_store=vectore_store)
            
        user_query= st.text_input("Type your message here")
        if user_query and user_query!="":
            response=get_response(user_query)
            st.write("You: " + user_query)
            st.session_state['chat_history'].append(HumanMessage(user_query))
            st.session_state['chat_history'].append(AIMessage(user_query)) 
            
            
            
            
    st.write("Chat History")
    for message in st.session_state['chat_history']:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("User"):
                st.write(message.content)
    
    

if __name__ == "__main__":
    main()