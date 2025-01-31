import streamlit as st
import os
from phi.agent import Agent
from phi.model.google import Gemini

# Import prompts with error handling
try:
    from Prompts import SYSTEM_PROMPTS, INSTRUCTIONS
except ImportError:
    st.error("Error importing prompts. Ensure 'Prompts.py' contains SYSTEM_PROMPTS and INSTRUCTIONS.")
    SYSTEM_PROMPTS, INSTRUCTIONS = "", ""  # Fallback

# Check if API key exists
if 'GEMINI_KEY' not in st.secrets:
    st.error("Google API Key is missing in Streamlit secrets!")

# Set API key
os.environ['GOOGLE_API_KEY'] = st.secrets.get('GEMINI_KEY', '')

@st.cache_resource(show_spinner=False)
def get_agent():
    return Agent(
        model=Gemini(id="gemini-1.5-flash"),
        system_prompt=SYSTEM_PROMPTS,
        instructions=INSTRUCTIONS,
        markdown=True,
    )

def analyze_text(text):
    agent = get_agent()
    with st.spinner('Analyzing text...'):
        try:
            response = agent.run("Analyze the provided text", text=text)
            if response and response.content:
                st.markdown(response.content)
            else:
                st.error("No response received from the API.")
        except Exception as e:
            st.error(f"Error analyzing text: {e}")

def main():
    st.set_page_config(page_title="Tutor Agent", layout="wide", initial_sidebar_state="collapsed")
    st.title("📘 Tutor Agent")

    user_input = st.text_area("Enter text for analysis:", placeholder="Type or paste the chapter content here...", height=200)

    if st.button("Analyze Text"):
        if user_input.strip():
            analyze_text(user_input)
        else:
            st.warning("Please enter some text before clicking 'Analyze Text'.")

if __name__ == "__main__":
    main()


    
