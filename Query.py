
# Required installations:
# pip install phidata google-generativeai streamlit

import streamlit as st
import os
from phi.agent import Agent
from phi.model.google import Gemini
from Prompts import SYSTEM_PROMPT, INSTRUCTIONS

# Set environment variables for API keys
os.environ['GOOGLE_API_KEY'] = st.secrets['GEMINI_KEY']

@st.cache_resource
def get_agent():
    return Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        system_prompt=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        markdown=True,
    )

def analyze_text(text):
    agent = get_agent()
    with st.spinner('Analyzing text...'):
        response = agent.run(
            "Analyze the provided text",
            text=text,
        )
        st.markdown(response.content)

def main():
    st.title("📘 Tutor Agent")

    # Text input area
    user_input = st.text_area(
        "Enter text for analysis:",
        placeholder="Type or paste the chapter content here...",
        height=200
    )

    if st.button("Analyze Text"):
        if user_input.strip():
            analyze_text(user_input)
        else:
            st.warning("Please enter some text before clicking 'Analyze Text'.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Tutor Agent",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()
