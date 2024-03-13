import streamlit as st
import helper_functions as hf
from PyPDF2 import PdfReader

def main():
    db,model,documents_names=hf.main_app()
    with st.sidebar:
        st.write("### this is the files that in the database:")
        for i in documents_names:
            st.markdown(f"- {i}")
    pdf = st.file_uploader("Upload a .pdf file", type=["pdf"])
    if pdf:
        st.write("pdf file were uploaded")
    query=st.text_input("Ask me Anything about the documents")
    if query:
        st.write(hf.get_response(query=query,db=db,model=model))
    
    
if __name__ == "__main__":
    main()