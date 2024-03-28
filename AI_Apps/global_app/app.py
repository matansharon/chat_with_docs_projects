import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    st.set_page_config(page_title="Global AI Apps",page_icon="🌍",layout="wide")
    st.title("Global AI Apps")
    st.write("This app is designed to help you navigate between the different AI apps")
    st.write("Please select the app you want to use from the sidebar")
    with st.sidebar:
        file=st.file_uploader("Upload a .pdf file", type=["pdf","csv",'mp3'])
        if file:
            st.session_state['file']=file
    if 'file' in st.session_state:
        st.write(file.type)
    
        
if __name__=="__main__":
    main()