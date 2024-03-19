
import streamlit as st
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

def get_urls():
    return["https://en.wikipedia.org/wiki/2024_United_States_presidential_election,"
           
        
    ]
def get_vectorstore_from_url(url):
    url="https://en.wikipedia.org/wiki/2024_United_States_presidential_election"
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

def get_response(user_input):
    conversation_rag_chain=st.session_state.conversion_rag_chain
    response = conversation_rag_chain.invoke({
                "chat_history": st.session_state.chat_history,
                "input": user_input
            })
    context=""
    for res in response:
        context+=res.page_content
    llm=ChatOpenAI()
    return llm.invoke(f"answer the following questions based on the below context:\n\n{context}")


def initialize_session_state():
    vector_store, retriever_chain, conversion_rag_chain, urls = run()
    st.session_state["vector_store"] = vector_store
    st.session_state["retriever_chain"] = retriever_chain
    st.session_state["conversion_rag_chain"] = conversion_rag_chain
    st.session_state["urls"] = urls
    st.session_state['chat_history'] = [AIMessage("Hello! I am a bot. Ask me anything!")]

def run():
    urls=get_urls()
    vector_store=get_vectorstore_from_url(urls)
    retriever_chain=context_retriever_chain(vector_store=vector_store)
    conversation_rag_chain = get_conversion_rag_chain(retriever_chain=retriever_chain)
    
    return conversation_rag_chain,vector_store,retriever_chain,urls


    

    






def main():
    if "conversion_rag_chain" not in st.session_state:
        initialize_session_state()
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
        if "urls"  in st.session_state:
            for url in st.session_state["urls"]:
                st.markdown(f"- {url}")

    user_query = st.text_input("Type your message here")
    if user_query and user_query != "" and 'chat_history' in st.session_state and "vector_store" in st.session_state and "conversion_rag_chain" in st.session_state and "retriever_chain" in st.session_state:
        response=get_response(user_query)
        st.write(response.content)
        st.session_state['chat_history'].append(HumanMessage(user_query))
        st.session_state['chat_history'].append(AIMessage(response.content))

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