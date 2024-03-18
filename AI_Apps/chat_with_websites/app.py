import streamlit as st

def main():
    with st.sidebar:
        st.write("Enter URL")
        url = st.text_input("URL")
        st.write(url)
    st.title("Chat with Website")
    st.header("Welcome to Chat with Website")
    
    
    st.markdown("""
    ## Instructions:
    1. Enter the URL of the website you want to chat with in the sidebar.
    2. Start chatting with the website using the input box below.
    """)

    st.subheader("Chat Box")
    message = st.text_input("Type your message here")

    if st.button("Send"):
        # Add code here to send the message to the website and display the response
        st.write("You: " + message)

    st.subheader("Website Response")
    # Add code here to display the response from the website
    

if __name__ == "__main__":
    main()