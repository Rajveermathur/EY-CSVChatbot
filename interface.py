import streamlit as st
st.set_page_config(page_title="Ask your CSV")
st.header("Ask your CSV 📈")

csv_file = st.file_uploader("Upload a CSV file", type="csv")
if csv_file is not None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    prompt = st.chat_input("What is up?")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
    
        response = f"Echo: {prompt}"
        with st.chat_message("assistant"):
            st.markdown(response)
    
        st.session_state.messages.append({"role": "assistant", "content": response})

