import streamlit as st
import helper_functions as hf
from PyPDF2 import PdfReader

def add_document_to_side_bar(doc_name):
    with st.sidebar:
        st.markdown(f"- {doc_name}")
flag=True
if flag:
    db,model,documents_names=hf.main_app()
    flag=False
# documents_names=["dskfnsdf","dsfsadf"]
with st.sidebar:
    st.write("### this is the files that in the database:")
    for i in documents_names:
        st.markdown(f"- {i}")
pdf = st.file_uploader("Upload a .pdf file", type=["pdf"])
if pdf:
    st.write("pdf file were uploaded")
    documents_names.append(pdf.name)
    # text=hf.add_document(pdf)
    p=PdfReader(pdf)
    hf.add_document(p,db)
    pdf=None
query=st.text_input("Ask me Anything about the documents")
if query:
    st.write(hf.get_response(query=query,db=db,model=model))
    
    
