# Importing dependencies
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()

# Basic information for page
st.set_page_config(page_title="All About your CSV")
selected_page = st.radio("Select Feature", ("Chatbot", "Data Visualizer"))

# Radio box to select Page
if selected_page == "Chatbot":
    st.header("Ask Your CSV")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def update_sidebar():
        st.sidebar.subheader("Query History")
        for message in st.session_state.messages:
            if message['role'] == 'user':
                st.sidebar.info(message['content'])

    # Display messages in main chat area
    def display_messages():
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    prompt = st.chat_input("What is up?")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner('Processing...'):
            # Send query to Flask backend
            payload = {
                "question": prompt
            }
            try:
                # Request to Backend
                response = requests.post("http://localhost:5000/api/rag", json=payload)
                response.raise_for_status()
                answer = response.json().get("answer", "No answer found.")
            except requests.exceptions.RequestException as e:
                answer = f"Error: {e}"

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
    update_sidebar()

# Data Visualizer Page
else:
    @st.cache_data
    def load_data():
        df = pd.read_csv(os.environ['FILE_NAME'])  
        return df

    # Load CSV data
    df = load_data()

    # Display header and initial rows of the CSV
    st.header("CSV Data")
    st.write(df.head())

    # Plotting section
    st.header("Data Visualization")

    # Sidebar for plot options
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Bar Chart", "Line Chart"])

    if plot_type == "Bar Chart":
        # Bar chart plot
        x_column = st.sidebar.selectbox("Select X-axis column", df.columns)
        y_column = st.sidebar.selectbox("Select Y-axis column", df.columns)
        fig = px.bar(df, x=x_column, y=y_column, title=f"Bar Chart: {x_column} vs {y_column}")
        st.plotly_chart(fig)

    elif plot_type == "Line Chart":
        # Line chart plot
        x_column = st.sidebar.selectbox("Select X-axis column", df.columns)
        y_column = st.sidebar.selectbox("Select Y-axis column", df.columns)
        fig = px.line(df, x=x_column, y=y_column, title=f"Line Chart: {x_column} vs {y_column}")
        st.plotly_chart(fig)


