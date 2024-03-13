from dotenv import load_dotenv
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import TextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import json
import PyPDF2
import chromadb
chroma_client = chromadb.Client()

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DIRECTORY_PATH='/Users/matansharon/python/chat_with_docs/AI_Apps/chat_with_txt/data'





def get_documents_names():
    documents_names = os.listdir(DIRECTORY_PATH)
    return documents_names
def load_all_docs_in_data_folder(documents_names):
    data_documents= []
    for doc in documents_names:
        path=os.path.join(DIRECTORY_PATH+'/',doc)
        Document=PyPDF2.PdfReader(path)
        text = ''
        for page in Document.pages:
            text += page.extract_text()
        data_documents.append(text)
        
    return data_documents
    
    

def split_text(text:str):
    
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )
    chunks=text_splitter.split_text(text)
    return chunks

def create_new_db(chunks):
    
    path='chroma_db'
    if chunks:
        
        db=Chroma.from_texts(texts=chunks,embedding=OpenAIEmbeddings(model='text-embedding-3-small'),persist_directory=path)
        return db
    if not os.path.exists(path):
        
        db=Chroma.from_texts(texts=[''],embedding=OpenAIEmbeddings(model='text-embedding-3-small'),persist_directory=path)
        return db
    return load_db()

def load_db():
    db = Chroma(persist_directory="chroma_db",embedding_function=OpenAIEmbeddings(model='text-embedding-3-small'))
    return db

def get_results_with_scores(query,db):
    
    res=db.similarity_search_with_relevance_scores(query,k=3)
    value_results=[]
    
    for i in res:
        score=i[1]
        if score>0 and score<0.5:
            value_results.append(i)
    return value_results
def get_prompt_template(results,query):
    if len(results)==0:
        # template="""
        # start the answer with the sentence: "i don't have any context to rely on so i give you the answer base on my previous knowledge."
        # and then add you answer for this {query}
        # """
        # return template
        return query
    template="""
    answer the question base only on the following context:
    {context}
    answer the question base on the above context: {query}
    
    """
    context_texts = []
    for i in range(len(results)):
        context_texts.append(results[i][0].page_content)
    temp = "\n\n---\n\n".join(context_texts)
    prompt_tamplate=ChatPromptTemplate.from_template(template)
    res=prompt_tamplate.format(context=temp,query=query)
    return res

def get_response(query,db,model):
    results=get_results_with_scores(query,db)
    prompt_template=get_prompt_template(results,query)
    response=model.invoke(prompt_template)
    return response.content

def main_app():

    documents_names=get_documents_names()
    docs=load_all_docs_in_data_folder(documents_names=documents_names)
    splited_docs=[]
    for doc in docs:
        chunks=split_text(doc)
        for chunk in chunks:
            splited_docs.append(chunk)
            
    print('splited_docs',len(splited_docs))
    db=create_new_db(splited_docs)
    model=ChatOpenAI()
    
    return db,model,documents_names

