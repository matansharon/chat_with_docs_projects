import streamlit as st
import helper_functions as hf


def main():
    # st.header("Chat with me")
    
    # db=hf.create_db(chunks)
    # db=hf.load_db()
    # model=hf.ChatOpenAI()
    # st.write("I am ready to chat")
    db,model=hf.main_app()
    
    
    query=st.text_input("Ask me anything")
    if query:
    
        
    # st.write(prompt_template)
        response=hf.get_response(query,db,model)
    # st.write(results[0][0].page_content)
    # st.write(db.similarity_search(query))
        st.write(response)
    
    
    
if __name__ == "__main__":
    main()