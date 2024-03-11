from dotenv import load_dotenv
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

load_dotenv()
directory_path='/Users/matansharon/python/chat_with_docs/data/text'

def load_and_split_documents():
    loader = DirectoryLoader(directory_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )
    chunks=text_splitter.split_documents(documents)
    return chunks
def create_db(chunks):
    path='chroma_db'
    if not os.path.exists(path):
        
        db=Chroma.from_documents(documents=chunks,embedding=OpenAIEmbeddings(),persist_directory=path)
        return db
    return load_db()
def load_db():
    db = Chroma(persist_directory="chroma_db",embedding_function=OpenAIEmbeddings())
    return db
def get_results_with_scores(query,db):
    bar=0.5
    res=db.similarity_search_with_relevance_scores(query,k=3)
    
    return res
def get_prompt_template(results,query):
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
    pass
    # chunks=load_and_split_documents()
    # db=create_db(chunks)
    
    # model=ChatOpenAI()
    # return db,model
