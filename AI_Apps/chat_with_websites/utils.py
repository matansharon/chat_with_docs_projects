from langchain_core.messages import AIMessage,HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
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
def get_response(user_input,chat_history,vector_store,conversation_rag_chain):
    
    response = conversation_rag_chain().invoke({
                "chat_history": chat_history,
                "input": user_input
            })
    return response


def run():
    vector_store=get_vectorstore_from_url()
    retriever_chain=context_retriever_chain(vector_store=vector_store)
    conversation_rag_chain = get_conversion_rag_chain(retriever_chain=retriever_chain)
    urls=get_urls()
    return conversation_rag_chain,vector_store,retriever_chain,urls
    