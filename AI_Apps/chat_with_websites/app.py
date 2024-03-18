import streamlit as st

def main():
    with st.sidebar:
        st.write("Enter URL")
        url = st.text_input("URL")
        st.write(url)

if __name__ == "__main__":
    main()