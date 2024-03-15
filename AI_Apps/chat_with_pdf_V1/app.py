import streamlit as st
import helper_functions as hf
from PyPDF2 import PdfReader
from langchain_core.messages import AIMessage, HumanMessage, ChatMessage

st.session_state['db']=None
st.session_state['model']=None
st.session_state['documents_names']=None
st.session_state['first_run']=False


def main():
    
    st.set_page_config(page_title="Chat with PDF",page_icon="📚",layout="wide")
    st.title("Chat with Elcam Documnet's 📚")
    st.write("This app is designed to help you find information in your documents")
    
    if st.session_state.db==None:
        
        db,model,documents_names=hf.main_app()
        st.session_state['db']=db
        st.session_state['model']=model
        st.session_state['documents_names']=documents_names
        
        
    if 'documents_names' in st.session_state:
        with st.sidebar:
            st.sidebar.subheader("List of files in the database:")
            for doc in st.session_state.documents_names:
                st.sidebar.markdown(f"- {doc}")
    # הקטע קוד כאן הוא בגרסה שאפשר להוסיף מסמכים דינמית
    # pdf = st.file_uploader("Upload a .pdf file", type=["pdf"])
    # if pdf :
    #     st.write("pdf file were uploaded")
    #     p=PdfReader(pdf)

        
    #     hf.add_document(p,st.session_state.db)
    #     pdf=None
    
    #add the AI and humen messages

    
    st.session_state.query=st.chat_input("Ask me Anything about the documents")
    with st.chat_message("AI"):
        st.write("AI: Hello and welcome to the Elcam's document chatbot")
    if st.session_state.query and not(st.session_state.db==None):
        
        response=hf.get_response(query=st.session_state.query,db=st.session_state.db,model=st.session_state.model)
        with st.chat_message("Human"):
            st.write(f"You: {st.session_state.query}")
        with st.chat_message("AI"):
            st.write(f"AI: {response}")
        st.session_state.query=""  
        
        
    
if __name__== "__main__":
    main()
