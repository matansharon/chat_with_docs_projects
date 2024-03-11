import streamlit as st




def main():
    st.header("Chat with me")
    msg=st.text_area("Enter your message", key="msg")
    st.button("Send")
    st.write(msg)
    
    
    
if __name__ == "__main__":
    main()