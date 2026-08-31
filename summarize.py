import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY")
)

system_prompt = "You are a helpful assistant that summarizes websites. You are given a website, and you need to summarize the website in a few sentences."
user_prompt_prefix = "Here are the contents of a website. Provide a short summary of this website. If it includes news or announcements, then summarize these too:\n"

st.title("Website Summarizer")
website = st.text_input("Enter a website URL or text: ")
button = st.button("Generate Summary")

def summarize_website(content):
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt_prefix + content}
        ]
    )
    return response.choices[0].message.content

if website:
    if button:
        summary = summarize_website(website)
        st.success.markdown(summary)
