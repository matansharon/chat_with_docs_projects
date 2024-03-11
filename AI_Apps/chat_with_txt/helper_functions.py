from dotenv import load_dotenv
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import json



load_dotenv()
DIRECTORY_PATH='/Users/matansharon/python/chat_with_docs/data/text'
DOCS_PATH='/Users/matansharon/python/chat_with_docs/AI_Apps/chat_with_txt/docs.json'



def get_all_docs():
    
    with open(DOCS_PATH,'r') as f:
        data=json.load(f)
        docs=data['documents']
    return docs

def load_all_docs_in_data_folder():
    loader = DirectoryLoader(DIRECTORY_PATH)
    documents = loader.load()
    return documents

def split_document(document):
    
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )
    chunks=text_splitter.split_documents(document)
    return chunks

def create_new_db(chunks):
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
    # pass
    documtnts=load_all_docs_in_data_folder()
    splited_documents=[]
    for doc in documtnts:
        d=split_document(doc)
        split_document.append(split_document(d))
        print(d)
    print(splited_documents)
    # db=create_new_db(documtnts)
    #for GPT-4 use this: 'gpt-4-turbo-preview'
    # model=ChatOpenAI()
    
    # return db,model
