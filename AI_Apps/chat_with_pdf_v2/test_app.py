import streamlit as st
from random import randint


def write_sidebar():
    
    if len(st.session_state.doc_names)>0:
        for doc in st.session_state.doc_names:
            st.sidebar.markdown(f"- {doc}")

def generate_word():
    
    res=''
    ab="abcdefghijklmnopqrstuvwxyz"
    for i in range(10):
        pos=randint(0, 24)
        res+=ab[pos]
    st.session_state.doc_names.append(res)
    write_sidebar()
def main():
    st.header("testing vegeterians!📖")
    if "doc_names" not in st.session_state:
        st.session_state['doc_names']=[]
    
    
    
    
    st.button("Process",on_click=generate_word())
    
if __name__== "__main__":
    main()