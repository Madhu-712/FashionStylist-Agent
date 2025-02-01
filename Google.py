from phi.agent import Agent
from phi.tools.googlesearch import GoogleSearch
import streamlit as st
import os
from phi.model.google import Gemini
from phi.tools.tavily import TavilyTools

# Define system prompt and instructions

SYSTEM_PROMPTS="""You are a google search agent that helps users search the information from the web and give response in markdown format."""
INSTRUCTIONS=""" Search a topic given by the user, respond with 4 latest news items about that topic.Give important resources by citing source,web links,book recommendations etc"""

        
# Set API keys from Streamlit secrets
os.environ['TAVILY_API_KEY'] = st.secrets['TAVILY_KEY']
os.environ['GOOGLE_API_KEY'] = st.secrets['GEMINI_KEY']

agent = Agent(
        model=Gemini(id="gemini-1.5-flash"),
        system_prompt=SYSTEM_PROMPTS,
        instructions=INSTRUCTIONS,
        tools=[TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))],
    #description="You are a search agent that helps users find the info from web",
    
        show_tool_calls=True,
        debug_mode=True,
)

st.title("🔎🔍🌐Google search Agent")

user_input = st.text_input("Enter a search topic:", "Mistral AI")

if st.button("Get info"):
    if user_input:  # Check if the user has entered something
        try:
            with st.spinner("Searching for info..."):
                response = agent.print_response(user_input, markdown=True)
                st.markdown(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a search topic.")
agent.print_response(" ", markdown=True)
