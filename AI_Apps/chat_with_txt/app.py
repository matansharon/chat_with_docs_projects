import streamlit as st
import helper_functions as hf


def main():
    # st.header("Chat with me")
    chunks=hf.load_and_split_documents()
    db=hf.create_db(chunks)
    model=hf.ChatOpenAI()
    # st.write("I am ready to chat")
    
    
    
    query="what is qlora?"
    results=hf.get_results_with_scores(query,db)
    prompt_template=hf.get_prompt_template(results,query)
    st.write(prompt_template)
    # st.write(results[0][0].page_content)
    # st.write(db.similarity_search(query))
    
    
    
    
if __name__ == "__main__":
    main()