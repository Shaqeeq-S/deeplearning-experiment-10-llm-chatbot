# Experiment 10 - Part D
# Testing and Deployment of LLM Chatbot
# Roll No: 24BAD109

import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Read API key
api_key = os.getenv("OPENROUTER_API_KEY")

# Support Streamlit Cloud secrets
if not api_key:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        api_key = None

# Page configuration
st.set_page_config(
    page_title="LLM Chatbot - Experiment 10",
    page_icon="💬",
    layout="centered"
)

st.title("LLM Chatbot")
st.caption("Experiment 10 - Part D: Testing and Deployment")

# Sidebar settings
st.sidebar.header("Chatbot Settings")

max_tokens = st.sidebar.selectbox(
    "Maximum response length",
    [100,500, 1000, 1500, 2500, 4000],
    index=2
)

st.sidebar.info(
    "Choose a higher token limit for longer answers. "
    "Actual output depends on the selected model."
)

if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

# Initialize conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Check API key
if not api_key:
    st.error(
        "API key not found. Add OPENROUTER_API_KEY "
        "to your .env file or Streamlit secrets."
    )
    st.stop()

# Configure OpenRouter
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Detailed response instructions
system_message = """
You are a helpful AI chatbot for educational purposes.

Answer the user's questions accurately and clearly.
Give detailed, complete explanations with relevant headings,
examples, and step-by-step points whenever appropriate.

For educational questions, explain the definition, working,
applications, advantages, and examples when relevant.
Avoid unnecessarily short answers.

Do not stop an explanation before completing the main points.
If you are uncertain about a fact, state the uncertainty clearly.
"""

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Example prompts
with st.expander("Try sample test prompts"):
    st.markdown("""
    1. Explain Artificial Intelligence and its applications in detail.
    2. Explain how machine learning works with examples.
    3. Discuss the advantages and limitations of LLM chatbots.
    4. Explain the Transformer architecture step by step.
    5. Write a detailed essay about environmental protection.
    """)

# User input
user_input = st.chat_input("Ask a question...")

if user_input:
    # Save and display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate detailed response
    with st.chat_message("assistant"):
        with st.spinner("Generating a detailed response..."):
            try:
                response = client.chat.completions.create(
                    model="openrouter/free",
                    messages=[
                        {
                            "role": "system",
                            "content": system_message
                        },
                        *st.session_state.messages
                    ],
                    max_tokens=max_tokens
                )

                answer = response.choices[0].message.content
                finish_reason = response.choices[0].finish_reason

                if not answer:
                    answer = "The model returned an empty response."

                st.markdown(answer)

                if finish_reason == "length":
                    st.warning(
                        "The response reached the model's output limit. "
                        "Try increasing the limit or ask the chatbot "
                        "to continue the previous answer."
                    )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Unable to generate response: {e}")