import streamlit as st
import helper_functions as hf
from PyPDF2 import PdfReader

def add_document_to_side_bar():
    with st.sidebar:
            st.write("### this is the files that in the database:")
            if not(st.session_state["documents_names"]==None):
                for i in st.session_state.documents_names:
                    st.markdown(f"- {i}")
    print(st.session_state.documents_names)
    

def main():
    if ("db" not in st.session_state):
        st.session_state['db']=None
        st.session_state['model']=None
        st.session_state['documents_names']=None
    if st.session_state.db==None:
        db,model,documents_names=hf.main_app()
        st.session_state['db']=db
        st.session_state['model']=model
        st.session_state['documents_names']=documents_names
        add_document_to_side_bar()
        
        
        
    
    
    pdf = st.file_uploader("Upload a .pdf file", type=["pdf"])
    if pdf and ('db' in st.session_state):
        st.write("pdf file were uploaded")

        
        p=PdfReader(pdf)
        st.session_state.documents_names.append(pdf.name)
        add_document_to_side_bar()
        hf.add_document(p,st.session_state.db)
        pdf=None
    query=st.text_input("Ask me Anything about the documents")
    if query and not(st.session_state.db==None):
        st.write(hf.get_response(query=query,db=st.session_state.db,model=st.session_state.model))
    
if __name__== "__main__":
    main()
