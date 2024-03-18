import streamlit as st

def main():
    with st.sidebar:
        st.write("Enter URL")
        url = st.text_input("URL")
        st.write(url)
    st.title("Chat with Website")
    st.header("Welcome to Chat with Website")
    st.write("Enter the URL of the website you want to chat with")
    st.write("The website should have a chatbot")
    st.write("This app will open the website and chat with the chatbot")
    st.write("The app will then display the chat history")
    st.write("The app will also display the chatbot's response")
    st.write("The app will also display the chatbot's response")
    st.write("The app will also display the chatbot's response")
    

    

if __name__ == "__main__":
    main()