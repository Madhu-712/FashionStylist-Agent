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

def answer_query(text):
    agent = get_agent()
    with st.spinner('Answering query...'):
        try:
            response = agent.run("Answer the provided query", text=text)
            if response and response.content:
                st.markdown(response.content)
            else:
                st.error("No response received from the API.")
        except Exception as e:
            st.error(f"Error answe query: {e}")

def main():
    st.set_page_config(page_title="Google Agent", layout="wide", initial_sidebar_state="collapsed")
    st.title("Google Agent")

    user_input = st.text_area("Enter queries:", placeholder="Type or paste the query.", height=200)

    if st.button("Answer Text"):
        if user_input.strip():
            analyze_text(user_input)
        else:
            st.warning("Please enter some text before clicking 'Answer query'.")

if __name__ == "__main__":
    main()


    
