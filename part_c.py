# Experiment 10 - Part C
# Building the Chatbot Interface
# Roll No: 24BAD109

import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Configure OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Page settings
st.set_page_config(
    page_title="LLM Chatbot",
    page_icon="💬"
)

st.title("LLM Chatbot")
st.write("Ask questions and get AI-generated answers.")

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Enter your message...")

if user_input:
    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            try:
                response = client.chat.completions.create(
                    model="openrouter/free",
                    messages=st.session_state.messages,
                    max_tokens=200
                )

                answer = response.choices[0].message.content
                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"API Error: {e}")