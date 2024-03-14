import streamlit as st
import helper_functions as hf
from PyPDF2 import PdfReader

def add_document_to_side_bar(doc_name):
    with st.sidebar:
        st.markdown(f"- {doc_name}")

def main():
    if not("db" in st.session_state):
        st.session_state['db']=None
        st.session_state['model']=None
        st.session_state['documents_names']=None
    if st.session_state.db==None:
        db,model,documents_names=hf.main_app()
        st.session_state['db']=db
        st.session_state['model']=model
        st.session_state['documents_names']=documents_names
        
    # documents_names=["dskfnsdf","dsfsadf"]
    with st.sidebar:
        st.write("### this is the files that in the database:")
        if not(st.session_state["documents_names"]==None):
            for i in st.session_state.documents_names:
                st.markdown(f"- {i}")
    pdf = st.file_uploader("Upload a .pdf file", type=["pdf"])
    if pdf and not('db' in st.session_state):
        st.write("pdf file were uploaded")
        st.session_state.documents_names.append(pdf.name)
        
        p=PdfReader(pdf)
        add_document_to_side_bar(pdf.name)
        hf.add_document(p,db)
        pdf=None
    query=st.text_input("Ask me Anything about the documents")
    if query and not(st.session_state.db==None):
        st.write(hf.get_response(query=query,db=st.session_state.db,model=st.session_state.model))
    
if __name__== "__main__":
    main()
