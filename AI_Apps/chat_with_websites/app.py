import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import os


load_dotenv()
_urls=[
"https://en.wikipedia.org/wiki/2024_United_States_presidential_election",
"https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm",]
# "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm",
# "https://pubmed.ncbi.nlm.nih.gov/",
# "https://ec.europa.eu/tools/eu"]

#----------------------------------- Alejandro's code -----------------------------------
# def get_vectorstore_from_url(url):
#     # get the text in document form
#     loader = WebBaseLoader(url)
#     document = loader.load()
    
#     # split the document into chunks
#     text_splitter = RecursiveCharacterTextSplitter()
#     document_chunks = text_splitter.split_documents(document)
    
#     # create a vectorstore from the chunks
#     vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())

#     return vector_store

#----------------------------------- my code code -----------------------------------
def add_new_url(url,vector_store:Chroma):
    _urls.append(url)
    if 'vector_store' in st.session_state:
        loader = WebBaseLoader(url)
        document = loader.load()
        
    # split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter()
        document_chunks = text_splitter.split_documents(document)
        vector_store.add_documents(document_chunks)
def get_vectorstore_from_url(urls):
    if not os.path.exists("website_db"):
    # get the text in document form
        all_documents = []
        for url in urls:
            loader = WebBaseLoader(url)
            document = loader.load()
        
        # split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter()
            document_chunks = text_splitter.split_documents(document)
            all_documents.extend(document_chunks)
        
        # create a vectorstore from the chunks
        vector_store = Chroma.from_documents(all_documents, OpenAIEmbeddings())

        return vector_store
    else:
        print("Loading from disk")
        return Chroma(persist_directory="website_db",embedding_function=OpenAIEmbeddings())

def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI()
    
    retriever = vector_store.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
      ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    
    return retriever_chain
    
def get_conversational_rag_chain(retriever_chain): 
    
    llm = ChatOpenAI()
    
    prompt = ChatPromptTemplate.from_messages([
      ("system", "Answer the user's questions based on the below context:\n\n{context}"),
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm,prompt)
    
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

def get_response(user_input):
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input
    })
    
    return response['answer']

# app config
st.set_page_config(page_title="Chat with websites", page_icon="🤖")
st.title("Chat with websites ")

# sidebar
with st.sidebar:
    st.header("Settings")
    st.subheader("Choose a website to chat with")
    website_url = st.selectbox("Website URL", _urls)
    new_website_url = st.text_input("Add an URL to chat with")
    if new_website_url is not None and new_website_url != "":
        st.write(new_website_url)
        

#session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]
if "vector_store" not in st.session_state:
    st.session_state.vector_store = get_vectorstore_from_url(_urls)    

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    response = get_response(user_query)
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    st.session_state.chat_history.append(AIMessage(content=response))
    
       

    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)








#----------------------------------- Alejandro's code -----------------------------------

# if website_url is None or website_url == "":
#     st.info("Please enter a website URL")

# else:
#     # session state
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = [
#             AIMessage(content="Hello, I am a bot. How can I help you?"),
#         ]
#     if "vector_store" not in st.session_state:
#         st.session_state.vector_store = get_vectorstore_from_url(website_url)    

#     # user input
#     user_query = st.chat_input("Type your message here...")
#     if user_query is not None and user_query != "":
#         response = get_response(user_query)
#         st.session_state.chat_history.append(HumanMessage(content=user_query))
#         st.session_state.chat_history.append(AIMessage(content=response))
        
       

#     # conversation
#     for message in st.session_state.chat_history:
#         if isinstance(message, AIMessage):
#             with st.chat_message("AI"):
#                 st.write(message.content)
#         elif isinstance(message, HumanMessage):
#             with st.chat_message("Human"):
#                 st.write(message.content)