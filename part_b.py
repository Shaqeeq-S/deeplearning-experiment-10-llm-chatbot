
# Experiment 10 - Part B
# Prompt Handling and Response Generation
# Roll No: 24BAD109

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_response(user_message):
    if not user_message.strip():
        return "Please enter a valid prompt."

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=150
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"


# Test with five different prompts
prompts = [
    "What is Artificial Intelligence?",
    "Explain machine learning simply.",
    "What is Python?",
    "Write a short paragraph about the environment.",
    "What are the applications of chatbots?"
]

for prompt in prompts:
    print("\nUser:", prompt)
    print("Chatbot:", generate_response(prompt))
    print("-" * 50)