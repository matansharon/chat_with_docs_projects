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
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import  create_stuff_documents_chain


load_dotenv()




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


def get_conversion_rag_chain(retriever_chain):
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ('system', "answer the following questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    # Correctly call create_retrieval_chain with the retriever_chain and stuff_documents_chain
    combined_retrieval_chain = create_retrieval_chain(retriever_chain, stuff_documents_chain)
    return combined_retrieval_chain


def main():
    st.set_page_config(page_title="Chat with Website", page_icon="🤖")
    
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
        #session state initialization
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = [
                AIMessage("Hello! I am a bot. Ask me anything!")
            ]
        if "vector_store" not in st.session_state:
            url="https://en.wikipedia.org/wiki/Graphics_processing_unit"
            st.session_state["vector_store"]=get_vectorstore_from_url(url)
        
        #create conversation chain

        if "retriever_chain" not in st.session_state:
            st.session_state["retriever_chain"] = context_retriever_chain(vector_store=st.session_state["vector_store"])
        if "conversion_rag_chain" not in st.session_state:
            st.session_state["conversion_rag_chain"]=get_conversion_rag_chain(st.session_state["conversion_rag_chain"])
            
        
            
        user_query= st.text_input("Type your message here")
        if user_query and user_query!="" and "conversion_rag_chain" in st.session_state:
            # response=get_response(user_query)
            response=st.session_state['conversion_rag_chain'].invoke([
                ("chat_history",st.session_state['chat_history']),
                ("input",user_query)
            
            ])
            st.write(response)
            # st.session_state['chat_history'].append(HumanMessage(user_query))
            # st.session_state['chat_history'].append(AIMessage(user_query)) 
            
            
            
            
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