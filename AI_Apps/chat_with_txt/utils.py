from dotenv import load_dotenv
import os
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

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
    if len(res)==0 or res[0][1]<bar:
        return 'No results found'
    r=[]
    for i in range(len(res)):
        if res[i][1]>bar:
            r.append(res[i])
    return r
def get_prompt_template(results,query):
    template="""
    answer the question base only on the following context:
    {context}
    answer the question base on the above context: {query}
    
    """
    context_text="\n\n---\n\n".join([res.page_content for res,_score in results])
    prompt_tamplate=ChatPromptTemplate.from_template(template)
    res=prompt_tamplate.format(context=context_text,query=query)
    return res
def get_response(query,db,model):
    results=get_results_with_scores(query,db)
    prompt_template=get_prompt_template(results,query)
    response=model.predict(prompt_template)
    return response
def main_app():
    db=load_db()
    model=ChatOpenAI()
    return db,model
