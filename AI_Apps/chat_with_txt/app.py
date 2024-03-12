import streamlit as st
from helper_functions import *
from PyPDF2 import PdfReader

def main():
    # db,model=main_app()
    query=st.text_input("Ask me anything")
    # if query:
    #     # response=get_response(query,db,model)
    #     st.write(response)
    file=st.file_uploader("Upload file")
    if file:
        st.write(file)
        pdf=PdfReader(file).pages[0].extract_text()
        st.write(pdf)
if __name__ == "__main__":
    main()