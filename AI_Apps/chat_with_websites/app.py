import streamlit as st
from utils import *

def main():
    st.set_page_config(page_title="Chat with Website", page_icon="🤖")

    st.title("Chat with Website")
    st.header("Welcome to Chat with Website")
    st.markdown("""
    ## Instructions:
    1. Enter the URL of the website you want to chat with in the sidebar.
    2. Start chatting with the website using the input box below.
    """)
    st.subheader("Chat Box")
    with st.sidebar:
        if "urls"  in st.session_state:
            for url in st.session_state["urls"]:
                st.markdown(f"- {url}")

    user_query = st.text_input("Type your message here")
    if user_query and user_query != "":
        response=get_response(user_query)
        st.write(response['answer'])
        st.session_state['chat_history'].append(HumanMessage(user_query))
        st.session_state['chat_history'].append(AIMessage(response['answer']))

    st.write("Chat History")
    for message in st.session_state['chat_history']:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("User"):
                st.write(message.content)

if __name__ == "__main__":
    if "conversion_rag_chain" not in st.session_state:
        vector_store,retriever_chain,conversion_rag_chain,urls=run()
        st.session_state["vector_store"]=vector_store
        st.session_state["retriever_chain"]=retriever_chain
        st.session_state["conversion_rag_chain"]=conversion_rag_chain
        st.session_state["urls"]=urls
        st.session_state['chat_history'] = [
                AIMessage("Hello! I am a bot. Ask me anything!")
            ]
        
    main()



















# def main():
#     st.set_page_config(page_title="Chat with Website", page_icon="🤖")
    
#     st.title("Chat with Website")
#     st.header("Welcome to Chat with Website")
#     st.markdown("""
#     ## Instructions:
#     1. Enter the URL of the website you want to chat with in the sidebar.
#     2. Start chatting with the website using the input box below.
#     """)
#     st.subheader("Chat Box")
#     with st.sidebar:
#         st.write("Enter URL")
#         url = st.text_input("URL")
        
#         if st.button("Send") and url:
#         # Add code here to send the message to the website and display the response
#             st.write("You: " + url)
    
#     if url is not None and url!= "":
#         st.info("Please wait while we load the website...")
#     else:
#         #session state initialization
#         if 'chat_history' not in st.session_state:
#             st.session_state['chat_history'] = [
#                 AIMessage("Hello! I am a bot. Ask me anything!")
#             ]
#         if "vector_store" not in st.session_state:
#             url="https://en.wikipedia.org/wiki/Graphics_processing_unit"
#             st.session_state["vector_store"]=get_vectorstore_from_url(url)
        
#         #create conversation chain

#         if "retriever_chain" not in st.session_state:
#             st.session_state["retriever_chain"] = context_retriever_chain(vector_store=st.session_state["vector_store"])
#         if "conversion_rag_chain" not in st.session_state:
#             st.session_state["conversion_rag_chain"]=get_conversion_rag_chain(st.session_state["conversion_rag_chain"])
            
        
            
#         user_query= st.text_input("Type your message here")
#         if user_query and user_query!="" and "conversion_rag_chain" in st.session_state:
#             # response=get_response(user_query)
#             response=st.session_state['conversion_rag_chain'].invoke([
#                 ("chat_history",st.session_state['chat_history']),
#                 ("input",user_query)
            
#             ])
#             st.write(response)
#             # st.session_state['chat_history'].append(HumanMessage(user_query))
#             # st.session_state['chat_history'].append(AIMessage(user_query)) 
            
            
            
            
#     st.write("Chat History")
#     for message in st.session_state['chat_history']:
#         if isinstance(message, AIMessage):
#             with st.chat_message("AI"):
#                 st.write(message.content)
#         elif isinstance(message, HumanMessage):
#             with st.chat_message("User"):
#                 st.write(message.content)
    
    

# if __name__ == "__main__":
#     main()