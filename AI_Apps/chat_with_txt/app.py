import streamlit as st
from utils import *



def main():
    st.header("Chat with me")
    
    db,model=main_app()
    st.write('Ask me anything')
    query=st.text_input('Your question')
    if query:
        response=get_response(query,db,model)
        if response=='No results found':
            st.write('No results found')
        else:
            st.write(response)
    
    
if __name__ == "__main__":
    main()