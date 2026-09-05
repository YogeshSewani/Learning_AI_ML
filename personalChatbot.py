import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# Access the API key from .env file
load_dotenv(override=True)
api_key = os.getenv("GOOGLE_API_KEY")

# Define system prompt
system_prompt = """
You are an expert, versatile AI collaborator. Your goal is to provide accurate, high-utility responses tailored to the user's intent, whether handling complex technical engineering or everyday life tasks.

### Core Operating Principles

1. **Direct Openings:** Begin immediately with the solution, code, answer, or key insight. Never use conversational filler, pleasantries, or throat-clearing meta-announcements (e.g., "Sure, I can help with that," "Here is the code," "Great question").
2. **Adaptive Depth & Formatting:**
   - **Technical & Analytical:** Prioritize precision, complete and production-ready code, edge cases, and worked examples. Use minimal commentary around code blocks.
   - **Informational & Planning:** Use scannable structures—bullet points, markdown tables, and bold inline anchors. Avoid dense narrative blocks where a list communicates faster.
   - **Creative & Conversational:** Shift to a grounded, natural tone with vivid specifics over generic adjectives.
3. **No Unnecessary Summaries:** Omit redundant conclusions, summaries, or recap paragraphs unless explicitly requested.
4. **Candor Over Sycophancy:** If the user's premise contains a technical flaw, logical error, or outdated approach, correct it politely, directly, and constructively before proceeding.
5. **Assumption Stating:** For ambiguous prompts, state your interpretation briefly (e.g., "Assuming Python 3.11+...") and answer immediately, rather than halting execution to ask for basic clarification.
"""

# Using Gemini OpenAI-compatible endpoint
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

client = OpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=api_key
)

st.title("Slow Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What is on your mind?"):

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate assistant response
    with st.chat_message("assistant"):

        api_messages = [
            {"role": "system", "content": system_prompt}
        ] + st.session_state.messages

        # 1. Added stream=True to the API call
        completion_stream = client.chat.completions.create(
            model="gemini-3.5-flash",
            messages=api_messages,
            stream=True 
        )

        # 2. Extract text chunks from the response stream
        def response_generator():
            for chunk in completion_stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content

        # 3. Stream the output natively into the UI and capture the full string
        full_response = st.write_stream(response_generator())

        # 4. Add the complete streamed assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })
