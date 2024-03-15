import streamlit as st
import helper_functions as hf
from PyPDF2 import PdfReader
from langchain_core.messages import AIMessage, HumanMessage, ChatMessage

# st.session_state['db']=None
# st.session_state['model']=None
# st.session_state['documents_names']=None
# st.session_state['first_run']=False


def main():
    
    st.set_page_config(page_title="Chat with PDF",page_icon="📚",layout="wide")
    st.title("Chat with Elcam Documnet's 📚")
    st.write("This app is designed to help you find information in your documents")
    
    if "db" not in st.session_state:
        
        db,model,documents_names=hf.main_app()
        st.session_state['db']=db
        st.session_state['model']=model
        st.session_state['documents_names']=documents_names
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[
        AIMessage("Hello and welcome to the Elcam's document chatbot"),
    ]    
    if 'documents_names' in st.session_state and st.session_state.documents_names is not None:
        with st.sidebar:
            
            file=st.sidebar.file_uploader("Upload a .pdf file", type=["pdf"])
            st.sidebar.subheader("List of files in the database:")
            if file:
                st.session_state.documents_names.append(file.name)
                p=PdfReader(file)
                hf.add_document(p,st.session_state.db)
                file=None
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
    
    if st.session_state.query and st.session_state.query!="" and st.session_state.db is not None:
        response=hf.get_response(query=st.session_state.query,db=st.session_state.db,model=st.session_state.model)
        st.session_state.chat_history.append(HumanMessage(st.session_state.query))
        st.session_state.chat_history.append(AIMessage(response))
    
    #log the conversation
    if st.session_state.chat_history:
        
        for message in st.session_state.chat_history:
            if message.type=="ai":
                with st.chat_message("AI"):
                    st.write(f"AI: {message.content}")
            else:
                with st.chat_message("Human"):
                    st.write(f"You: {message.content}")
        
        
    
if __name__== "__main__":
    main()
