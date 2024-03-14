import streamlit as st
import helper_functions as hf
from PyPDF2 import PdfReader

    
    


def main():
    if ("db" not in st.session_state):
        st.session_state['db']=None
        st.session_state['model']=None
        st.session_state['documents_names']=None
        st.session_state['first_run']=False
        
    if st.session_state.db==None:
        
        db,model,documents_names=hf.main_app()
        st.session_state['db']=db
        st.session_state['model']=model
        st.session_state['documents_names']=documents_names
        
    if 'documents_names' in st.session_state:
        with st.sidebar:
            for doc in st.session_state.documents_names:
                st.sidebar.markdown(f"- {doc}")
    pdf = st.file_uploader("Upload a .pdf file", type=["pdf"])
    if pdf :
        st.write("pdf file were uploaded")
        p=PdfReader(pdf)

        
        hf.add_document(p,st.session_state.db)
        pdf=None
    query=st.text_input("Ask me Anything about the documents")
    if query and not(st.session_state.db==None):
        st.write(hf.get_response(query=query,db=st.session_state.db,model=st.session_state.model))
        
    
if __name__== "__main__":
    main()
